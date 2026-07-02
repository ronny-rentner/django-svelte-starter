import re
from datetime import datetime
import xml.etree.ElementTree as ET

from django.db import models
from pytubefix import YouTube

from djultra import fields
import djultra.models


class YouTubeVideo(djultra.models.Base):
    class Admin:
        search_fields = ['title']

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        FETCHED = 'fetched', 'Fetched'
        ERROR   = 'error',   'Error'

    video_id                      = fields.CharField(max_length=20, unique=True, blank=False)
    title                         = fields.CharField()
    status                        = fields.CharField(choices=Status.choices, default=Status.PENDING, max_length=15)
    description                   = fields.TextField(blank=True, null=True)
    thumbnail_url                 = models.URLField(blank=True, null=True)
    published_at                  = models.DateTimeField(blank=True, null=True)

    raw_info                      = fields.JSONField()
    duration_seconds              = fields.IntegerField()
    view_count                    = fields.IntegerField()
    channel_id                    = fields.CharField(max_length=64)
    channel_title                 = fields.CharField()
    default_audio_language_code   = fields.CharField(max_length=10)
    default_caption_language_code = fields.CharField(max_length=10)
    all_thumbnails                = fields.JSONField()

    YT_ID_REGEX = re.compile(
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/'
        r'(?:watch\?.*?v=|embed/|v/)|youtu\.be/)'
        r'([0-9A-Za-z_-]{11})'
    )

    def __init__(self, *args, **kwargs):
        url_or_id = kwargs.pop("video_url_or_id", None)
        super().__init__(*args, **kwargs)
        if url_or_id:
            self.video_id = self.extract_video_id(url_or_id)

    @classmethod
    def extract_video_id(cls, url_or_id):
        m = cls.YT_ID_REGEX.search(url_or_id)
        if m:
            return m.group(1)
        if len(url_or_id) == 11 and re.fullmatch(r'[0-9A-Za-z_-]{11}', url_or_id):
            return url_or_id
        raise ValueError("Invalid YouTube URL or video ID")

    @property
    def api(self):
        if not getattr(self, "_api", None):
            if not self.video_id:
                raise ValueError("video_id must be set before accessing .api")
            self._api = YouTube(f"https://www.youtube.com/watch?v={self.video_id}")
        return self._api

    @property
    def link(self):
        return f"https://www.youtube.com/watch?v={self.video_id}"

    @djultra.models.admin_action()
    def fetch_and_store_video(self, save_transcripts=True):
        try:
            # 1) metadata
            self.title         = self.api.title
            self.description   = self.api.description
            self.thumbnail_url = self.api.thumbnail_url
            self.published_at  = self.api.publish_date or datetime.utcnow()

            # 2) vid_info + raw JSON
            info = getattr(self.api, "vid_info", {})
            self.raw_info = info

            vd   = info.get("videoDetails", {})
            caps = self.api.captions  # CaptionQuery

            length = vd.get("lengthSeconds")
            self.duration_seconds = int(length) if length and length.isdigit() else None

            vc = vd.get("viewCount")
            self.view_count = int(vc) if vc and vc.isdigit() else None

            self.channel_id    = vd.get("channelId")
            self.channel_title = vd.get("author")

            # default audio lang
            default_audio = None
            if caps:
                first = next(iter(caps), None)
                if first:
                    code = first.code
                    default_audio = code.replace("a.", "")
            self.default_audio_language_code = default_audio

            # default caption lang
            default_caption = None
            if caps:
                # choose first track as default caption
                default_caption = next(iter(caps)).code.replace("a.", "")
            self.default_caption_language_code = default_caption

            thumb = vd.get("thumbnail", {}).get("thumbnails")
            self.all_thumbnails = thumb if isinstance(thumb, list) else None

            self.status = self.Status.FETCHED
            self.save()

            if save_transcripts:
                self.fetch_all_transcripts()

        except Exception:
            self.status = self.Status.ERROR
            self.save()
            raise

    def fetch_all_transcripts(self, save=True):
        """
        Parse built-in captions from pytubefix rather than external API.
        """
        results = {}
        for caption in self.api.captions:
            raw_code      = caption.code               # e.g. "de" or "a.de"
            generated     = raw_code.startswith("a.")
            lang_code     = raw_code.replace("a.", "")
            xml           = caption.xml_captions       # timedtext XML
            tree          = ET.fromstring(xml)
            segments_list = []
            for node in tree.findall("text"):
                start = float(node.get("start", 0.0))
                dur   = float(node.get("dur",   0.0))
                text  = node.text or ""
                segments_list.append({"text": text, "start": start, "duration": dur})

            if save:
                obj, _ = YouTubeTranscript.objects.update_or_create(
                    video=self,
                    language_code=lang_code,
                    defaults={
                        "is_generated": generated,
                        "segments":     segments_list,
                    },
                )
                results[lang_code] = obj
            else:
                results[lang_code] = segments_list

        return results

    @property
    def transcript(self):
        """
        Return text in preferred audio lang (default_audio_language_code),
        falling back to the first available transcript.
        """
        preferred = self.default_audio_language_code
        for t in self.transcripts.all():
            if t.language_code == preferred:
                return t.text
        first = self.transcripts.first()
        return first.text if first else None

    def __str__(self):
        return self.title or self.video_id


class YouTubeTranscript(djultra.models.Base):
    video          = models.ForeignKey(
        YouTubeVideo,
        on_delete=models.CASCADE,
        related_name="transcripts",
    )
    language_code  = fields.CharField(max_length=2)
    is_generated   = models.BooleanField(default=True)
    segments       = fields.JSONField()
    text           = fields.TextField()

    class Meta:
        unique_together = ("video", "language_code")
        ordering        = ("video", "language_code")

    def save(self, *args, **kwargs):
        if self.segments:
            self.text = " ".join(snippet["text"] for snippet in self.segments)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.video.video_id} [{self.language_code}]"

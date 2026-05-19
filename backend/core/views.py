import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class GenericAPIThrottle(UserRateThrottle):
    rate = '2/minute'


def index(request):
    context = {
        'frontend_api_url': settings.FRONTEND_API_URL,
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'index.html', context)


class TokenLoginView2(APIView):
    permission_classes = []

    def get(self, request):
        return self.post(request)

    def post(self, request):
        token = request.data.get('token', '') if request.method == 'POST' else request.GET.get('token', '')
        logger.debug(f'Received token: {token}')
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, token=token)
        logger.debug('Auth user after authentication: ', user)

        if user:
            login(request, user)
            session_id = request.session.session_key
            return Response({
                "detail": "Login successful.",
                "session_key": settings.SESSION_COOKIE_NAME,
                "session_id": session_id,
            }, status=status.HTTP_200_OK)

        logger.warn('Authentication failed for token ', token)
        return Response({'detail': 'Invalid token or authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.post(request)

    def post(self, request):
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)


class Ping(APIView):
    permission_classes = []

    def get(self, request):
        logger.warn('Auth ping: ', request.user, request.user.is_authenticated)
        if request.user.is_authenticated:
            return Response({"detail": "Authenticated"}, status=status.HTTP_200_OK)
        return Response({"detail": "Not authenticated"}, status=status.HTTP_200_OK)

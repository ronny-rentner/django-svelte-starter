from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("api/ping/", views.Ping.as_view(), name="api_ping"),
    path("api/signout/", views.SignOutView.as_view(), name="api_sign_out"),
    path("api/contact/", views.ContactMessageView.as_view(), name="api_contact"),
]

# User login API — registered only when enabled, so login can be turned off entirely
# (this gates just the endpoints; no models are touched).
if settings.USER_LOGIN_ENABLED:
    urlpatterns += [
        path("api/token-login/", views.TokenLoginView.as_view(), name="api_token_login"),
        path("api/signin-request/", views.SigninRequestView.as_view(), name="api_signin_request"),
        path("api/person/", views.PersonView.as_view(), name="api_person_default"),
        path("api/person/<int:person_pk>", views.PersonView.as_view(), name="api_person"),
    ]

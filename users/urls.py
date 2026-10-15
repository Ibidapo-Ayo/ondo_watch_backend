from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CurrentUserProfileView, OfficialAccountCreateView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("officials/", OfficialAccountCreateView.as_view(), name="official_create"),
    path("profile/", CurrentUserProfileView.as_view(), name="user_profile"),
]
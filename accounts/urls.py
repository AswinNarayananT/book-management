from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView, CookieTokenRefreshView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('refresh-token/',CookieTokenRefreshView.as_view(),name='refresh-token'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
]

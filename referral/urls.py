from django.urls import path

from .views import (
    home_page,
    AuthCheckView,
    EditNameView,
    LogInView,
    LogOutView,
    ProfileView,
)

app_name = 'referral'

urlpatterns = [
    path('', home_page, name='home-page'),
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('profile/edit', EditNameView.as_view(), name='edit-name'),
    path('login/', LogInView.as_view(), name='login'),
    path('login/authcheck/', AuthCheckView.as_view(), name='auth-check'),
    path('logout', LogOutView.as_view(), name='logout'),
]

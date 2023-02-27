from django.urls import path
from auth import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        'login/',
        views.MyObtainTokenPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'login/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'signup/',
        views.SignupView.as_view(),
        name='auth_register'
    ),
    path(
        'change_password/',
        views.ChangePasswordView.as_view(),
        name='auth_change_password'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='auth_logout'
    ),
    path(
        'users/',
        views.UsersListView.as_view(),
        name='auth_users_list'
    ),
]

from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt import views
from authentication.views import *
from authentication import views as admin_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    re_path("auth/jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    re_path("auth/jwt/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path("auth/jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('admin-login/',AdminLogin.as_view(),name='admin-login'),
    path('auth/admin/login/', admin_views.admin_login, name='admin_login'),
]

"""accounts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import kakao_callback, kakao_login

urlpatterns = [
    path('admin/', admin.site.urls),
    # 로그인
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    #url(r'account/registration/confirm-email/(?P<key>.+)/$', confirm_email, name='confirm_email'),
    path('', include('django.contrib.auth.urls')),
    # 소셜 로그인
    path('account/login/kakao/', kakao_login, name='kakao_login'),
    path('account/login/kakao/callback/', kakao_callback, name='kakao_callback'),
]

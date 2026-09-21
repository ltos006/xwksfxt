"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including a URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.http import HttpResponse


def healthz(request):
    """Render 健康检查端点。"""
    return HttpResponse("ok")


urlpatterns = [
    path('healthz', healthz),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/admin/', include('admins.urls')),
    path('api/bindings/', include('bindings.urls')),
    # SPA 兜底：Vue Router 的前端路由直接访问时不 404
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

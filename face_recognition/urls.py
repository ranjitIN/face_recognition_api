"""
URL configuration for face_recognition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from face_recognition.services import face_services
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_schema_view
from rest_framework import permissions

schema_view = swagger_schema_view(
    openapi.Info(
        title="Face Recognition Api",
        default_version='v0.0.1'
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registerFace',face_services.register_Face),
    path('recogniseFace',face_services.recognise_face),
    path('uploadImage',face_services.upload_image),
    path('completeTraining',face_services.complete_training),
    path('swagger',schema_view.with_ui('swagger',cache_timeout = 0),name = 'swagger-schema')
    #  path('api/upload/',face_services.ImageUploadView.as_view(), name='image-upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
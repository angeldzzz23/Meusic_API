from django.urls import path,include
from api import views
#from rest_framework.routers import DefaultRouter



urlpatterns = [
    # when django matches the path, it calls hellAPIView
    path('image', views.UpdateImage.as_view(), name='image'),
    path('video', views.UpdateVideo.as_view(), name='video'),
    path('video/<str:id>', views.UpdateVideo.as_view(), name='video_by_id')

    #path('image/<str:id>', views.UpdateImage.as_view(), name='image_by_id')
]

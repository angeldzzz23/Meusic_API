
from django.urls import path,include
from . import views

from rest_framework import routers




router = routers.DefaultRouter()
router.register('awsimage', views.awsimageView)

urlpatterns = [

    # when django matches the path, it calls hellAPIView
    path('',include(router.urls))


]

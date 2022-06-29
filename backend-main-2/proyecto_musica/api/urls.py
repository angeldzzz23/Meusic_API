from django.urls import path,include

from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet) # we dont need to specify a base_name because in our view set we have a query set obejct
router.register('feed',views.UserProfileFeedViewSet)


urlpatterns = [
    # when django matches the path, it calls hellAPIView
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))


]

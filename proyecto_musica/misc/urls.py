
from django.urls import path
from misc import views

urlpatterns = [
    path('genres', views.GenreView.as_view(), name="genres"),
    path('skills', views.SkillView.as_view(), name="skills"),
    path('spotify', views.SpotifyPlatforms.as_view(), name='spotify'),
    path('spotify/<str:id>', views.SpotifyPlatforms.as_view(), name='spotify_by_id'),
    path('vimeo/<str:id>', views.VimeoPlatforms.as_view(), name='vimeo_by_id'),
    path('vimeo', views.VimeoPlatforms.as_view(), name='vimeo'),

]

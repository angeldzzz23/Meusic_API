
from django.urls import path
from misc import views

urlpatterns = [
    path('genres', views.GenreView.as_view(), name="genres"),
    path('genres/<str:id>', views.GenreView.as_view(), name="genres_by_id"),
    path('skills', views.SkillView.as_view(), name="skills"),
    path('skills/<str:id>', views.SkillView.as_view(), name='skills_by_id'),
    path('genders', views.GenderView.as_view(), name="genders"),
    path('genders/<str:id>', views.GenderView.as_view(), name="genders_by_id"),
    path('spotify', views.SpotifyPlatforms.as_view(), name='spotify'),
    path('spotify/<str:id>', views.SpotifyPlatforms.as_view(), name='spotify_by_id'),
    path('vimeo/<str:id>', views.VimeoPlatforms.as_view(), name='vimeo_by_id'),
    path('vimeo', views.VimeoPlatforms.as_view(), name='vimeo'),
    path('youtube', views.YoutubePlatforms.as_view(), name='youtube'),
    path('youtube/<str:id>', views.YoutubePlatforms.as_view(), name='youtube'),
    path('nationalities', views.NationalityView.as_view(), name="nationalities"),
    path('nationalities/<str:id>', views.NationalityView.as_view(), name='nationalities_by_id'),
    
]

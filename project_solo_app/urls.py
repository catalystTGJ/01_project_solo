from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('signout', views.signout),
    
    path('words', views.words),
    path('words/<str:action>', views.words),
    path('words/<str:action>/<int:word_id>', views.words),

    #background task base
    path('definition-harvest', views.definition_harvest),
    path('job-harvest', views.job_harvest),
    path('word-collect', views.word_collect),
    path('test-wait/<int:wait>', views.test_wait),
]
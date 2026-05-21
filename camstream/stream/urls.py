from django.urls import path
from . import views

urlpatterns=[
        path('', views.index, name='home'),
        path('video/',views.video_feed,name='video_feed'),
        path('status/',views.get_status,name='get_status'),
        path('start/',views.start_stream,name='start_stream'),
        path('stop/',views.stop_stream,name='stop_stream'),
        path('capture/', views.capture_image, name='capture'),
        path('record/', views.record_video, name='record'),
        path('switch_camera/', views.switch_camera, name='switch'),

]
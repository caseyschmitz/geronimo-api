from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root, name='api-root'),
    path('speedtest/', views.SpeedTestList.as_view(), name='speedtest-list'),
    path('speedtest/<int:pk>', views.SpeedTestDetail.as_view(), name='speedtest-detail'),
    path('speedtestclient/', views.SpeedTestClientList.as_view(), name='speedtestclient-list'),
    path('speedtestclient/<int:pk>', views.SpeedTestClientList.as_view(), name='speedtestclient-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
])
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root, name='api-root'),
    path('speedtest/', views.SpeedTestList.as_view(), name='speedtest-list'),
    path('speedtest/<int:pk>', views.SpeedTestDetail.as_view(), name='speedtest-detail'),
    path('testnode/', views.TestNodeList.as_view(), name='testnode-list'),
    path('testnode/<int:pk>', views.TestNodeList.as_view(), name='testnode-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
])
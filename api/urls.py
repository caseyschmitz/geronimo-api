from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root, name='api-root'),
    path('api-auth-token/', obtain_auth_token),
    path('speed-tests/', views.SpeedTestList.as_view(), name='speedtest-list'),
    path('speed-tests/<int:pk>', views.SpeedTestDetail.as_view(), name='speedtest-detail'),
    path('speed-test-clients/', views.SpeedTestClientList.as_view(), name='speedtestclient-list'),
    path('speed-test-clients/<int:pk>', views.SpeedTestClientDetail.as_view(), name='speedtestclient-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/register', views.UserCreate.as_view(), name='user-create'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
])

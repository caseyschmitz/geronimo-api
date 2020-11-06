from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('monitor/', views.SpeedTestList.as_view(), name='monitor-root'),
]
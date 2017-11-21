from django.conf.urls import url
from library import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]

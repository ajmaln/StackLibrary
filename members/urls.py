from django.conf.urls import url

from members import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.MemberCreateView.as_view(), name='create'),
    url(r'^view/(?P<pk>\d+)', views.MemberDetailView.as_view(), name='details'),
    url(r'^edit/(?P<pk>\d+)', views.MemberEditView.as_view(), name='edit')
]

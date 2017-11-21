from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.BookCreateView.as_view(), name='create'),
    url(r'^edit/(?P<pk>\d+)$', views.BookEditView.as_view(), name='edit'),
    url(r'^view/(?P<pk>\d+)$', views.BookDetailsView.as_view(), name='details'),
    url(r'^view/(?P<pk>\d+)/add_copies$', views.CopyCreateView.as_view(), name='copy_create'),
    url(r'^add_copies/$', views.CopyCreateView.as_view(), name='copy_create'),
    url(r'^delete/(?P<pk>\d+)$', views.BookDeleteView.as_view(), name='delete'),
    url(r'^issue/(?P<code>\w+)$', views.IssueView.as_view(), name='issue'),
    url(r'^return/(?P<code>\w+)$', views.ReturnView.as_view(), name='return'),
    url(r'^search/', views.SearchBooks.as_view(), name='search')
]

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^post/(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^add/', views.post_create, name='post_create'),
    url(r'^edit/(?P<post>[-\w]+)/$', views.post_create, name='post_edit'),
    url(r'^user/(?P<username>[-\w]+)/$', views.user_page, name='user_page'),
    url(r'^vote/$', views.post_vote, name='post_vote'),
    url(r'^$', views.index, name='index')
]
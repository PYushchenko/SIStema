from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^(?P<message_id>[^/]+)/', views.message, name='message')
]
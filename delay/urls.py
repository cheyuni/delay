from django.conf.urls import patterns, include, url
from apps import views

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^apps/logout$', views.logout),
                       url(r'^join$', views.join),
                       url(r'^apps/delay$', views.do_delay),
)

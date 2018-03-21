from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

# app_name = 'logbook'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_make_model_choose/$', views.edit_make_model_choose, name='edit_make_model_choose'),
    url(r'^edit_make_model_process/$', views.edit_make_model_process, name='edit_make_model_process'),
    url(r'^edit_make_model/([0-9]+)/$', views.edit_make_model, name='edit_make_model'),
    url(r'^edit_make_model_delete/([0-9]+)/$', views.edit_make_model_delete, name='edit_make_model_delete'),
    url(r'^edit_make_model_add/$', views.edit_make_model_add, name='edit_make_model_add'),
    url(r'^summaries/$', views.summaries, name='summaries'),
    url(r'^create/$', views.create, name='create'),
    url(r'^dates/([0-9]{4})/$', views.year, name='year'),
    url(r'^dates/([0-9]{4})/([0-9]+)/$', views.month, name='month'),
    url(r'^flights/([0-9]+)/$', views.flight, name='flight'),
    url(r'^dispatch/$', views.dispatch, name='dispatch'),
    url(r'^make_model_process/$', views.make_model_process, name='make_model_process'),
    url(r'^make_model/([0-9]+)/$', views.make_model, name='make_model'),
    url(r'^equipment_process/$', views.equipment_process, name='equipment_process'),
    url(r'^equipment/([0-9]+)/$', views.equipment, name='equipment'),
    url(r'^date_range_choose/$', views.date_range_choose, name = 'date_range_choose'),
    url(r'^date_range/([0-9]{2}\.[0-9]{2}\.[0-9]{4})/([0-9]{2}\.[0-9]{2}\.[0-9]{4})/$',
        views.date_range, name='date_range')
]

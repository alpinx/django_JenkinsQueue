from django.conf.urls import url
from example import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^dispqueue/$', views.dispqueue, name='dispqueue'),
    url(r'get_more_tables/$', views.get_more_tables, name='get_more_tables'),
    url(r'get_more_tables_All_Vm/$', views.get_more_tables, name='get_more_tables_All_Vm'),
    url(r'get_finished_builds/$', views.get_finished_builds, name='get_finished_builds'),
]

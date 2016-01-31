from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^home$', 'openshift.views.home', name='home'),
    url(r'^$', 'openshift.views.index', name='index'),
    url(r'^list/$', 'openshift.views.list', name='list'),
    url(r'^howto/$', 'openshift.views.howto', name='howto'),
    url(r'^turnoncc/$', 'openshift.views.turnoncc', name='turnoncc'),
    url(r'^about/$', 'openshift.views.about', name='about'),
    url(r'^whatisit/$', 'openshift.views.whatisit', name='whatisit'),
    url(r'^search.*', 'openshift.views.search', name='search'),
    url(r'^add.*', 'openshift.views.add', name='add'),
    url(r'^del.*', 'openshift.views.delete', name='delete'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

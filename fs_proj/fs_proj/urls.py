from django.conf.urls import patterns, include, url
from django.contrib import admin
from fs_renderer import views as fs_renderer_views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fs_proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', fs_renderer_views.Index.as_view(), name='index'),
    url(r'^html/(\w+)/(\w+)/(\w+)', csrf_exempt(fs_renderer_views.HTMLView.as_view())),
    url(r'^html/(\w+)/(\w+)', csrf_exempt(fs_renderer_views.HTMLView.as_view())),
    url(r'^html/(\w+)', csrf_exempt(fs_renderer_views.HTMLView.as_view())),
    url(r'^html/', csrf_exempt(fs_renderer_views.HTMLView.as_view())),
)

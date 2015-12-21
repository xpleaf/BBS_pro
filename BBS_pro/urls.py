from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS_pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include('app01.urls')),
    (r'^login/$',views.Login),
    (r'^logout/$',views.logout_view),
    (r'^home/$',views.Home_page),
    (r'^accounts/login/$',views.Login),
)

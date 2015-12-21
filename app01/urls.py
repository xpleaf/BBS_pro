from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    
    url(r'^$',views.index),
    (r'^category/(\d+)/$',views.index),
    (r'^detail/(\d+)/$',views.bbs_detial),
    (r'^sub_comment/$',views.sub_comment),
    (r'^bbs_pub/$',views.bbs_pub),
    (r'^bbs_sub/$',views.bbs_sub),
)

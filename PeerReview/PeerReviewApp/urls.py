from django.conf.urls import patterns, include, url
from django.conf import settings
from PeerReviewApp import views
from django.contrib import admin

#adminpatterns = patterns('',
#	url(r'^$', views.auth_admin, name='admin_home')
#)

admin.autodiscover()
urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	#url(r'^admin/$', include(adminpatterns)),
	url(r'^admin/', include(admin.site.urls)),	
	url(r'^terms/$', views.terms, name='terms'), # Eventually change this to point at 'terms of service' view
	url(r'^edit/(?P<mid>\d+)/$', views.edit_manuscript, name='edit_manuscript'),
	url(r'^submitmanuscript/(?P<mid>\d+)/$', views.submit_manuscript, name='submit_manuscript'),
	url(r'^deletemanuscript/(?P<mid>\d+)/$', views.delete_manuscript, name='delete_manuscript'),
	url(r'^about/$', views.about, name='about'),
    url(r'^help/$', views.help, name='help'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$', views.auth_login, name='login'),
	url(r'^account/$', views.account, name='account'),
	url(r'^logout/$', views.auth_logout, name='logout'),
	url(r'^remove/(?P<fid>\d+)/$', views.remove_associated_file, name='remove_associated_file'),
	url(r'^author/$', views.author_home, name='authorhome'),
	url(r'^review/$', views.reviewer_home, name='review'),
	url(r'^browse/(?P<current_page>\d+)/$',views.browse_manuscripts, name='browse'),
	url(r'^agreement/$', views.agreement, name='agreement'),
	url(r'^assignedmanuscripts/(?P<current_page>\d+)/$',views.assigned_manuscripts, name='assigned_manuscripts'),
	url(r'^uploadmanuscript/$', views.upload_manuscript, name='upload_manuscript'),
	url(r'^admin_login/$', views.admin_login, name='admin_login'),
	url(r'^admin_homepage/$', views.admin_homepage, name='admin_homepage'),
	url(r'^admin_browselist/$', views.admin_browselist, name='admin_browselist'),
	url(r'^admin_browselist/admin_ajax/$', views.admin_ajax, name='admin_ajax'),
	url(r'^admin_browselist/admin_submit_ajax/$', views.admin_submit_ajax, name='admin_submit_ajax'),
	url(r'^admin_browselist/admin_confirm_ajax/$', views.admin_confirm_ajax, name='admin_confirm_ajax'),
	#url(r'^manuscript_detail/$', views.manuscript_detail, name='manuscript_detail'),
	#url(r'^user_detail/$', views.user_detail, name='user_detail'),
	url(r'^manuscript_detail/(?P<pk>[0-9]+)/$', views.manuscript_detail, name='manuscript_detail'),
	url(r'^user_detail/(?P<pk>[0-9]+)/$', views.user_detail, name='user_detail'),
	url(r'^admin_setting/$', views.setting, name='admin_setting'),
	url(r'^admin_logout/$', views.admin_logout, name='admin_logout'),
	url(r'^admin_help/$', views.admin_help, name='admin_help'),
	# Media root for serving files when on a local dev server
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

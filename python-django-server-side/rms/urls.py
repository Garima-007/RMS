from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('rms.views',
    url(r'zoozo/$','zoozo'),
    url(r'^home/$', 'home'),
    url(r'^login/$','login'),
    url(r'^calorie_page/$','calorie_page'),
    url(r'^garima/$','garima'),
)
urlpatterns +=patterns('rms.GameOfDenomination.views',
    url(r'^god/add_host/','host_game'),
    url(r'^god/join_host/','join_host'),
    url(r'^god/start_game/','start_game'),
    url(r'^god/update_move/','update_move'),
    url(r'^god/get_move/','get_move'),
    url(r'^god/end_game/','end_game'),
)
urlpatterns +=patterns('rms.rms_models.views',
    url(r'^mobile_applications/verify_cred/','verify_cred'),
    url(r'^mobile_applications/add_user/','add_user'),
    url(r'^mobile_applications/add_restaurant/','add_restaurant'),
    url(r'^mobile_applications/load_menu/','load_menu'),
    url(r'^mobile_applications/create_suggestion_table/','create_suggestion_table'),
    url(r'^mobile_applications/transaction_complete/','transaction_complete'),
    url(r'^mobile_applications/update_user_ratings/','update_user_ratings')

)
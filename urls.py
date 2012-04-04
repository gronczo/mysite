from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


from adverts.feeds import *

sitemaps = { 'adverts': AdvertsMap }

feeds = {'adverts': LatestAdverts }

urlpatterns = patterns("",

    url(r"^$", 'adverts.views.show_adverts'),

    url(r'^new_advert/', 'adverts.views.new_advert'),
    url(r'^new_category/', 'adverts.views.new_category'),
    url(r'^new_subcategory/', 'adverts.views.new_subcategory'),

    url(r'^show_advert/(?P<advert_id>\d{1,4})$', 'adverts.views.show_advert'),
    url(r'^show_advert/', 'adverts.views.show_adverts'),
    url(r'^edit_advert/(?P<advert_id>\d{1,4})$', 'adverts.views.edit_advert'),
    url(r'^delete_advert/(?P<advert_id>\d{1,4})$', 'adverts.views.delete_advert'),

    url(r'^show_category/', 'adverts.views.show_category'),
    url(r'^show_subcategory/', 'adverts.views.show_subcategory'),

    url(r'^login_user/', 'adverts.views.login_user'),
    url(r'^logout_user/', 'adverts.views.logout_user'),
    url(r'^registration/', 'adverts.views.registration'),
    url(r'^user/', 'adverts.views.user'),

    url(r'^my_advert/', 'adverts.views.my_advert'),
    url(r'^search/', 'adverts.views.search'),

    url(r'^generate_pdf/(?P<advert_id>\d{1,4})$', 'adverts.views.generate_pdf'),

    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':feeds}),


    # django
    url(r"^$", direct_to_template, {"template": "homepage.html",}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )

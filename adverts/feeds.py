from django.contrib.sitemaps import *
from adverts.models import *
from django.contrib.syndication.feeds import *

class AdvertsMap(Sitemap):
    def items(self):
        return Advert.objects.all()
    #def lastmod(self, obj):
    #    return 'last'
    #def changefreq(self, obj):
    #    return 'monthly'


class LatestAdverts(Feed):
    title = 'Wiadomosc z ogloszenia.pl'
    link = 'http://127.0.0.1:8000'
    description = 'Najnowsze ogloszenia'
    def items(self):
        return Advert.objects.order_by('-id')[:10]
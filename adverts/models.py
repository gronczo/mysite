from django.db import models
from django.contrib.auth import models as auth_models


class Category(models.Model):
    title = models.CharField(max_length=255,verbose_name='tytul')
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.title#


class Subcategory(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class Advert(models.Model):
    user = models.ForeignKey(auth_models.User)
    subcategory = models.ForeignKey(Subcategory,verbose_name='kategoria')
    title = models.CharField(max_length=255,verbose_name='tytul')
    description = models.CharField(max_length=255,verbose_name='tresc')
    price = models.IntegerField(default=0,verbose_name='cena')
    city = models.CharField(max_length=255,verbose_name='miejscowosc')
    contact = models.CharField(max_length=255,verbose_name='kontakt')
    views = models.IntegerField(default=0)
    #def __str__(self):
    #    return self.title
    #def __unicode__(self):
    #    return self.title
    def get_absolute_url(self):
        return '/show_advert/' + str(self.id)

class Attachment(models.Model):
    user = models.ForeignKey(auth_models.User)
    advert = models.ForeignKey(Advert)
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    file = models.FileField(upload_to='attachmnets',verbose_name='zdjecie')

class Comment(models.Model):
    user = models.ForeignKey(auth_models.User)
    advert = models.ForeignKey(Advert)
    content = models.CharField(max_length=255)
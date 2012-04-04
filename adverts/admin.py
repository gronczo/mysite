from django.contrib import admin
from adverts.models import *

#class Advert(admin.ModelAdmin):
#    list_display = {'title', 'description'}

admin.site.register(Advert)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Attachment)
admin.site.register(Comment)
#admin.site.register(User)
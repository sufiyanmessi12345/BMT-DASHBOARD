

# Register your models here.
# bmtapp/admin.py

from django.contrib import admin
from .models import Section, SectionUser, OrderItem, Attachment

admin.site.register(Section)
admin.site.register(SectionUser)
admin.site.register(OrderItem)
admin.site.register(Attachment)
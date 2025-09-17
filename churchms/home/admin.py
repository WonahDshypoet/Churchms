from django.contrib import admin

# Register your models here.
from .models import Family, Member, Event, Registration, Donation, Communication, Devotional, CustomUser

admin.site.register(CustomUser)
admin.site.register(Family)
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Donation)
admin.site.register(Communication)
admin.site.register(Devotional)
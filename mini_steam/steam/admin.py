from django.contrib import admin
from steam.models import Game, Achivments, UserAchivment, Order
# Register your models here.

@admin.register(Game)
class SteamAdmin(admin.ModelAdmin):
    ...

@admin.register(Achivments)
class AchivmentsAdmin(admin.ModelAdmin):
    ...

@admin.register(UserAchivment)
class AchivmentsAdmin(admin.ModelAdmin):
    ...

@admin.register(Order)
class AchivmentsAdmin(admin.ModelAdmin):
    ...
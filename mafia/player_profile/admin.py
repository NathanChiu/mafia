from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PlayerProfile

# Short descriptor of player profile model
class PlayerProfileInline(admin.StackedInline):
    model = PlayerProfile
    
class PlayerProfileAdmin(UserAdmin):
    inlines = (PlayerProfileInline,)

admin.site.unregister(User)
admin.site.register(User, PlayerProfileAdmin)

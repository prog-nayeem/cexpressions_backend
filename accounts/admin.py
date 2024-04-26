from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'auth_provider', 'is_staff', 'is_active')
    list_display_links = ('id', 'email') 
    list_filter = ('auth_provider', 'is_staff', 'is_active')  
    search_fields = ('id', 'email', 'full_name')  
    search_help_text= "Search by ID, email or full name"



    

admin.site.register(User, UserAdmin)
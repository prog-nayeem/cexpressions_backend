from django.contrib import admin
from .models import AboutPage, GoalSettings, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization
from django.db import models
from tinymce.widgets import TinyMCE

class AboutPageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ('id', 'created_at')

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.make_active()
        
        obj.save()

        
class UnderstandingGoalPrioritizationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ("id", "created_at")



class SuccessfulGoalPlanningInstructionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ("id", "created_at")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.make_active()
        
        obj.save()

class SuggestionsForSuccessAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ("id", "created_at")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.make_active()
        
        obj.save()

class GoalSettingsAdmin(admin.ModelAdmin):
    list_display = ("id","user", "created_at")
    list_display_links = ("id", "user")
    search_fields = ("id", "user__email")
    search_help_text= "Search by ID or user email"
    list_filter=("goal_term", "priority_scale")
    


admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(UnderstandingGoalPrioritization , UnderstandingGoalPrioritizationAdmin)
admin.site.register(SuccessfulGoalPlanningInstruction , SuccessfulGoalPlanningInstructionAdmin)
admin.site.register(SuggestionsForSuccess , SuggestionsForSuccessAdmin)
admin.site.register(GoalSettings , GoalSettingsAdmin)


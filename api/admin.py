from django.contrib import admin
from .models import AboutPage, GoalSettings, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization, Progress, Link
from django.db import models
from tinymce.widgets import TinyMCE
from django import forms

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
    list_display = ("id", "title", "created_at")
    list_display_links = ("id", "title")



class SuccessfulGoalPlanningInstructionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ("id", "created_at", "is_active")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.make_active()
        
        obj.save()

class SuggestionsForSuccessAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    list_display = ("id", "created_at", "is_active")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            obj.make_active()
        
        obj.save()


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 0


class GoalSettingsAdmin(admin.ModelAdmin):
    list_display = ("id","goal_to_achieve", "user", "created_at")
    list_display_links = ("id", "goal_to_achieve", "user")
    search_fields = ("id", "user__email")
    search_help_text= "Search by ID or user email"
    list_filter=("goal_term", "priority_scale")
    inlines = [ProgressInline]


class ProgressAdmin(admin.ModelAdmin):
    list_display = ("id", "get_goal_to_achieve")

    def get_goal_to_achieve(self, obj):
        return obj.goal.goal_to_achieve

    get_goal_to_achieve.admin_order_field = 'goal__goal_to_achieve' 
    get_goal_to_achieve.short_description = 'Goal To Achieve'
    search_fields = ("id", "goal__goal_to_achieve")
    list_filter = ("status",)
    search_help_text= "Search by ID or Goal"


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url','platform', 'is_share_app')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'url')
    search_help_text= "Search by Name or URL"



admin.site.register(AboutPage, AboutPageAdmin)
admin.site.register(UnderstandingGoalPrioritization , UnderstandingGoalPrioritizationAdmin)
admin.site.register(SuccessfulGoalPlanningInstruction , SuccessfulGoalPlanningInstructionAdmin)
admin.site.register(SuggestionsForSuccess , SuggestionsForSuccessAdmin)
admin.site.register(GoalSettings , GoalSettingsAdmin)
admin.site.register(Progress, ProgressAdmin)



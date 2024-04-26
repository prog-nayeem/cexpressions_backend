from django.db import models
from tinymce import models as tinymce_models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class AboutPage(models.Model):
    about_text = tinymce_models.HTMLField(verbose_name="About Text")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Is Active')

    def make_active(self):
        AboutPage.objects.exclude(id=self.id).update(is_active=False)
        self.is_active = True
        self.save() 

    
class UnderstandingGoalPrioritization(models.Model):
    title = models.CharField(verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)


class SuccessfulGoalPlanningInstruction(models.Model):
    content = tinymce_models.HTMLField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Is Active')

    def make_active(self):
        SuccessfulGoalPlanningInstruction.objects.exclude(id=self.id).update(is_active=False)
        self.is_active = True
        self.save() 

class SuggestionsForSuccess(models.Model):
    content= tinymce_models.HTMLField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Is Active')

    def make_active(self):
        SuggestionsForSuccess.objects.exclude(id=self.id).update(is_active=False)
        self.is_active = True
        self.save() 


class GoalSettings(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Med', 'Med'),
        ('High', 'High'),
    ]

    TERM_CHOICES = [
        ('Short Term', 'Short Term'),
        ('Long Term', 'Long Term'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_to_achieve = models.CharField()
    purpose_of_goal = models.CharField()
    plan_to_implement = models.CharField()
    area_of_focus = models.CharField()
    target_completion_date = models.DateTimeField()
    priority_scale = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    goal_term = models.CharField(max_length=20, choices=TERM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)




from rest_framework import serializers
from django.utils import timezone
from accounts.models import User
from .models import AboutPage, GoalSettings, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization, Progress, Link

class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = ['id', 'about_text', 'created_at']


class UnderstandingGoalPrioritizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnderstandingGoalPrioritization
        fields = ['id', 'title', 'description', 'created_at']
        many=True

class SuccessfulGoalPlanningInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfulGoalPlanningInstruction
        fields = ['id', 'content', 'created_at']

class SuggestionsForSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionsForSuccess
        fields = ['id', 'content', 'created_at']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'progress_accomplishment', 'setbacks', 'what_will_do_next', 'status', 'goal_date']
    
    def validate_status(self, value):
        """
        Validate status based on choices.
        """
        if value not in dict(Progress.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid status. Choose from available options.")
        return value


class GoalSettingsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False, 
        default=serializers.CurrentUserDefault(),
    )
    
    progresses = ProgressSerializer(many=True, read_only=True)
     
    class Meta:
        model = GoalSettings
        fields = ['id', 'user', 'goal_to_achieve', 'purpose_of_goal', 'plan_to_implement', 'area_of_focus', 'target_completion_date', 'priority_scale', 'goal_term', 'progresses', 'created_at']
    
    def validate_target_completion_date(self, value):
        """
        Validate that target_completion_date is not in the past.
        """
        if value.date() < timezone.now().date():
            raise serializers.ValidationError("Target completion date cannot be in the past.")
        return value



    def validate(self, data):
        is_partial_update = getattr(self, 'partial', False)
        errors = {}

        # Validate priority_scale field only if it's not a partial update or if it's being updated
        if not is_partial_update or 'priority_scale' in data:
            priority_scale = data.get('priority_scale')
            if priority_scale not in dict(GoalSettings.PRIORITY_CHOICES).keys():
                errors['priority_scale'] = 'Invalid priority scale. Choose from available options.'

        # Validate goal_term field only if it's not a partial update or if it's being updated
        if not is_partial_update or 'goal_term' in data:
            goal_term = data.get('goal_term')
            if goal_term not in dict(GoalSettings.TERM_CHOICES).keys():
                errors['goal_term'] = 'Invalid goal term. Choose from available options.'

        if errors:
            raise serializers.ValidationError(errors)

        return data


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'name', 'url','platform', 'is_share_app', 'share_app_message']
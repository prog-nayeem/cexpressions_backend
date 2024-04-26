from rest_framework import serializers

from accounts.models import User
from .models import AboutPage, GoalSettings, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization

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


class GoalSettingsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Assuming User is your user model
        required=False,  # Make the user field not required
        default=serializers.CurrentUserDefault(),  # Automatically set the current user
    )
     
    class Meta:
        model = GoalSettings
        fields = ['id', 'user', 'goal_to_achieve', 'purpose_of_goal', 'plan_to_implement', 'area_of_focus', 'target_completion_date', 'priority_scale', 'goal_term']

    def validate(self, data):
        errors = {}

        # Validate priority_scale field
        priority_scale = data.get('priority_scale')
        if priority_scale not in dict(GoalSettings.PRIORITY_CHOICES).keys():
            errors['priority_scale'] = 'Invalid priority scale. Choose from available options.'

        # Validate goal_term field
        goal_term = data.get('goal_term')
        if goal_term not in dict(GoalSettings.TERM_CHOICES).keys():
            errors['goal_term'] = 'Invalid goal term. Choose from available options.'

        if errors:
            raise serializers.ValidationError(errors)

        return data

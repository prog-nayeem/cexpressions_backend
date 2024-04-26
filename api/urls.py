from django.urls import path
from .views import AboutPageView, GoalSettingsCreateView, SuccessfulGoalPlanningInstructionView, SuggestionsForSuccessView, UnderstandingGoalPrioritizationView

urlpatterns = [
    path('about/', AboutPageView.as_view({'get': 'retrieve'}), name='about'),
    path('understanding-goal-prioritization/', UnderstandingGoalPrioritizationView.as_view({'get': 'list'}), name='understanding_goal_prioritization'),
    path('successful-goal-planning-instruction/', SuccessfulGoalPlanningInstructionView.as_view({'get': 'retrieve'}), name='successful_goal_planning_instruction'),
    path('suggestions-for-success/', SuggestionsForSuccessView.as_view({'get': 'retrieve'}), name='suggestions_for_success'),
    path('goal-settings/create/', GoalSettingsCreateView.as_view(), name='goal_settings_create'),

]

 
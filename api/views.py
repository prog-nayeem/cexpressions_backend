from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.models import User
from .models import AboutPage, GoalSettings, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization
from .serializers import AboutPageSerializer, GoalSettingsSerializer, SuccessfulGoalPlanningInstructionSerializer, SuggestionsForSuccessSerializer, UnderstandingGoalPrioritizationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator



class AboutPageView(viewsets.ViewSet):
    @method_decorator(ratelimit(key='user_or_ip', rate='100/m', method='GET'))
    def retrieve(self, request):
        try:
            about_page = AboutPage.objects.get(is_active=True)

            serializer = AboutPageSerializer(about_page)

            return Response({'success': True, 'data': serializer.data})
        except AboutPage.DoesNotExist:
            return Response({'success': False, 'error': 'No active about content found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class UnderstandingGoalPrioritizationView(viewsets.ViewSet):
    @method_decorator(ratelimit(key='user_or_ip', rate='100/m', method='GET'))
    def list(self, request):
        try:
            queryset = UnderstandingGoalPrioritization.objects.all()

            serializer = UnderstandingGoalPrioritizationSerializer(queryset, many=True)

            return Response({'success': True, 'data': serializer.data})
        except AboutPage.DoesNotExist:
            return Response({'success': False, 'error': 'Not found any content.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

class SuccessfulGoalPlanningInstructionView(viewsets.ViewSet):
    @method_decorator(ratelimit(key='user_or_ip', rate='100/m', method='GET'))
    def retrieve(self, request):
        try:
            queryset = SuccessfulGoalPlanningInstruction.objects.get(is_active=True)

            serializer = SuccessfulGoalPlanningInstructionSerializer(queryset)

            return Response({'success': True, 'data': serializer.data})
        except AboutPage.DoesNotExist:
            return Response({'success': False, 'error': 'Not found any content.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class SuggestionsForSuccessView(viewsets.ViewSet):
    @method_decorator(ratelimit(key='user_or_ip', rate='100/m', method='GET'))
    def retrieve(self, request):
        try:
            queryset = SuggestionsForSuccess.objects.get(is_active=True)

            serializer = SuggestionsForSuccessSerializer(queryset)

            return Response({'success': True, 'data': serializer.data})
        except AboutPage.DoesNotExist:
            return Response({'success': False, 'error': 'Not found any content.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user 

class GoalSettingsView(APIView):
    serializer_class = GoalSettingsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except AuthenticationFailed:
            return Response({'success': False, 'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_user_goals(self, user, status=None):
        goals = GoalSettings.objects.filter(user=user)
        if status:
            goals = goals.filter(status=status)
        serializer = GoalSettingsSerializer(goals, many=True)
        return serializer.data
    
    @method_decorator(ratelimit(key='user_or_ip', rate='100/m', method='GET'))
    def get(self, request):
        try:
            user = request.user
            if not isinstance(user, User): 
                raise NotFound("User not found.")
            
            status = request.query_params.get('status')
            user_goals = self.get_user_goals(user, status=status)
            return Response({'success': True, 'data': user_goals})
        except NotFound as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(ratelimit(key='user_or_ip', rate='50/m', method='POST'))
    def post(self, request):
        serializer = GoalSettingsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Goal Settings created successfully'}, status=status.HTTP_201_CREATED)
        else:
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            return Response({'success': False, 'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(ratelimit(key='user_or_ip', rate='70/m', method='PATCH')) 
    def patch(self, request, pk, format=None):
        try:
            obj = GoalSettings.objects.get(id=pk)
        except GoalSettings.DoesNotExist:
            return Response({'success': False, 'error': 'Goal settings not found.'}, status=status.HTTP_404_NOT_FOUND)

        if obj.user != request.user:
            return Response({'success': False, 'error': 'You are not allowed to update this goal.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GoalSettingsSerializer(obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Goal Settings updated successfully'}, status=status.HTTP_200_OK)
        else:
            formatted_errors = {}
            for field, errors in serializer.errors.items():
                formatted_errors[field] = errors[0]
            return Response({'success': False, 'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(ratelimit(key='user_or_ip', rate='30/m', method='DELETE'))  
    def delete(self, request, pk, format=None):
        goal = get_object_or_404(GoalSettings, pk=pk)
        
        if goal.user != request.user:
            return Response({'success': False, 'error': 'You are not allowed to delete this goal.'}, status=status.HTTP_403_FORBIDDEN)

        goal.delete()
        return Response({'success': True, 'message': 'Goal deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
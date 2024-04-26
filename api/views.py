from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AboutPage, SuccessfulGoalPlanningInstruction, SuggestionsForSuccess, UnderstandingGoalPrioritization
from .serializers import AboutPageSerializer, GoalSettingsSerializer, SuccessfulGoalPlanningInstructionSerializer, SuggestionsForSuccessSerializer, UnderstandingGoalPrioritizationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed



class AboutPageView(viewsets.ViewSet):
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
    def retrieve(self, request):
        try:
            queryset = SuggestionsForSuccess.objects.get(is_active=True)

            serializer = SuggestionsForSuccessSerializer(queryset)

            return Response({'success': True, 'data': serializer.data})
        except AboutPage.DoesNotExist:
            return Response({'success': False, 'error': 'Not found any content.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

class GoalSettingsCreateView(APIView):
    serializer_class = GoalSettingsSerializer
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except AuthenticationFailed:
            return Response({'success': False, 'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

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
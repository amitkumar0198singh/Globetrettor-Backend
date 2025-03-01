import random

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from game.services import destination_service
from game.serializers.destination_serializer import DestinationSerializer


class DestinationView(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        destination = destination_service.get_destination(pk)
        serializer = DestinationSerializer(destination)
        return Response({'status': True, 'message': "Destination found", 
                        'destination': serializer.data}, status=status.HTTP_200_OK)

    def list(self, request):
        destinations = destination_service.get_all_destinations()
        serializer = DestinationSerializer(destinations, many=True)
        return Response({'status': True, 'message': "Destinations found", 
                        'destinations': serializer.data}, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['post'], url_path='create', url_name='create', permission_classes=[IsAuthenticated])
    def create_destination(self, request):
        serializer = DestinationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['created_by'] = data['updated_by'] = request.user
        response = destination_service.create_destination(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='bulk-create', url_name='bulk-create', permission_classes=[IsAuthenticated])
    def bulk_create(self, request):
        serializer = DestinationSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data_list = serializer.validated_data
        response = destination_service.bulk_create_destinations(data_list, request.user)
        return Response(response, status=status.HTTP_201_CREATED)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from AirTrafficApp.models import Items
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getData(request):
    items = Items.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addItem(request):
    many = isinstance(request.data, list)
    serializer = ItemSerializer(data=request.data, many=many, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


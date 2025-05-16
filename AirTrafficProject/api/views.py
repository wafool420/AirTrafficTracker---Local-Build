from rest_framework.response import Response
from rest_framework.decorators import api_view
from AirTrafficApp.models import Items
from .serializers import ItemSerializer


@api_view(['GET'])
def getData(request):
    items = Items.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
def addItem(request):
    many = isinstance(request.data, list)
    serializer = ItemSerializer(data=request.data, many=many)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


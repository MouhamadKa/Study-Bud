from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    # A view to show all the routes in our API
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    # A view to show all the rooms
    rooms = Room.objects.all()
    searializer = RoomSerializer(rooms, many=True)
    return Response(searializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    # A view to show a specific room
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament
from .serializers import TournamentSerializer


@api_view(['GET', 'POST'])
def tournament_list(request):
    """
    List all tournaments or create a new tournament.
    """
    if request.method == 'GET':
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tournament_detail(request, pk):
    """
    Retrieve, update or delete a tournament instance.
    """
    try:
        tournament = Tournament.objects.get(pk=pk)
    except Tournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TournamentSerializer(tournament)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TournamentSerializer(tournament, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

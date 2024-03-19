from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament, Match, Team, TournamentResult, Player
from .serializers import TournamentSerializer, MatchSerializer, TeamSerializer, TournamentResultSerializer, PlayerSerializer
from .utils import create_match, get_match, update_match, delete_match, generate_knockout_stages
import stripe
from django.conf import settings
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
def create_checkout_session(request):
    try:
        logger.info("Creating Stripe checkout session")
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1Ow4wuHJ4pSO9vPN2wwPQaLg',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.SITE_URL +
            '/?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.SITE_URL + '/?canceled=true',
        )
        logger.info(f"Checkout session created: {checkout_session.url}")
        # return redirect(checkout_session.url)
        return Response({'url': checkout_session.url})
    except:
        logger.error(f"Error creating checkout session: {e}")
        return Response(
            {'error': 'Something went wrong when creating the checkout session'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
def player_list(request):
    """
    List all players or create a new player.
    """
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def player_detail(request, pk):
    """
    Retrieve, update or delete a player instance.
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def tournament_list(request):
    """
    List all tournaments or create a new tournament.
    """
    if request.method == 'GET':
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            tournament = serializer.save()

            # Automatically generate knockout stage matches
            try:
                generate_knockout_stages(tournament.id)
            except ValueError as e:
                tournament.delete()  # Rollback the creation of the tournament
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET', 'POST'])
def match_list(request):
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        match = create_match(request.data)
        serializer = MatchSerializer(match)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def match_detail(request, pk):
    if request.method == 'GET':
        match = get_match(pk)
        if match:
            serializer = MatchSerializer(match)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        match = update_match(pk, request.data)
        if match:
            serializer = MatchSerializer(match)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if delete_match(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def team_list(request):
    """
    List all teams or create a new team.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    """
    Retrieve, update or delete a team instance.
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def tournament_result_list(request):
    if request.method == 'GET':
        results = TournamentResult.objects.all()
        serializer = TournamentResultSerializer(results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TournamentResultSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new TournamentResult instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tournament_result_detail(request, pk):
    try:
        result = TournamentResult.objects.get(pk=pk)
    except TournamentResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TournamentResultSerializer(result)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TournamentResultSerializer(result, data=request.data)
        if serializer.is_valid():
            # Update the TournamentResult instance
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the TournamentResult instance
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

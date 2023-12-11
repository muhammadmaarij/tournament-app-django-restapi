from django.db import transaction
from .models import Match, Team, Tournament


def generate_knockout_stages(tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except Tournament.DoesNotExist:
        raise ValueError("Tournament does not exist")

    num_slots = tournament.slots
    if num_slots not in [2, 4, 8, 16]:
        raise ValueError("Number of slots must be 2, 4, 8, or 16")

    rounds = num_slots // 2  # Number of matches in the first round
    match_list = []

    with transaction.atomic():
        for i in range(rounds):
            match = Match.objects.create(
                name=f"Round {i + 1} Match {i + 1}",
                team1=None,  # Empty slots for teams
                team2=None,
                tournament=tournament,
                time=None 
            )
            match_list.append(match)

    return match_list


# Function to create a new match
def create_match(data):
    match = Match.objects.create(**data)
    return match

# Function to retrieve a specific match


def get_match(match_id):
    try:
        return Match.objects.get(pk=match_id)
    except Match.DoesNotExist:
        return None

# Function to update an existing match


def update_match(match_id, update_data):
    match = get_match(match_id)
    if match:
        for field, value in update_data.items():
            setattr(match, field, value)
        match.save()
        return match
    return None

# Function to delete a match


def delete_match(match_id):
    match = get_match(match_id)
    if match:
        match.delete()
        return True
    return False

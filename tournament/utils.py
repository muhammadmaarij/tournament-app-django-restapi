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
                time=None  # Set time as None for now
            )
            match_list.append(match)

    return match_list


def create_match(data):
    match = Match.objects.create(**data)
    return match


def get_match(match_id):
    try:
        return Match.objects.get(pk=match_id)
    except Match.DoesNotExist:
        return None


def update_match(match_id, update_data):
    match = get_match(match_id)
    if match:
        for field, value in update_data.items():
            if field in ['tournament', 'team1', 'team2'] and isinstance(value, int):
                # Handle ForeignKey fields
                try:
                    related_instance = {'tournament': Tournament, 'team1': Team, 'team2': Team}[
                        field].objects.get(pk=value)
                    setattr(match, field, related_instance)
                except (Tournament.DoesNotExist, Team.DoesNotExist):
                    continue  # or handle the error as needed
            else:
                setattr(match, field, value)
        match.save()
        return match
    return None


def delete_match(match_id):
    match = get_match(match_id)
    if match:
        match.delete()
        return True
    return False

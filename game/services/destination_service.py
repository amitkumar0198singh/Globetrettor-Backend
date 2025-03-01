import random

from game.models.destination import Destination
from game.utils import custom_exceptions, utility



def get_destination(id):
    try:
        return Destination.objects.get(id=id)
    except Destination.DoesNotExist:
        raise custom_exceptions.DataNotFoundException('Destination not found')

def get_all_destinations():
    return Destination.objects.all()

def get_destination_choices(id):
    destination = get_destination(id)
    choices = list(Destination.objects.exclude(id=id).values_list('city', flat=True))
    random.shuffle(choices)
    choices = choices[:3] + [destination.city]
    random.shuffle(choices)
    return choices


def create_destination(data):
    clues = data.get('clues')
    fun_fact = data.get('fun_fact')
    trivia = data.get('trivia')
    Destination.objects.create(
        city=data.get('city'),
        country=data.get('country'),
        clues=utility.list_to_paragraph(clues),
        fun_fact=utility.list_to_paragraph(fun_fact),
        trivia=utility.list_to_paragraph(trivia),
        created_by=data.get('created_by'),
        updated_by=data.get('updated_by'),
    )
    return {'status': True, 'message': "Destination created successfully"}


def bulk_create_destinations(data_list, player):
    destinations = []
    for data in data_list:
        destination = Destination(city=data.get('city'), country=data.get('country'),
            clues=utility.list_to_paragraph(data.get('clues')),
            fun_fact=utility.list_to_paragraph(data.get('fun_fact')),
            trivia=utility.list_to_paragraph(data.get('trivia')),
            created_by=player, updated_by=player,  
        )
        destinations.append(destination)
    Destination.objects.bulk_create(destinations, ignore_conflicts=True)
    return {'status': True, 'message': "Destinations created successfully",
                                                'total_destinations': len(data_list)}
from rest_framework import serializers

from game.models.destination import Destination


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['city', 'country', 'clues', 'fun_fact', 'trivia',]
        extra_kwargs = {
            'city': {'required': True}, 'country': {'required': True}, 'clues': {'required': True},
            'fun_fact': {'required': True}, 'trivia': {'required': True},
        }

    def to_representation(self, destination):
        destination_data = super().to_representation(destination)

        for field in ['clues', 'fun_fact', 'trivia']:
            if destination_data.get(field):
                # Split text into a list & remove empty strings
                destination_data[field] = [line.strip() for line in destination_data[field].split('\n') if line.strip()]

        return destination_data
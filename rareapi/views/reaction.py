"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

from rareapi.models import Reaction

class ReactionView(ViewSet):
    """ Reaction view """

    def list(self, request):
        """ Handle GET requests to get all reactions """
        reactions = Reaction.objects.all()
        serializers = ReactionSerializer(reactions, many=True)
        return Response(serializers.data)

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions """
    class Meta:
        model = Reaction
        fields = ('id', 'label')
        depth = 1

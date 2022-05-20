"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

from rareapi.models import PostReaction

class PostReactionView(ViewSet):
    """ PostReaction view """

    def list(self, request):
        """ Handle GET requests to get all postreactions """
        postreactions = PostReaction.objects.all()
        serializers = PostReactionSerializer(postreactions, many=True)
        return Response(serializers.data)

class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for postreactions """
    class Meta:
        model = PostReaction
        fields = ('id', 'post', 'reaction', 'user')
        depth = 1

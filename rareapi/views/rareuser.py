"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import action

from rareapi.models import RareUser


class RareUserView(ViewSet):
    """ RareUser view """
    def retrieve(self, request, pk):
        """ single rareuser """
        try:
            rareuser = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rareuser)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all rareusers

        Returns:
            Response -- JSON serialized list of rareusers
        """
        rareusers = RareUser.objects.all()
        for rareuser in rareusers:
            user = User.objects.get(pk=rareuser.user_id)
            rareuser.user = user
        serializer = RareUserSerializer(rareusers, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def reactivate(self, request, pk):
        """Put request for a user to be reactivated"""

        rareuser = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(rareuser, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User Reactivated'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def deactivate(self, request, pk):
        """Put request for a user to be deactivated"""

        rareuser = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(rareuser, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User Deactivated'}, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUser """
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'active', 'user', 'created_on')
        depth = 1

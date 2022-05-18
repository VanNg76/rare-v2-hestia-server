"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rareapi.models import RareUser, Post


class RareUserView(ViewSet):
    """ RareUser view """
    def retrieve(self, request, pk):
        """ single rareuser """
        try:
            rareuser = RareUser.objects.get(pk=pk)
            posts_by_user = Post.objects.filter(user_id=pk)
            serializer = RareUserSerializer(rareuser)
            
            # create a copy of serializer.data
            serializer_data = serializer.data
            
            # add a property (w/o modify class, or add a custom property to class)
            serializer_data["postCount"] = len(posts_by_user)
            
            return Response(serializer_data)
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

    
class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUser """
    
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'user')
        depth = 1

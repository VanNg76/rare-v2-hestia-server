"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.db.models import Q  # use for search query

from rareapi.models import RareUser, Post
from .post import PostSerializer


class RareUserView(ViewSet):
    """ RareUser view """

    def retrieve(self, request, pk):
        """ single rareuser """
        try:
            if pk == '0':
                rareuser = RareUser.objects.get(user_id=request.auth.user)
            else:
                rareuser = RareUser.objects.get(pk=pk)
            # return postCount to client
            posts_by_user = Post.objects.filter(user_id=pk)
            serializer = RareUserSerializer(rareuser)

            # create a copy of serializer.data
            serializer_data = serializer.data

            # add a property (w/o modify class, or add a custom property to class)
            serializer_data["postCount"] = len(posts_by_user)

            return Response(serializer_data)

            # return filtered posts to client
            # serializer = RareUserEventSerializer(rareuser)
            # return Response(serializer.data)

        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all rareusers

        Returns:
            Response -- JSON serialized list of rareusers
        """
        rareusers = RareUser.objects.all()
        users = User.objects.all()
        adminCount = users.filter(is_staff=True)
        user_id = request.query_params.get('user_id', None)
        for rareuser in rareusers:
            user = User.objects.get(pk=rareuser.user_id)
            rareuser.user = user
            rareuser.admin_count = len(adminCount)
            if rareuser.user.is_staff == True:
                rareuser.is_admin = True
            else:
                rareuser.is_admin = False
        serializer = RareUserSerializer(rareusers, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def reactivate(self, request, pk):
        """Put request for a user to be reactivated"""

        rareuser = RareUser.objects.get(pk=pk)
        rareuser.active = True
        rareuser.save()
        return Response({'message': 'User Reactivated'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def deactivate(self, request, pk):
        """Put request for a user to be deactivated"""

        rareuser = RareUser.objects.get(pk=pk)
        if rareuser.admin_approval == 0:
            rareuser.admin_approval = 1
            rareuser.save()
        else:
            rareuser.admin_approval = 0
            rareuser.active = False
            rareuser.save()
        return Response({'message': 'User Deactivated'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def demote(self, request, pk):
        """Put request for a user to be demoted"""

        rareuser = RareUser.objects.get(pk=pk)
        if rareuser.admin_approval == 0:
            rareuser.admin_approval = 1
            rareuser.save()
        else:
            user = User.objects.get(pk=rareuser.user_id)
            rareuser.admin_approval = 0
            user.is_staff = False
            rareuser.save()
            user.save()
        return Response({'message': 'User Demoted'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def promote(self, request, pk):
        """Put request for a user to be demoted"""

        rareuser = RareUser.objects.get(pk=pk)
        user = User.objects.get(pk=rareuser.user_id)
        user.is_staff = True
        user.save()
        return Response({'message': 'User Promoted'}, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUser """
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'active', 'user',
                  'created_on', 'is_admin', 'admin_count', 'admin_approval')
        depth = 1


class RareUserEventSerializer(serializers.ModelSerializer):
    """add filtered posts into single rareuser"""
    posts = serializers.SerializerMethodField()

    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'user', 'posts')
        depth = 1

    def get_posts(self, pk):
        posts_by_user = Post.objects.filter(user_id=pk)
        return PostSerializer(posts_by_user, many=True).data

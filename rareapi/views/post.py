from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rareapi.models.rareuser import RareUser

class PostView(ViewSet):
    """Rare posts view"""

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        try:
            posts = Post.objects.all()
            user = request.query_params.get('user_id', None)
            if user is not None:
                users = User.objects.get(auth_token=user)
                rare_user = RareUser.objects.get(user=users)
                posts = posts.filter(user=rare_user)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """

    class Meta:
        model = Post
        fields = ('id', 'title', 'publication_date', 'image_url', 'content', 'approved', 'category', 'user')
        depth = 2
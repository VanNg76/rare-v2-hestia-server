from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment
from rareapi.models.rareuser import RareUser

class CommentView(ViewSet):
    """Rare posts view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        try:
            comments = Comment.objects.order_by('-created_on')
            for comment in comments:
                if comment.author_id == request.auth.user.id:
                    comment.is_author = True
                else:
                    comment.is_author = False

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized comment instance
        """
        rareuser = RareUser.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=rareuser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    """
    class Meta:
        model = Comment
        fields = ('id', 'created_on', 'content', 'author', 'post', 'is_author')
        depth = 2


class CreateCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    """
    class Meta:
        model = Comment
        fields = ('id', 'created_on', 'content', 'post')
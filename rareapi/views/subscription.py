"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from rareapi.models import Subscription

class SubscriptionView(ViewSet):
    """ Subscription view """

#     def retrieve(self, request, pk):
#         """ single subscription """
#         try:
#             subscription = Subscription.objects.get(pk=pk)
#             serializer = SubscriptionSerializer(subscription)
#             return Response(serializer.data)
#         except Subscription.DoesNotExist as ex:
#             return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """ subscription list """
        
        subscriptions = Subscription.objects.all()
        
        # get query of follower id
        param_id = self.request.query_params.get('follower', None)
        
        # filter subs to get all subs have follower_id
        if param_id is not None:
            subscriptions = subscriptions.filter(follower_id=param_id)
        
        serializers = SubscriptionSerializer(subscriptions, many=True)
        
        return Response(serializers.data)

    # def update(self, request, pk):
    #     """Handle PUT requests for a subscription"""

    #     subscription = Subscription.objects.get(pk=pk)
    #     serializer = CreateSubscriptionSerializer(subscription, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


    # def create(self, request):
    #     """ POST a subscription """

    #     serializer = CreateSubscriptionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def destroy(self, request, pk):
    #     subscription = Subscription.objects.get(pk=pk)
    #     subscription.delete()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscription/subscriptions """

    class Meta:
        model = Subscription
        fields = ('id', 'author', 'follower')
        depth = 1

# class CreateSubscriptionSerializer(serializers.ModelSerializer):
#     """JSON serializer for create/update subscription """

#     class Meta:
#         model = Subscription
#         fields = ('id', 'author', 'follower')
#         depth = 1

# class SubscriptionPostSerializer(serializers.ModelSerializer):
#     """add filtered posts into single subscription"""
#     posts = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Subscription
#         fields = ('id', 'follower', 'author', 'posts')
#         depth = 1

#     def get_posts(self, param_id):
#         posts_by_follower = Post.objects.filter(user_id=param_id)
#         return PostSerializer(posts_by_follower, many=True).data      
from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Client, Stock, FriendList, StockList


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.Field(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')


class ClientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Client
        fields = ('name', 'password')


class StockSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Stock
        fields = ('name', 'price', 'updated')



class FriendListSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = FriendList
        fields = ('owner', 'friends')

class StockListSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = StockList
        fields = ('sl_owner', 'stocks')
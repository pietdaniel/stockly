from snippets.models import Snippet, Client, Stock, FriendList, StockList
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer, UserSerializer, ClientSerializer, StockSerializer, FriendListSerializer, StockListSerializer
from rest_framework import generics
from rest_framework import permissions 
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from snippets.permissions import IsOwnerOrReadOnly

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import viewsets
from rest_framework.decorators import link
from rest_framework import status

@api_view(['GET', 'POST'])
def create_user(request):
    print request.POST
    print request.POST['username']
    print request.POST['password']
    return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @link(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def pre_save(self, obj):
        obj.owner = self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class Client(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class Stock(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

class FriendList(viewsets.ModelViewSet):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer
    permission_classes = [IsOwnerOrReadOnly]

class StockList(viewsets.ModelViewSet):
    queryset = StockList.objects.all()
    serializer_class = StockListSerializer
    permission_classes = [IsOwnerOrReadOnly]
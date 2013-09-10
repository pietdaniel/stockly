from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from rest_framework.routers import DefaultRouter
from snippets.views import SnippetViewSet, UserViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'clients', views.Client)
router.register(r'stocks', views.Stock)
router.register(r'friendlists', views.FriendList)
router.register(r'stocklists', views.StockList)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('snippets.views',
	url (r'^create_user/$', 'create_user'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
from django.urls import path, include
from blogging.views import stub_view, list_view, detail_view, logout
from django.conf import settings
from . import views
# from django.contrib.auth.views import logout
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    path('', list_view, name="blog_index"),
    path('posts/<int:post_id>/', detail_view, name="blog_detail"),
    # below via google
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='logout'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

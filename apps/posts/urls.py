from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'apps.posts'

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_individual'),
    path('crear/', PostCreateView.as_view(), name='post_crear'),
    path('editar/<int:pk>/', PostUpdateView.as_view(), name='post_editar'),
    path('eliminar/<int:pk>/', PostDeleteView.as_view(), name='post_eliminar'),
]
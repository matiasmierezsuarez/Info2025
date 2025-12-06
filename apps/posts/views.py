from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   # <-- añadido UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Categoria, Comentario
from .forms import PostForm, ComentarioForm


# 1. Listado de Posts (Con filtros)
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5  # Opcional: paginación

    def get_queryset(self):
        queryset = Post.objects.filter(activo=True)
        
        # Filtros
        categoria_id = self.request.GET.get('categoria')
        orden = self.request.GET.get('orden')
        
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
            
        if orden == 'antiguo':
            queryset = queryset.order_by('fecha') # Ascendente
        else:
            queryset = queryset.order_by('-fecha') # Descendente (default)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

# 2. Detalle del Post (Y creación de comentarios)
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = self.object.comentarios.all().order_by('-fecha')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.post = self.object
            comentario.save()
            return redirect('apps.posts:post_individual', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))
    
    def abm_comentario(self, request):
        comentario = self.get_object()
        return comentario.usuario == self.request.user

# 3. Vistas CRUD (Solo usuarios logueados)
class PostCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('apps.posts:posts')


    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('apps.posts:posts')

# Protegemos actualización para que solo el autor pueda editar
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('apps.posts:posts')

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user



# Protegemos eliminación para que solo el autor pueda borrar
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:posts')

    def test_func(self):
        post = self.get_object()
        return post.autor == self.request.user

class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_editar.html' # Crea este template sencillo

    def get_success_url(self):
        # Redirige de nuevo al detalle del post al que pertenece el comentario
        return reverse_lazy('apps.posts:post_individual', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Esta función verifica si el usuario logueado es el dueño del comentario
        comentario = self.get_object()
        return self.request.user == comentario.usuario

class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/comentario_eliminar.html' # Template de confirmación

    def get_success_url(self):
        return reverse_lazy('apps.posts:post_individual', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.usuario
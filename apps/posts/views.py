from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
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

# 3. Vistas CRUD (Solo usuarios logueados)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('apps.posts:posts')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('apps.posts:posts')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:posts')


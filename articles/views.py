from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as dj_login, logout as dj_logout
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, ListView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint
from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm, UserEditForm, UserResetForm, ChangeUserPassword, CommentForm, \
    EditCommentForm, CreatePostForm, EditPostForm
from .models import CustomUser, Post, Tag, Category, Comment


# Create your views here.

def like_view(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        messages.info(request, 'Может передумаешь?')
        post.likes.remove(request.user)
        liked = False
    else:
        messages.success(request, 'Спасибо за положительный отклик! 🍬 🍨')
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post', args=[str(slug)]))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'articles/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            dj_login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'articles/login.html', {'form': form})


def logout(request):
    dj_logout(request)
    return redirect('home')


class UserProfileDetail(DetailView):
    model = CustomUser
    template_name = 'articles/user-profile.html'
    context_object_name = 'detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_posts'] = Post.objects.filter(author=self.object)
        return context


class HomePage(ListView):
    model = Post
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['populars'] = Post.objects.order_by('-views')[:4]
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetail(DetailView):
    model = Post
    template_name = 'articles/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

    # лайки
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = total_likes
        context['liked'] = liked

    # кол-ство просмотров
        self.object.views = F('views') + randint(2, 15)
        self.object.save()
        self.object.refresh_from_db()

    # комментарии
        context['comments'] = stuff.comment_set.filter(published=True)
        context['form'] = CommentForm()
        # на модерации
        context['comments_false'] = stuff.comment_set.filter(published=False)

    # популярные посты
        context['popular_posts'] = Post.objects.order_by('-views')[:5]

        return context


class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.name = request.user
            form.save()
        return redirect(post.get_absolute_url())


class UpdateComment(UpdateView):
    model = Comment
    form_class = EditCommentForm
    template_name = 'articles/edit_comment.html'

    def get_success_url(self):
        messages.info(self.request, 'Комментарий опубликован')
        return reverse('update_comment', kwargs={'pk': self.object.pk})


class PostTag(ListView):
    model = Post
    template_name = 'articles/tag_post.html'
    context_object_name = 'posts'
    paginate_by = 8
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetCategory(ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])

        return context


def access_denied(request):
    return render(request, 'articles/access-denied.html')


class UserEdit(LoginRequiredMixin, UpdateView):
    form_class = UserEditForm
    login_url = '/access_denied/'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Не верно заполненное поле')
        return self.render_to_response(self.get_context_data(form=form))


class UserPasswordResetView(PasswordResetView):
    form_class = UserResetForm
    from_email = settings.EMAIL_HOST_USER
    html_email_template_name = 'registration/password_reset_email.html'


class UserPasswordResetConfirm(PasswordResetConfirmView):
    form_class = ChangeUserPassword
    post_reset_login = True
    success_url = 'http://127.0.0.1:8000/'
    template_name = 'registration/reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно обновлен')
        return super().form_valid(form)


class SearchView(ListView):
    template_name = 'articles/search.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search_post'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        context['search_post'] = f"search_post={self.request.GET.get('search_post')}&"
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'articles/add_post.html'
    raise_exception = True

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        messages.info(self.request, 'Пост отправлен на модерацию')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class EditPostView(UpdateView):
    template_name = 'articles/edit-post.html'
    model = Post
    form_class = EditPostForm

    def get_success_url(self):
        messages.success(self.request, 'Пост опубликован')
        return reverse('edit_post', kwargs={'slug': self.object.slug})


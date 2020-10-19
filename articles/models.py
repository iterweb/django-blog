from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.safestring import mark_safe
from slugify import slugify


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    facebook = models.URLField(blank=True)
    vk = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    github = models.URLField(blank=True)
    site = models.URLField(blank=True)
    label = models.CharField(blank=True, max_length=30)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    slug = models.SlugField(verbose_name='url', unique=True, max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(verbose_name='Тег', max_length=30)
    slug = models.SlugField(verbose_name='url', unique=True, max_length=60)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    photo = models.ImageField(verbose_name='Превью', upload_to='photos/%Y/%m/%d/', blank=True)
    slug = models.SlugField(verbose_name='url', unique=True, max_length=160, null=True, blank=True)
    content = models.TextField(verbose_name='Контент')
    file = models.FileField(upload_to='files/%Y/%m/%d/', blank=True, verbose_name='Файл')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='author')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    likes = models.ManyToManyField(CustomUser, related_name='blog_posts', blank=True)
    dislike = models.IntegerField(default=0, verbose_name='Дизлайк')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def get_photo(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="300">')
        else:
            return 'Нет фото'

    # pip install python-slugify
    # https://github.com/un33k/python-slugify
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + str(self.id))
        return super(Post, self).save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def get_comments(self):
        return self.comment_set.filter(parent__isnull=True, published=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField("Сообщение", max_length=2000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Post, verbose_name="пост", on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['timestamp']
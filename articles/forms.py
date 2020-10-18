from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from captcha.fields import CaptchaField
from ckeditor.widgets import CKEditorWidget

from .models import CustomUser, Comment, Post


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Каптча')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Каптча')


class UserEditForm(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'используется для входа на сайт'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    label = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Это мой статус'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Расскажите немного о себе'}))
    facebook = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://www.facebook.com/profile.php?id=00000000'}))
    vk = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://www.vk.com/id=00000000'}))
    instagram = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://www.instagram.com/my_name'}))
    telegram = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://t.me/name'}))
    youtube = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/channel/name_chanel'}))
    github = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://github.com/your_profile'}))
    site = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'https://example.com'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'avatar', 'label', 'bio', 'facebook', 'vk',
                  'instagram', 'telegram', 'youtube', 'github', 'site')

    def clean_facebook(self):
        data = self.cleaned_data['facebook']
        if data == '':
            pass
        elif "https://www.facebook.com/" not in data and "https://facebook.com/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://www.facebook.com/" или "https://facebook.com/"')
        return data

    def clean_vk(self):
        data = self.cleaned_data['vk']
        if data == '':
            pass
        elif "https://www.vk.com/" not in data and "https://vk.com/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://www.vk.com/" или "https://vk.com/"')
        return data

    def clean_instagram(self):
        data = self.cleaned_data['instagram']
        if data == '':
            pass
        elif "https://www.instagram.com/" not in data and "https://instagram.com/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://www.instagram.com/" или '
                                        '"https://instagram.com/"')
        return data

    def clean_telegram(self):
        data = self.cleaned_data['telegram']
        if data == '':
            pass
        elif "https://t.me/" not in data and "https://www.t.me/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://t.me/" или "https://www.t.me/"')
        return data

    def clean_youtube(self):
        data = self.cleaned_data['youtube']
        if data == '':
            pass
        elif "https://www.youtube.com/" not in data and "https://youtube.com/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://www.youtube.com/" или '
                                        '"https://youtube.com/"')
        return data

    def clean_github(self):
        data = self.cleaned_data['github']
        if data == '':
            pass
        elif "https://www.github.com/" not in data and "https://github.com/" not in data:
            raise forms.ValidationError('Ссылка должна начинаться с "https://www.github.com/" или '
                                        '"https://github.com/"')
        return data


class UserResetForm(PasswordResetForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    captcha = CaptchaField(label='Каптча')


class ChangeUserPassword(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Подтверждение нового пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'contactcomment', 'rows': 5, 'placeholder': 'Оставьте комментарий здесь'}))
    published = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'custom-control custom-checkbox mb-1 ml-3'}
    ))
    captcha = CaptchaField(label='Каптча')

    class Meta:
        model = Comment
        fields = ('text', 'published')


class EditCommentForm(forms.ModelForm):
    text = forms.CharField(label='Проверьте и отредактируйте... если нужно..!', widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'contactcomment', 'rows': 5, 'placeholder': 'Оставьте комментарий здесь'}))
    published = forms.BooleanField(label='Опубликовать?', widget=forms.CheckboxInput(
        attrs={'class': 'custom-control custom-checkbox mb-1 ml-3'}
    ))

    class Meta:
        model = Comment
        fields = ('text', 'published')


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Как называется ваш пост'}))
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'rows': 10}))
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    is_published = forms.BooleanField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'custom-control custom-checkbox mb-1 ml-3'}
    ))
    captcha = CaptchaField(label='Каптча')

    class Meta:
        model = Post
        fields = ('title', 'photo', 'content', 'category', 'file', 'is_published')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms

from .models import Post, Comment

MIN_POST_LEN = 30
MIN_COMMENT_LEN = 5


class PostForm(forms.ModelForm):
    """Форма добавления поста."""

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

    def clean_text(self):
        data = self.cleaned_data["text"]

        if len(data) < MIN_POST_LEN:
            raise forms.ValidationError(
                f"Длинна поста должна быть не менее {MIN_POST_LEN} символов!"
            )

        return data


class CommentForm(forms.ModelForm):
    """Форма добавления комментария."""
    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        data = self.cleaned_data['text']

        if len(data) < MIN_COMMENT_LEN:
            raise forms.ValidationError(
                f"Длинна комментария должна быть не менее {MIN_COMMENT_LEN} символов!"
            )

        return data

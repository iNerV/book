# -*- coding: utf-8 -*-

from django import forms
from blog.models import Post


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'content_short')

    def save(self, author):
        post = super(AddPostForm, self).save(commit=False)
        post.author = author
        post.save()
        return post
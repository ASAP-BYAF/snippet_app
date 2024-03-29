from django.db import models
from accounts.models import CustomUser


class User(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return f'<ID = {self.id}> {self.username}'


# Create your models here.
class Lang(models.Model):
    lang = models.CharField(max_length=100)
    ### 他のテーブルとの関連
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'<ID = {self.id}> {self.user.username} --- {self.lang}'


class Type(models.Model):
    type = models.CharField(max_length=100)

    ### 他のテーブルとの関連
    lang = models.ForeignKey(Lang, on_delete=models.CASCADE)

    def __str__(self):
        return f'<ID = {self.id}> {self.lang.user.username} --- ' \
                f'{self.lang.lang} --- {self.type}'


class Snippet(models.Model):
    title = models.CharField(max_length=100)
    explanation = models.TextField(blank=True, null=True)
    code = models.TextField()
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    ### 他のテーブルとの関連
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f'<ID = {self.id}> {self.type.lang.user.username} --- ' \
               f'{self.type.lang.lang} --- ' \
               f'{self.type.type} --- {self.title}'

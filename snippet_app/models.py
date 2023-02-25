from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    def __str__(self):
        return f'<ID = {self.id}> {self.username}'

# Create your models here.
class Lang(models.Model):
    lang = models.CharField(max_length=100)
    ### 他のテーブルとの関連
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return f'<ID = {self.id}> {self.user.username} --- {self.lang}'

class Type(models.Model):
    type = models.CharField(max_length=100)

    ### 他のテーブルとの関連
    lang = models.ForeignKey(Lang, on_delete=models.PROTECT)
    def __str__(self):
        return f'<ID = {self.id}> {self.lang.lang} --- {self.type}'

class Snippet(models.Model):
    title = models.CharField(max_length=100)
    explanation = models.TextField(blank=True, null=True)
    code = models.TextField()

    ### 他のテーブルとの関連
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    def __str__(self):
        return f'<ID = {self.id}> {self.type.lang.lang} --- '\
            f'{self.type.type} --- {self.title}'


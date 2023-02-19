from django.db import models

# Create your models here.
class Lang(models.Model):
    lang = models.CharField(max_length=100)
class Type(models.Model):
    type = models.CharField(max_length=100)

    ### 他のテーブルとの関連
    lang = models.ForeignKey(Lang, on_delete=models.PROTECT)
class Snippet(models.Model):
    title = models.CharField(max_length=100)
    code = models.TextField()

    ### 他のテーブルとの関連
    type = models.ForeignKey(Type, on_delete=models.PROTECT)

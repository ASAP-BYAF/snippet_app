from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Lang, Type, Snippet
from accounts.models import CustomUser


# Create your views here.

class IndexView(TemplateView):

    def get(self, request):
        return render(request, 'snippet_app/index.html')


class SnippetListView(ListView):
    model = Snippet

    def get_context_data(self, **kwargs):
        user = self.get_user()
        lang = self.get_lang()
        if lang is not None:
            type_list = lang.type_set.all()
        else:
            type_list = None
        my_dict = {
            'user_list': CustomUser.objects.all(),
            'user': user,
            'lang_list': user.lang_set.all(),
            'lang': lang,
            'type_list': type_list,
        }
        return super().get_context_data(**my_dict)

    def get_queryset(self):
        type = self.get_type()
        if type is not None:
            self.queryset = type.snippet_set.all()
        else:
            self.queryset = None

        return super().get_queryset()

    def get_template_names(self):
        # スニペットが一つも作成されていないとき template を変更
        # 現在テスト中であり、代わりのテンプレートとして、 index.html
        #　を使っている。今後、適切な内容に変更が必要。
        if self.queryset is None:
            self.template_name = 'snippet_app/index.html'
        return super().get_template_names()
    def get_user(self):
        # 指定されてユーザーを取得。デフォルトは開発者。
        return CustomUser.objects.get(id=self.request.GET.get('user', 1))

    def get_lang(self):
        user = self.get_user()
        try:
            return Lang.objects.get(id=self.request.GET.get('lang', \
                                                            user.lang_set.first().id))
        # lang が一つも登録されていないとき
        except AttributeError:
            return None

    def get_type(self):
        lang = self.get_lang()
        try:
            return lang.type_set.get(id=self.request.GET.get('type', \
                                                             lang.type_set.first().id))
        # type が一つも登録されていないとき
        except AttributeError:
            return None

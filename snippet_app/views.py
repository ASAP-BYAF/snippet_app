from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Lang, Type, Snippet
from .forms import SnippetForm
from accounts.models import CustomUser


# Create your views here.
class GetCustomUserMixin:

    def get_context_data(self, **kwargs):
        kwargs.update({
            'person_list': CustomUser.objects.all(),
        })
        return super().get_context_data(**kwargs)

class IndexView(TemplateView):

    def get(self, request):
        return render(request, 'snippet_app/index.html')


class SnippetCreateView(LoginRequiredMixin, GetCustomUserMixin, CreateView):
    model = Snippet
    form_class = SnippetForm
    success_url = reverse_lazy('snippet_app:list')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'person': self.request.user.id,
            }
        )
        return kwargs
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        snippet = form.save(commit=False)

        # 既存の言語でスニペットを作成
        if (lang_id := self.request.POST['lang']) != '0':
            snippet.lang = Lang.objects.get(id=lang_id)
            # 既存の言語でスニペットを作成
            if (type_id := self.request.POST['type'].split('.')[-1]) != '0':
                snippet.type = Type.objects.get(id=type_id)
            # 新しい分類でスニペットを作成
            else:
                snippet.type = save_new_type(self.request.POST['new_type'], snippet.lang)
        # 新しい言語でスニペットを作成
        else:
            user = self.request.user
            snippet.lang = save_new_lang(user, self.request.POST['new_lang'])
            snippet.type = save_new_type(self.request.POST['new_type'], snippet.lang)

        snippet.save()
        messages.add_message(self.request, messages.SUCCESS, '新しいスニペットを作成しました。')
        self.object = snippet
        return HttpResponseRedirect(self.get_success_url())


class SnippetUpdateView(LoginRequiredMixin, GetCustomUserMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm
    success_url = reverse_lazy('snippet_app:list')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'person': self.request.GET['person'],
            }
        )
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        snippet = form.save(commit=False)

        # 既存の言語でスニペットを作成
        if (lang_id := self.request.POST['lang']) != '0':
            snippet.lang = Lang.objects.get(id=lang_id)
            # 既存の言語でスニペットを作成
            if (type_id := self.request.POST['type'].split('.')[-1]) != '0':
                snippet.type = Type.objects.get(id=type_id)
            # 新しい分類でスニペットを作成
            else:
                snippet.type = save_new_type(self.request.POST['new_type'], snippet.lang)
        # 新しい言語でスニペットを作成
        else:
            user = self.request.user
            snippet.lang = save_new_lang(user, self.request.POST['new_lang'])
            snippet.type = save_new_type(self.request.POST['new_type'], snippet.lang)

        snippet.save()
        messages.add_message(self.request, messages.SUCCESS, 'スニペットを一部変更しました。')
        self.object = snippet
        return HttpResponseRedirect(self.get_success_url())


class SnippetDeleteView(LoginRequiredMixin, GetCustomUserMixin, DeleteView):
    model = Snippet
    success_url = reverse_lazy('snippet_app:list')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def delete(self, request, *args, **kwargs):
        # messages.add_message(self.request, messages.SUCCESS, 'スニペットを削除しました。')
        return super().delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        kwargs.update(
            {'snippet': kwargs['object']}
        )
        return super().get_context_data(**kwargs)


class SnippetListView(GetCustomUserMixin, ListView):
    model = Snippet

    def get_context_data(self, **kwargs):
        person = self.get_person()
        lang = self.get_lang()
        if lang is not None:
            type_list = lang.type_set.all()
        else:
            type_list = None
        kwargs.update({
            'person': person,
            'lang': lang,
            'type': self.get_type(),
            'lang_type_snippet': [[i_lang, [[i_type, i_type.snippet_set.all()] for i_type in i_lang.type_set.all()]] for i_lang in person.lang_set.all()],
        })
        return super().get_context_data(**kwargs)

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
        # 　を使っている。今後、適切な内容に変更が必要。
        if self.queryset is None:
            self.template_name = 'snippet_app/index.html'
        return super().get_template_names()

    def get_person(self):
        # 指定されてユーザーを取得。デフォルトは開発者。
        return CustomUser.objects.get(id=self.request.GET.get('person', 1))

    def get_lang(self):
        person = self.get_person()
        try:
            return Lang.objects.get(id=self.request.GET.get('lang',
                                                            person.lang_set.first().id))
        # lang が一つも登録されていないとき
        except AttributeError:
            return None

    def get_type(self):
        lang = self.get_lang()
        try:
            return lang.type_set.get(id=self.request.GET.get('type',
                                                             lang.type_set.first().id))
        # type が一つも登録されていないとき
        except AttributeError:
            return None

def save_new_type(type, lang):
    new_type = Type()
    new_type.type = type
    new_type.lang = lang
    new_type.save()
    return new_type

def save_new_lang(user, lang):
    new_lang = Lang()
    new_lang.lang = lang
    new_lang.user = user
    new_lang.save()
    return new_lang



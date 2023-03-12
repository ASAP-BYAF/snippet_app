from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Lang, Type, Snippet
from .forms import SnippetForm
from accounts.models import CustomUser


# Create your views here.

class IndexView(TemplateView):

    def get(self, request):
        return render(request, 'snippet_app/index.html')


class SnippetCreateView(LoginRequiredMixin, CreateView):
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
        type_id = self.request.POST['type'].split('.')[1]
        snippet.type = Type.objects.get(id = type_id)
        snippet.type = Type.objects.get(id = self.request.POST['lang'])
        print(snippet)
        print(snippet.code)
        print(snippet.explanation)
        snippet.save()
        self.object = snippet
        return HttpResponseRedirect(self.get_success_url())
class SnippetListView(ListView):
    model = Snippet

    def get_context_data(self, **kwargs):
        person = self.get_person()
        lang = self.get_lang()
        if lang is not None:
            type_list = lang.type_set.all()
        else:
            type_list = None
        my_dict = {
            'person_list': CustomUser.objects.all(),
            'person': person,
            'lang_list': person.lang_set.all(),
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

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
    def get(self, request):
        self.get_user()
        return super().get(self.request)
    def get_context_data(self, **kwargs):
        user = self.user
        lang = Lang.objects.get(id=self.request.GET.get('lang', \
            user.lang_set.first().id))
        my_dict = {
            'user_list': CustomUser.objects.all(),
            'lang_list': user.lang_set.all(),
            'lang': lang,
            'type_list': lang.type_set.all(),
        }
        return super().get_context_data(**my_dict)
    def get_queryset(self):
        user = self.user
        lang = Lang.objects.get(id=self.request.GET.get('lang', \
            user.lang_set.first().id))
        type = lang.type_set.get(id=self.request.GET.get('type',\
            lang.type_set.first().id))
        self.queryset = type.snippet_set.all()
        return super().get_queryset()

    def get_user(self):
        self.user = CustomUser.objects.get(id=self.request.GET.get('user', 1))
        return
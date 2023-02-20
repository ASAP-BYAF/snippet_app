from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Lang, Type, Snippet
# Create your views here.

class IndexView(TemplateView):

    def get(self, request):
        return render(request, 'snippet_app/index.html')

class SnippetListView(ListView):
    model = Snippet
    def get_context_data(self, **kwargs):
        my_dict = {
            'lang_list': Lang.objects.all(),
            'type_list': Type.objects.all(),
        }
        return super().get_context_data(**my_dict)
    def get_queryset(self):
        lang = Lang.objects.get(id=self.request.GET.get('lang', 1))
        type = lang.type_set.get(id=self.request.GET.get('type', 1))
        self.queryset = type.snippet_set.all()
        return super().get_queryset()


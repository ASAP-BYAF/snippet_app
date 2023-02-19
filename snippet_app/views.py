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


from django import forms
from .models import Snippet, Lang, Type


class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ['title', 'code', 'explanation',]

    def __init__(self, person, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lang_queryset = Lang.objects.filter(user__id=person)
        lang_list = [(i_lang.id, i_lang.lang) for i_lang in lang_queryset]
        type_list = [(i_type.id, i_type.type) for i_lang in lang_queryset
            for i_type in i_lang.type_set.all()]
        self.fields['lang'] = forms.ChoiceField(
            choices=lang_list,
            widget = forms.RadioSelect
        )
        self.fields['type'] = forms.ChoiceField(
            choices = type_list,
            widget = forms.RadioSelect
        )

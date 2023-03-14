from django import forms
from .models import Snippet, Lang, Type
from collections import OrderedDict

class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ['title', 'code', 'explanation',]
        labels={
            'title': 'タイトル',
            'code': 'コード',
            'explanation': '説明'
            }
    def __init__(self, person, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lang_queryset = Lang.objects.filter(user__id=person)
        lang_list = [(i_lang.id, i_lang.lang) for i_lang in lang_queryset]
        lang_list.append(('0', '新しい言語を作成'))
        type_list = [(f'{i_lang.id}.{i_type.id}', i_type.type) for i_lang in lang_queryset
            for i_type in i_lang.type_set.all()]
        type_list.append(('0', '新しい分類を作成'))
        self.fields['lang'] = forms.ChoiceField(
            choices=lang_list,
            widget = forms.RadioSelect,
            label = '言語'
        )
        self.fields['new_lang'] = forms.CharField(
            label='新しい言語を入力',
            required=False
        )
        self.fields['type'] = forms.ChoiceField(
            choices = type_list,
            widget = forms.RadioSelect,
            label = '分類'
        )
        self.fields['new_type'] = forms.CharField(
            label='新しい分類を入力',
            required=False
        )

        fields_keyOrder = ['lang', 'new_lang', 'type', 'new_type', \
            'title', 'code', 'explanation', ]
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)


    def clean_title(self):
        new_title = self.data['title']
        if Snippet.objects.filter(title__iexact = new_title):
            raise forms.ValidationError('既に登録されているタイトルです。')

    def clean(self):
        if self.cleaned_data['lang'] == '0':
            new_lang = self.data['new_lang']
            if not new_lang.replace(' ', '').replace('　', ''):
                raise forms.ValidationError('新しい言語が入力されていません。')
            if Lang.objects.filter(lang__iexact = new_lang):
                raise forms.ValidationError('既に登録されている言語です。')

        if self.cleaned_data['type'] == '0':
            new_type = self.data['new_type']
            if not new_type.replace(' ', '').replace('　', ''):
                raise forms.ValidationError('新しい分類が入力されていません。')
            if Type.objects.filter(type__iexact = new_type):
                raise forms.ValidationError('既に登録されている分類です。')

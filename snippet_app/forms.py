from django import forms
from .models import Snippet, Lang, Type
from collections import OrderedDict
from accounts.models import CustomUser

class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ['title', 'code', 'explanation',]
        labels={
            'title': 'タイトル',
            'code': 'コード',
            'explanation': '説明'
            }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-title'}),
            'code': forms.Textarea(attrs={
                'class': 'form-code',
                'cols': 100,
                'rows': 10}),
            'explanation': forms.Textarea(attrs={
                'class': 'form-code',
                'cols': 100,
                'rows': 10}),
        }
    def __init__(self, person, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 初期値の設定
        # update
        if self.instance.id:
            initial_lang = self.instance.type.lang.id
            initial_type = self.instance.type.id
            initial_type =f'{initial_lang}.{initial_type}'
        # create
        else:
            initial_lang = 0
            initial_type = 0

        lang_queryset = Lang.objects.filter(user__id=person)
        lang_list = [(i_lang.id, i_lang.lang) for i_lang in lang_queryset]
        lang_list.append(('0', '新しい言語を作成'))
        self.fields['lang'] = forms.ChoiceField(
            choices=lang_list,
            widget = forms.RadioSelect,
            label = '言語',
            initial=initial_lang
        )
        self.fields['new_lang'] = forms.CharField(
            label='新しい言語を入力',
            required=False,
            widget = forms.TextInput(attrs={'class': 'form-title'})
        )

        type_list = [(f'{i_lang.id}.{i_type.id}', i_type.type) for i_lang in lang_queryset
            for i_type in i_lang.type_set.all()]
        type_list.append(('0', '新しい分類を作成'))
        self.fields['type'] = forms.ChoiceField(
            choices = type_list,
            widget = forms.RadioSelect,
            label = '分類',
            initial=initial_type
        )
        self.fields['new_type'] = forms.CharField(
            label='新しい分類を入力',
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-title'})
        )

        # フィールドの並び順を設定
        fields_keyOrder = ['lang', 'new_lang', 'type', 'new_type', \
            'title', 'code', 'explanation', ]
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_keyOrder)

        # 各フォームに対して user_id の情報を持たせる
        # バリデーションの時にユーザーに関連する言語を検索するため
        self.user = CustomUser.objects.get(id = person)

    def clean(self):
        if self.cleaned_data['lang'] == '0':
            lang = self.cleaned_data['new_lang']
            if not lang.replace(' ', '').replace('　', ''):
                raise forms.ValidationError('新しい言語が入力されていません。')
            if Lang.objects.filter(user = self.user, lang__iexact = lang):
                raise forms.ValidationError('既に登録されている言語です。')

        else:
            lang = Lang.objects.get(id = self.cleaned_data['lang']).lang

        if self.cleaned_data['type'] == '0':
            new_type = self.cleaned_data['new_type']
            if not new_type.replace(' ', '').replace('　', ''):
                raise forms.ValidationError('新しい分類が入力されていません。')
            if Type.objects.filter(lang__lang__iexact = lang, type__iexact = new_type):
                raise forms.ValidationError('既に登録されている分類です。')


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username"]
        labels={
            'username': '新しいユーザー名',
            }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-title'}),
        }

class SnippetSearchForm(forms.Form):
    REFINE_LIST = [
        ("author", "作成者"),
        ("lang_type", "言語および分類"),
    ]

    refine_list = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=REFINE_LIST,
        label='絞り込む要素を選択'
    )

    AUTH_LIST = [(i_auth.id, i_auth.username) for i_auth in CustomUser.objects.all()]
    author = forms.ChoiceField(
        choices=AUTH_LIST,
        required=False,
        widget=forms.RadioSelect,
        label='人物で絞り込む')

    filter_lang = forms.CharField(
        label='言語を入力',
        required=False,
        widget = forms.TextInput(attrs={'class': 'form-title'})
    )

    filter_type = forms.CharField(
        label='分類を入力',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-title'})
    )
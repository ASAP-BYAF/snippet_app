from rest_framework import serializers
from snippet_app.models import Lang, Type, Snippet
from accounts.models import CustomUser


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.CharField(style={'base_template': 'textarea.html'})
    password = serializers.CharField(style={'base_template': 'textarea.html'})


    def create(self, validated_data):
        """
        新しいUserインスタンスを作成して返す。
        インスタンスは、バリデーション済みのデータを基にして作成する。
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        既存のUserインスタンスを変更して返す。
        インスタンスは、バリデーション済みのデータを基にして変更する。
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

    def validate_user_id(self, value):

         if len(value) < 5:
             raise serializers.ValidationError("user_id が短すぎます。")
         return value

    def validate_password(self, value):

         if len(value) < 5:
             raise serializers.ValidationError("password が短すぎます。")
         return value

    def validate(self, data):

        user_id = data.get('user_id')
        password = data.get('password')

        if user_id == password:
            raise serializers.ValidationError("user_id と password の類似度が高いです。")
        return data

class SnippetModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ('code',)


class TypeModelSerializer(serializers.ModelSerializer):

    snippet_rev = SnippetModelSerializer(many=True, read_only=True)

    class Meta:
        model = Type
        fields = ('type', 'snippet_rev')

class LangModelSerializer(serializers.ModelSerializer):

    type_rev = TypeModelSerializer(many=True, read_only=True)

    class Meta:
        model = Lang
        fields = ('lang', 'type_rev')
        # fields = ('id', 'lang')


class CustomUserModelSerializer(serializers.ModelSerializer):

    lang_rev = LangModelSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'lang_rev')
        # fields = '__all__'

class FromSnippetModelSerializer(serializers.ModelSerializer):

    type = serializers.ReadOnlyField(source='type.type')
    lang = serializers.ReadOnlyField(source='type.lang.lang')
    user = serializers.   ReadOnlyField(source='type.lang.user.username')
    class Meta:
        model = Snippet
        fields = ('id', 'code', 'type', 'lang', 'user')
        # fields = '__all__'

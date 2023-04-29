from rest_framework import serializers
from .models import Snippet


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(style={'base_template': 'textarea.html'})


    def create(self, validated_data):
        """
        新しいSnippetインスタンスを作成して返す。
        インスタンスは、バリデーション済みのデータを基にして作成する。
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        既存のSnippetインスタンスを変更して返す。
        インスタンスは、バリデーション済みのデータを基にして変更する。
        """
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance

class SnippetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'code',)
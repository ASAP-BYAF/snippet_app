from rest_framework import serializers
from .models import User


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

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_id', 'password')
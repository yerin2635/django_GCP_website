from rest_framework import serializers
from home.models import Post


class work_serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'photo', 'location', 'created_at')

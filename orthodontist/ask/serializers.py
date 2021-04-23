from django.urls import reverse
from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    question_url = serializers.HyperlinkedIdentityField(view_name='ask:question')
    author_url = serializers.SerializerMethodField()
    author_first_name = serializers.ReadOnlyField(source='author.first_name')
    author_last_name = serializers.ReadOnlyField(source='author.last_name')
    author_image_url = serializers.ReadOnlyField(source='author.profile.image.url')
    answers_count = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    like_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['question_url', 'id', 'text', 'title', 'date',
                  'author_url', 'author_first_name', 'author_last_name', 'author_image_url',
                  'answers_count', 'like', 'like_count', 'like_url']

    def get_answers_count(self, obj):
        try:
            return obj.answers_count
        except:
            return None

    def get_like(self, obj):
        if self.context['user'] in obj.like.all():
            return True
        else:
            return False

    def get_like_count(self,obj):
        return obj.like_count

    def get_like_url(self, obj):
        return reverse('ask:like', args=[obj.id])

    def get_author_url(self, obj):
        return reverse('user', args=[obj.author.id])

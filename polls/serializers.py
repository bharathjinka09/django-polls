from rest_framework import serializers

from polls.models import Question, Choice


class PollsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ('url','question','choice_text','votes')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('url','question_text','pub_date')

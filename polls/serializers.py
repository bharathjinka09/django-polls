from rest_framework import serializers

from polls.models import Question, Choice


class PollsSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Question
        # fields = 'question_text', 'pub_date'
        model = Choice
        fields = '__all__'

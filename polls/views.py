from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, viewsets

from .models import Question, Choice
from polls.serializers import PollsSerializer, QuestionSerializer

# Get questions and display them


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# Vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def resultsData(request, obj):
    voteData = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for vote in votes:
        voteData.append({vote.choice_text:vote.votes})
    print(voteData)
    return JsonResponse(voteData, safe=False)

class PollsView(APIView):
    def get(self, request):
        choices = Choice.objects.all()
        context={'request': request}
        serializer = PollsSerializer(choices, many=True,context=context)

        return Response(serializer.data)


class QuestionsView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        context={'request': request}
        serializer = QuestionSerializer(questions, many=True,context=context)

        return Response(serializer.data)

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
class AnswerView(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = PollsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    

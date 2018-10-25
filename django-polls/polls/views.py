from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice

from django.views import generic


# from django.template import loader


def index(request):
    try:
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
    except Exception:
        latest_question_list = Question.objects.order_by('-pub_date')
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/other/../templates/polls/index.html', context)


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404('Question does not found.')
#
#     return render(request, 'polls/detail.html', {'question': question})

# 快捷方式
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/other/../templates/polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/other/../templates/polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/other/../templates/polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice',
        })
    else:
        select_choice.votes += 1
        select_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# 使用通用视图
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        try:
            latest_question_list = Question.objects.order_by('-pub_date')[:5]
        except Exception:
            latest_question_list = Question.objects.order_by('-pub_date')
        return latest_question_list


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

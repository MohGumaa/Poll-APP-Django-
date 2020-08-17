from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.db.models import F
from .forms import UpdateQuestion


# def index(request):
#     context = {
#         "latest_question_list" : Question.objects.order_by('-pub_date')[:5]
#     }
#     return render(request, 'poll/home.html', context)

class IndexView(generic.ListView):
    model = Question
    template_name = 'poll/home.html'
    context_object_name ='latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]


# def detail(request, pk):
#     question = get_object_or_404(Question, id=pk)
#     if request.method == "POST":
#         form = UpdateQuestion(request.POST, instance=question)
#         if form.is_valid():
#             form.save()
#             return redirect('poll:home')
#     else:
#         form = UpdateQuestion(instance=question)

#     context = {
#         "question": question,
#         "form": form
#     }

    # return render(request, 'poll/details.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = "poll/details.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultView(generic.DetailView):
    model = Question
    template_name ='poll/result.html'



def vote(request, pk):
    question = get_object_or_404(Question, id=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        raise Http404('Choice DoesNotExist')
    else:
        selected_choice.vote = F('vote') + 1
        selected_choice.save()
        # return HttpResponseRedirect(reverse('poll:result', args=(question.id,)))
        return redirect('poll:result', pk=question.id)



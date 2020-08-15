from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    context = {
        "latest_question_list" : Question.objects.order_by('-pub_date')[:5]
    }
    return render(request, 'poll/home.html', context)


def details(request, id):
    question = get_object_or_404(Question, pk=id)

    context ={
        "question": question
    }

    return render(request, "poll/details.html", context)


def result(request, id):
    question = get_object_or_404(Question, pk=id)
    context ={
        "question": question
    }
    return render(request, "poll/result.html", context)





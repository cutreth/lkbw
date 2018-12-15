from random import randint

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from quiz.models import Category, Question


def index(request):

    if not request.user.id:
        raise Http404
        return HttpResponse("Access denied")

    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return render(request, 'quiz/index.html', context)


def question(request, category_id):

    if not request.user.id:
        raise Http404
        return HttpResponse("Access denied")

    question_list = Question.objects.filter(category__exact=category_id).filter(remove__exact=False)
    question_count = question_list.count()

    if question_count == 0:
        return HttpResponse("No valid questions")

    question_id = randint(1, question_count)
    question_str = str(question_id)

    redirect_path = '/django-admin/quiz/question/'
    return redirect(redirect_path + question_str)

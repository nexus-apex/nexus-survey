import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Survey, Question, SurveyResponse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['survey_count'] = Survey.objects.count()
    ctx['survey_draft'] = Survey.objects.filter(status='draft').count()
    ctx['survey_active'] = Survey.objects.filter(status='active').count()
    ctx['survey_closed'] = Survey.objects.filter(status='closed').count()
    ctx['question_count'] = Question.objects.count()
    ctx['question_multiple_choice'] = Question.objects.filter(question_type='multiple_choice').count()
    ctx['question_rating'] = Question.objects.filter(question_type='rating').count()
    ctx['question_text'] = Question.objects.filter(question_type='text').count()
    ctx['surveyresponse_count'] = SurveyResponse.objects.count()
    ctx['surveyresponse_complete'] = SurveyResponse.objects.filter(status='complete').count()
    ctx['surveyresponse_partial'] = SurveyResponse.objects.filter(status='partial').count()
    ctx['surveyresponse_total_score'] = SurveyResponse.objects.aggregate(t=Sum('score'))['t'] or 0
    ctx['recent'] = Survey.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def survey_list(request):
    qs = Survey.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'survey_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def survey_create(request):
    if request.method == 'POST':
        obj = Survey()
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.status = request.POST.get('status', '')
        obj.responses = request.POST.get('responses') or 0
        obj.created_date = request.POST.get('created_date') or None
        obj.deadline = request.POST.get('deadline') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/surveys/')
    return render(request, 'survey_form.html', {'editing': False})


@login_required
def survey_edit(request, pk):
    obj = get_object_or_404(Survey, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.status = request.POST.get('status', '')
        obj.responses = request.POST.get('responses') or 0
        obj.created_date = request.POST.get('created_date') or None
        obj.deadline = request.POST.get('deadline') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/surveys/')
    return render(request, 'survey_form.html', {'record': obj, 'editing': True})


@login_required
def survey_delete(request, pk):
    obj = get_object_or_404(Survey, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/surveys/')


@login_required
def question_list(request):
    qs = Question.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(survey_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(question_type=status_filter)
    return render(request, 'question_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def question_create(request):
    if request.method == 'POST':
        obj = Question()
        obj.survey_title = request.POST.get('survey_title', '')
        obj.text = request.POST.get('text', '')
        obj.question_type = request.POST.get('question_type', '')
        obj.required = request.POST.get('required') == 'on'
        obj.position = request.POST.get('position') or 0
        obj.save()
        return redirect('/questions/')
    return render(request, 'question_form.html', {'editing': False})


@login_required
def question_edit(request, pk):
    obj = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        obj.survey_title = request.POST.get('survey_title', '')
        obj.text = request.POST.get('text', '')
        obj.question_type = request.POST.get('question_type', '')
        obj.required = request.POST.get('required') == 'on'
        obj.position = request.POST.get('position') or 0
        obj.save()
        return redirect('/questions/')
    return render(request, 'question_form.html', {'record': obj, 'editing': True})


@login_required
def question_delete(request, pk):
    obj = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/questions/')


@login_required
def surveyresponse_list(request):
    qs = SurveyResponse.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(survey_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'surveyresponse_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def surveyresponse_create(request):
    if request.method == 'POST':
        obj = SurveyResponse()
        obj.survey_title = request.POST.get('survey_title', '')
        obj.respondent = request.POST.get('respondent', '')
        obj.score = request.POST.get('score') or 0
        obj.submitted_date = request.POST.get('submitted_date') or None
        obj.feedback = request.POST.get('feedback', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/surveyresponses/')
    return render(request, 'surveyresponse_form.html', {'editing': False})


@login_required
def surveyresponse_edit(request, pk):
    obj = get_object_or_404(SurveyResponse, pk=pk)
    if request.method == 'POST':
        obj.survey_title = request.POST.get('survey_title', '')
        obj.respondent = request.POST.get('respondent', '')
        obj.score = request.POST.get('score') or 0
        obj.submitted_date = request.POST.get('submitted_date') or None
        obj.feedback = request.POST.get('feedback', '')
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/surveyresponses/')
    return render(request, 'surveyresponse_form.html', {'record': obj, 'editing': True})


@login_required
def surveyresponse_delete(request, pk):
    obj = get_object_or_404(SurveyResponse, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/surveyresponses/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['survey_count'] = Survey.objects.count()
    data['question_count'] = Question.objects.count()
    data['surveyresponse_count'] = SurveyResponse.objects.count()
    return JsonResponse(data)

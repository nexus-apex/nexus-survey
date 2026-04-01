from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('surveys/create/', views.survey_create, name='survey_create'),
    path('surveys/<int:pk>/edit/', views.survey_edit, name='survey_edit'),
    path('surveys/<int:pk>/delete/', views.survey_delete, name='survey_delete'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/create/', views.question_create, name='question_create'),
    path('questions/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('surveyresponses/', views.surveyresponse_list, name='surveyresponse_list'),
    path('surveyresponses/create/', views.surveyresponse_create, name='surveyresponse_create'),
    path('surveyresponses/<int:pk>/edit/', views.surveyresponse_edit, name='surveyresponse_edit'),
    path('surveyresponses/<int:pk>/delete/', views.surveyresponse_delete, name='surveyresponse_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]

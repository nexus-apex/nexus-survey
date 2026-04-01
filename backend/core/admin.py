from django.contrib import admin
from .models import Survey, Question, SurveyResponse

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "responses", "created_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "category"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["survey_title", "question_type", "required", "position", "created_at"]
    list_filter = ["question_type"]
    search_fields = ["survey_title"]

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ["survey_title", "respondent", "score", "submitted_date", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["survey_title", "respondent"]

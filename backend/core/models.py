from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("active", "Active"), ("closed", "Closed")], default="draft")
    responses = models.IntegerField(default=0)
    created_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Question(models.Model):
    survey_title = models.CharField(max_length=255)
    text = models.TextField(blank=True, default="")
    question_type = models.CharField(max_length=50, choices=[("multiple_choice", "Multiple Choice"), ("rating", "Rating"), ("text", "Text"), ("yes_no", "Yes No"), ("scale", "Scale")], default="multiple_choice")
    required = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.survey_title

class SurveyResponse(models.Model):
    survey_title = models.CharField(max_length=255)
    respondent = models.CharField(max_length=255, blank=True, default="")
    score = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    submitted_date = models.DateField(null=True, blank=True)
    feedback = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("complete", "Complete"), ("partial", "Partial")], default="complete")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.survey_title

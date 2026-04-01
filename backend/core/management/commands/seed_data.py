from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Survey, Question, SurveyResponse
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusSurvey with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexussurvey.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Survey.objects.count() == 0:
            for i in range(10):
                Survey.objects.create(
                    title=f"Sample Survey {i+1}",
                    category=f"Sample {i+1}",
                    status=random.choice(["draft", "active", "closed"]),
                    responses=random.randint(1, 100),
                    created_date=date.today() - timedelta(days=random.randint(0, 90)),
                    deadline=date.today() - timedelta(days=random.randint(0, 90)),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Survey records created'))

        if Question.objects.count() == 0:
            for i in range(10):
                Question.objects.create(
                    survey_title=f"Sample Question {i+1}",
                    text=f"Sample text for record {i+1}",
                    question_type=random.choice(["multiple_choice", "rating", "text", "yes_no", "scale"]),
                    required=random.choice([True, False]),
                    position=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 Question records created'))

        if SurveyResponse.objects.count() == 0:
            for i in range(10):
                SurveyResponse.objects.create(
                    survey_title=f"Sample SurveyResponse {i+1}",
                    respondent=f"Sample {i+1}",
                    score=round(random.uniform(1000, 50000), 2),
                    submitted_date=date.today() - timedelta(days=random.randint(0, 90)),
                    feedback=f"Sample feedback for record {i+1}",
                    status=random.choice(["complete", "partial"]),
                )
            self.stdout.write(self.style.SUCCESS('10 SurveyResponse records created'))

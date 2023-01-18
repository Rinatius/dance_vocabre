from django.db import transaction
from rest_framework import viewsets

from .models import Encounter
from .models.answersheet import AnswerSheet
from .serializer import (
    AnswerSheetSerializer,
    AnswerSheetCreateSerializer,
    AnswerSheetEditSerializer,
)
from .utils.questiongenerator import generate_questions
from .utils.answergrader import generate_encounters_and_score


class AnswerSheetViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return AnswerSheetCreateSerializer
        elif self.action == "update":
            return AnswerSheetEditSerializer
        else:
            return AnswerSheetSerializer

    def perform_create(self, serializer):
        questions, uischema, answers = generate_questions(
            serializer.validated_data["type"],
            serializer.validated_data["learner"],
            amount=10,
        )
        serializer.save(
            questions=questions, uischema=uischema, correct_answers=answers
        )

    def perform_update(self, serializer):
        encounters, score = generate_encounters_and_score(
            self.get_object(), serializer.validated_data["learner_answers"]
        )
        with transaction.atomic():
            serializer.save(score=score)
            Encounter.objects.bulk_create(encounters)

    # def create(self, request, *args, **kwargs):
    #     """
    #     post:
    #     Create a new answersheet.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         answersheet = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(
    #             serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #         )

    queryset = AnswerSheet.objects.all()

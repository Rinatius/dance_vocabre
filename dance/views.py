from django.db import transaction
from rest_framework import viewsets

from .const import EncounterType, QuestionType
from .models import Encounter
from .models.answersheet import AnswerSheet
from .serializer import (
    AnswerSheetSerializer,
    AnswerSheetCreateSerializer,
    AnswerSheetEditSerializer,
)
from .utils.questiongenerator import make_questions
from .utils.answergrader import generate_encounters_and_score
from .utils.wordselector import select_from_stack, select_words


class AnswerSheetViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return AnswerSheetCreateSerializer
        elif self.action == "update":
            return AnswerSheetEditSerializer
        else:
            return AnswerSheetSerializer

    def perform_create(self, serializer):
        learner = serializer.validated_data["learner"]
        collection = serializer.validated_data.get("collection", None)
        type = serializer.validated_data.get(
            "type", QuestionType.FAMILIAR_SELECTION
        )

        if serializer.validated_data.get("regenerate_stack", False):
            words = select_words(
                learner, serializer.validated_data["test_language"], collection
            )
        else:
            words = select_from_stack(learner, collection)
        questions, uischema, answers = make_questions(
            serializer.validated_data["type"],
            serializer.validated_data["learner"],
            serializer.validated_data["test_language"],
            serializer.validated_data["native_language"],
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

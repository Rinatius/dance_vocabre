from rest_framework import viewsets

from .models.answersheet import AnswerSheet
from .serializer import AnswerSheetSerializer


class AnswerSheetViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSheetSerializer
    queryset = AnswerSheet.objects.all()

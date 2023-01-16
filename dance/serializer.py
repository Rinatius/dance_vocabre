from rest_framework import serializers

from .models.answersheet import AnswerSheet


class AnswerSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSheet
        fields = "__all__"

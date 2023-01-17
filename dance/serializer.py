from rest_framework import serializers

from .models.answersheet import AnswerSheet


class AnswerSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSheet
        fields = "__all__"


class AnswerSheetCreateSerializer(serializers.ModelSerializer):
    questions = serializers.JSONField(read_only=True)
    uischema = serializers.JSONField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AnswerSheet
        fields = ["id", "type", "learner", "questions", "uischema"]

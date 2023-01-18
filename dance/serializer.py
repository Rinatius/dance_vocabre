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


class AnswerSheetEditSerializer(serializers.ModelSerializer):
    questions = serializers.JSONField(read_only=True)
    uischema = serializers.JSONField(read_only=True)
    correct_answers = serializers.JSONField(read_only=True)
    score = serializers.JSONField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    learner = serializers.CharField(read_only=True)

    class Meta:
        model = AnswerSheet
        fields = [
            "id",
            "type",
            "learner",
            "questions",
            "uischema",
            "learner_answers",
            "correct_answers",
            "score",
        ]

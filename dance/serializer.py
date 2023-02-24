from rest_framework import serializers

from .models.answersheet import AnswerSheet
from .utils.answergrader import generate_encounters_and_score


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
        fields = [
            "id",
            "type",
            "learner",
            "test_language",
            "native_language",
            "collection",
            "regenerate_stack",
            "clear_excluded",
            "stack_size",
            "questions",
            "uischema",
        ]

    def create(self, validated_data):
        answer_sheet = AnswerSheet(**validated_data)
        answer_sheet.generate()
        return answer_sheet


class AnswerSheetEditSerializer(serializers.ModelSerializer):
    questions = serializers.JSONField(read_only=True)
    uischema = serializers.JSONField(read_only=True)
    correct_answers = serializers.JSONField(read_only=True)
    score = serializers.JSONField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    learner = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        instance.process_answers(validated_data["learner_answers"])
        return instance

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

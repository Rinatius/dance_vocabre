from rest_framework import serializers

from .models import Learner
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

    learner_external_id = serializers.CharField(
        write_only=True,
        help_text="Learner's external ID"
    )

    class Meta:
        model = AnswerSheet
        fields = [
            "id",
            "type",
            "system",
            "learner_external_id",
            "test_language",
            "native_language",
            "collection",
            "regenerate_stack",
            "clear_excluded",
            "review",
            "stack_size",
            "questions",
            "uischema",
        ]

    def create(self, validated_data):
        learner, created = Learner.objects.get_or_create(
            external_id=validated_data.pop("learner_external_id", None),
            system=validated_data["system"]
        )
        answer_sheet = AnswerSheet(**validated_data, learner=learner)
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

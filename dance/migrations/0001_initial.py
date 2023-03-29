# Generated by Django 4.1.4 on 2023-03-02 08:41

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConText",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                ("text", models.TextField(help_text="Text for the context")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                ("schema", models.TextField(help_text="Question JSON Schema")),
                ("text", models.TextField(help_text="Text for the question")),
                (
                    "correct_response",
                    models.TextField(help_text="Correct response JSON"),
                ),
                (
                    "context",
                    models.ForeignKey(
                        help_text="Context for the questions",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="dance.context",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="System",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Word",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                ("word", models.CharField(max_length=200)),
                ("order", models.IntegerField()),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("KY", "KYRGYZ"),
                            ("EN", "ENGLISH"),
                            ("RU", "RUSSIAN"),
                        ],
                        default="EN",
                        max_length=2,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "translations",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "Translations of the word into other languages and"
                            " synonyms"
                        ),
                        to="dance.word",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                (
                    "questions",
                    models.ManyToManyField(
                        help_text="Quiz questions",
                        related_name="questions",
                        to="dance.question",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="question",
            name="words",
            field=models.ManyToManyField(
                help_text="Words tested in the question",
                related_name="questions",
                to="dance.word",
            ),
        ),
        migrations.CreateModel(
            name="Learner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                ("external_id", models.CharField(max_length=200)),
                (
                    "system",
                    models.ForeignKey(
                        help_text="System which Learner belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Learners",
                        to="dance.system",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Encounter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                (
                    "encounter_type",
                    models.CharField(
                        choices=[
                            (
                                "MQC",
                                "Correct answer to multiple choice question",
                            ),
                            (
                                "MQI",
                                "Incorrect answer to multiple choice question",
                            ),
                            (
                                "NQC",
                                (
                                    "Correct answer to multiple choice quiz"
                                    " with choices in native language"
                                ),
                            ),
                            (
                                "NQI",
                                (
                                    "Incorrect answer to multiple choice quiz"
                                    " with choices in native language"
                                ),
                            ),
                            ("SQC", "Correct answer to spelling quiz"),
                            ("SQI", "Incorrect answer to spelling quiz"),
                            ("SFC", "Word selected as familiar"),
                            ("SFI", "Word selected as unfamiliar"),
                            ("SKC", "Word selected as known"),
                            ("SKI", "Word selected as unknown"),
                        ],
                        max_length=4,
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        help_text="Learner who encountered the Word",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="encounters",
                        to="dance.learner",
                    ),
                ),
                (
                    "word",
                    models.ForeignKey(
                        help_text="Word encountered by Learner",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="encounters",
                        to="dance.word",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("words", models.ManyToManyField(blank=True, to="dance.word")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AnswerSheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("MQ", "Multiple choice quiz"),
                            (
                                "NQ",
                                (
                                    "Multiple choice quiz with choices in"
                                    " native language"
                                ),
                            ),
                            ("SQ", "Spelling quiz"),
                            ("SF", "Familiar selection"),
                            ("SK", "Known selection"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "questions",
                    models.JSONField(
                        default=dict,
                        help_text="Questions in JSON Schema format",
                    ),
                ),
                (
                    "uischema",
                    models.JSONField(
                        default=dict,
                        help_text=(
                            "UI schema for Questions in JSON Schema React Form"
                            " format"
                        ),
                    ),
                ),
                (
                    "correct_answers",
                    models.JSONField(
                        default=dict,
                        help_text=(
                            "Correct answers in JSON format matching schema in"
                            " Questions"
                        ),
                    ),
                ),
                (
                    "learner_answers",
                    models.JSONField(
                        default=dict,
                        help_text=(
                            "Answers by Learner in JSON format matching schema"
                            " in Questions"
                        ),
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        help_text="Percentage of correct responses", null=True
                    ),
                ),
                (
                    "test_language",
                    models.CharField(
                        choices=[
                            ("KY", "KYRGYZ"),
                            ("EN", "ENGLISH"),
                            ("RU", "RUSSIAN"),
                        ],
                        default="EN",
                        max_length=2,
                    ),
                ),
                (
                    "native_language",
                    models.CharField(
                        choices=[
                            ("KY", "KYRGYZ"),
                            ("EN", "ENGLISH"),
                            ("RU", "RUSSIAN"),
                        ],
                        default="EN",
                        max_length=2,
                    ),
                ),
                ("stack_size", models.IntegerField(blank=True, null=True)),
                (
                    "regenerate_stack",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text=(
                            "Flag indicating that Stack Answersheet is using"
                            " to make questions should be regenerated"
                        ),
                    ),
                ),
                (
                    "clear_excluded",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text=(
                            "Flag indicating that Stack Answersheet is using"
                            " to make questions should clear its Excluded"
                            " field. It leads to Answersheet using all Words"
                            " from Stack."
                        ),
                    ),
                ),
                (
                    "review",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        help_text=(
                            "Flag indicating that generated Answersheet will"
                            " be used for review and correctly answered"
                            " questions will not be excluded from Stack."
                        ),
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        blank=True,
                        help_text=(
                            "Selection of words that limits question"
                            " generation for an Answersheet instance. If null,"
                            " all words are considered for this particular"
                            " user and language. Collection also influences"
                            " which Stack is used."
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dance.collection",
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        help_text="Responding Learner",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="dance.learner",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates that this user has all permissions"
                            " without explicitly assigning them."
                        ),
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": (
                                "A user with that username already exists."
                            )
                        },
                        help_text=(
                            "Required. 150 characters or fewer. Letters,"
                            " digits and @/./+/-/_ only."
                        ),
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates whether the user can log into this"
                            " admin site."
                        ),
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text=(
                            "Designates whether this user should be treated as"
                            " active. Unselect this instead of deleting"
                            " accounts."
                        ),
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will get"
                            " all permissions granted to each of their groups."
                        ),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Stack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Time of creation"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="Last update time"
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("KY", "KYRGYZ"),
                            ("EN", "ENGLISH"),
                            ("RU", "RUSSIAN"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stacks",
                        to="dance.collection",
                    ),
                ),
                (
                    "excluded_words",
                    models.ManyToManyField(
                        blank=True,
                        related_name="stacks_excluded",
                        to="dance.word",
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stack",
                        to="dance.learner",
                    ),
                ),
                (
                    "words",
                    models.ManyToManyField(
                        blank=True, related_name="stacks", to="dance.word"
                    ),
                ),
            ],
            options={
                "unique_together": {("learner", "language", "collection")},
            },
        ),
    ]

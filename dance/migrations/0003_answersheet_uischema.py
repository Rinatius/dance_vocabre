# Generated by Django 4.1.4 on 2023-01-17 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0002_context_question_system_word_order_quiz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answersheet',
            name='uischema',
            field=models.TextField(blank=True, help_text='UI schema for Questions in JSON Schema React Form format', null=True),
        ),
    ]

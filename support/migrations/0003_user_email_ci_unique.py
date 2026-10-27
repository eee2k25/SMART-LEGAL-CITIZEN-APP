from django.db import migrations, models
from django.db.models.functions import Lower


def add_case_insensitive_email_constraint(apps, schema_editor):
    User = apps.get_model("auth", "User")
    constraint = models.UniqueConstraint(
        Lower("email"),
        condition=~models.Q(email=""),
        name="auth_user_email_ci_unique",
    )
    schema_editor.add_constraint(User, constraint)


def remove_case_insensitive_email_constraint(apps, schema_editor):
    User = apps.get_model("auth", "User")
    constraint = models.UniqueConstraint(
        Lower("email"),
        condition=~models.Q(email=""),
        name="auth_user_email_ci_unique",
    )
    schema_editor.remove_constraint(User, constraint)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        (
            "support",
            "0002_alter_advocate_options_alter_citizenservice_options_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            add_case_insensitive_email_constraint,
            remove_case_insensitive_email_constraint,
        ),
    ]

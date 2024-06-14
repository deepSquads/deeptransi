# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 4.2.9 on 2024-02-01 07:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trans", "0011_alter_component_suggestion_autoaccept_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="notify",
            field=models.BooleanField(
                blank=True,
                default=True,
                help_text="Send notification to subscribed users.",
                verbose_name="Notify users",
            ),
        ),
    ]
# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 4.2.5 on 2023-09-18 08:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import weblate.utils.backup
import weblate.utils.validators


class Migration(migrations.Migration):
    replaces = [
        ("wladmin", "0001_squashed_0008_auto_20191011_0816"),
        ("wladmin", "0002_supportstatus_discoverable"),
        ("wladmin", "0003_auto_20210512_1955"),
        ("wladmin", "0004_alter_backupservice_repository"),
        ("wladmin", "0005_alter_backuplog_event"),
        (
            "wladmin",
            "0006_rename_configurationerror_ignored_timestamp_wladmin_con_ignored_fb498d_idx",
        ),
        ("wladmin", "0007_supportstatus_limits"),
        ("wladmin", "0008_alter_backupservice_repository"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BackupService",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "repository",
                    models.CharField(
                        default="",
                        help_text="Use /path/to/repo for local backups or user@host:/path/to/repo or ssh://user@host:port/path/to/backups for remote SSH backups.",
                        max_length=500,
                        validators=[weblate.utils.validators.validate_backup_path],
                        verbose_name="Backup repository URL",
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("paperkey", models.TextField()),
                (
                    "passphrase",
                    models.CharField(
                        default=weblate.utils.backup.make_password, max_length=100
                    ),
                ),
            ],
            options={
                "verbose_name": "Support service",
                "verbose_name_plural": "Support services",
            },
        ),
        migrations.CreateModel(
            name="BackupLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "event",
                    models.CharField(
                        choices=[
                            ("backup", "Backup performed"),
                            ("error", "Backup failed"),
                            ("prune", "Deleted the oldest backups"),
                            ("cleanup", "Cleaned up backup storage"),
                            ("init", "Repository initialization"),
                        ],
                        db_index=True,
                        max_length=100,
                    ),
                ),
                ("log", models.TextField()),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wladmin.backupservice",
                    ),
                ),
            ],
            options={
                "verbose_name": "Backup log",
                "verbose_name_plural": "Backup logs",
            },
        ),
        migrations.CreateModel(
            name="ConfigurationError",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("ignored", models.BooleanField(db_index=True, default=False)),
            ],
            options={
                "verbose_name": "Configuration error",
                "verbose_name_plural": "Configuration errors",
                "indexes": [
                    models.Index(
                        fields=["ignored", "timestamp"],
                        name="wladmin_con_ignored_fb498d_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="SupportStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("secret", models.CharField(max_length=400)),
                ("expiry", models.DateTimeField(db_index=True, null=True)),
                ("in_limits", models.BooleanField(default=True)),
                ("discoverable", models.BooleanField(default=False)),
                ("limits", models.JSONField(default=dict)),
            ],
            options={
                "verbose_name": "Support status",
                "verbose_name_plural": "Support statuses",
            },
        ),
    ]
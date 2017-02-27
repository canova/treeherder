# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 19:50
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BugJobMap',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bug_id', models.PositiveIntegerField(db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'bug_job_map',
            },
        ),
        migrations.CreateModel(
            name='Bugscache',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('status', models.CharField(db_index=True, max_length=64)),
                ('resolution', models.CharField(blank=True, db_index=True, max_length=64)),
                ('summary', models.CharField(max_length=255)),
                ('crash_signature', models.TextField(blank=True)),
                ('keywords', models.TextField(blank=True)),
                ('os', models.CharField(blank=True, max_length=64)),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'bugscache',
                'verbose_name_plural': 'bugscache',
            },
        ),
        migrations.CreateModel(
            name='BuildPlatform',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('os_name', models.CharField(max_length=25)),
                ('platform', models.CharField(db_index=True, max_length=100)),
                ('architecture', models.CharField(blank=True, db_index=True, max_length=25)),
            ],
            options={
                'db_table': 'build_platform',
            },
        ),
        migrations.CreateModel(
            name='ClassifiedFailure',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bug_number', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'classified_failure',
            },
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=40)),
                ('author', models.CharField(max_length=150)),
                ('comments', models.TextField()),
            ],
            options={
                'db_table': 'commit',
            },
        ),
        migrations.CreateModel(
            name='ExclusionProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_default', models.BooleanField(db_index=True, default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exclusion_profiles_authored', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exclusion_profile',
            },
        ),
        migrations.CreateModel(
            name='FailureClassification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'failure_classification',
            },
        ),
        migrations.CreateModel(
            name='FailureLine',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('job_guid', models.CharField(max_length=50)),
                ('action', models.CharField(choices=[('test_result', 'test_result'), ('log', 'log'), ('crash', 'crash'), ('truncated', 'truncated')], max_length=11)),
                ('line', models.PositiveIntegerField()),
                ('test', models.TextField(blank=True, null=True)),
                ('subtest', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PASS', 'PASS'), ('FAIL', 'FAIL'), ('OK', 'OK'), ('ERROR', 'ERROR'), ('TIMEOUT', 'TIMEOUT'), ('CRASH', 'CRASH'), ('ASSERT', 'ASSERT'), ('SKIP', 'SKIP'), ('NOTRUN', 'NOTRUN')], max_length=7)),
                ('expected', models.CharField(blank=True, choices=[('PASS', 'PASS'), ('FAIL', 'FAIL'), ('OK', 'OK'), ('ERROR', 'ERROR'), ('TIMEOUT', 'TIMEOUT'), ('CRASH', 'CRASH'), ('ASSERT', 'ASSERT'), ('SKIP', 'SKIP'), ('NOTRUN', 'NOTRUN')], max_length=7, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('signature', models.TextField(blank=True, null=True)),
                ('level', models.CharField(blank=True, choices=[('PASS', 'PASS'), ('FAIL', 'FAIL'), ('OK', 'OK'), ('ERROR', 'ERROR'), ('TIMEOUT', 'TIMEOUT'), ('CRASH', 'CRASH'), ('ASSERT', 'ASSERT'), ('SKIP', 'SKIP'), ('NOTRUN', 'NOTRUN')], max_length=8, null=True)),
                ('stack', models.TextField(blank=True, null=True)),
                ('stackwalk_stdout', models.TextField(blank=True, null=True)),
                ('stackwalk_stderr', models.TextField(blank=True, null=True)),
                ('best_is_verified', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('best_classification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_for_lines', to='model.ClassifiedFailure')),
            ],
            options={
                'db_table': 'failure_line',
            },
        ),
        migrations.CreateModel(
            name='FailureMatch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('classified_failure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='model.ClassifiedFailure')),
                ('failure_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='model.FailureLine')),
            ],
            options={
                'db_table': 'failure_match',
                'verbose_name_plural': 'failure matches',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('guid', models.CharField(max_length=50, unique=True)),
                ('project_specific_id', models.PositiveIntegerField(null=True)),
                ('coalesced_to_guid', models.CharField(default=None, max_length=50, null=True)),
                ('option_collection_hash', models.CharField(max_length=64)),
                ('who', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=125)),
                ('result', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('submit_time', models.DateTimeField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('running_eta', models.PositiveIntegerField(default=None, null=True)),
                ('tier', models.PositiveIntegerField()),
                ('build_platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.BuildPlatform')),
                ('failure_classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.FailureClassification')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='JobDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=70, null=True)),
                ('value', models.CharField(max_length=125)),
                ('url', models.URLField(max_length=512, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Job')),
            ],
            options={
                'db_table': 'job_detail',
            },
        ),
        migrations.CreateModel(
            name='JobDuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(max_length=50)),
                ('average_duration', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'job_duration',
            },
        ),
        migrations.CreateModel(
            name='JobExclusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('info', jsonfield.fields.JSONField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'job_exclusion',
            },
        ),
        migrations.CreateModel(
            name='JobGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, default='?', max_length=25)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'job_group',
            },
        ),
        migrations.CreateModel(
            name='JobLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=255)),
                ('status', models.IntegerField(choices=[(0, 'pending'), (1, 'parsed'), (2, 'failed')], default=0)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Job')),
            ],
            options={
                'db_table': 'job_log',
            },
        ),
        migrations.CreateModel(
            name='JobNote',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('failure_classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.FailureClassification')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'job_note',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, default='?', max_length=25)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('job_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='model.JobGroup')),
            ],
            options={
                'db_table': 'job_type',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'machine',
            },
        ),
        migrations.CreateModel(
            name='MachinePlatform',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('os_name', models.CharField(max_length=25)),
                ('platform', models.CharField(db_index=True, max_length=100)),
                ('architecture', models.CharField(blank=True, db_index=True, max_length=25)),
            ],
            options={
                'db_table': 'machine_platform',
            },
        ),
        migrations.CreateModel(
            name='Matcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'matcher',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'option',
            },
        ),
        migrations.CreateModel(
            name='OptionCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('option_collection_hash', models.CharField(max_length=40)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Option')),
            ],
            options={
                'db_table': 'option_collection',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Push',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision_hash', models.CharField(max_length=50, null=True)),
                ('revision', models.CharField(max_length=40, null=True)),
                ('author', models.CharField(max_length=150)),
                ('time', models.DateTimeField()),
            ],
            options={
                'db_table': 'push',
            },
        ),
        migrations.CreateModel(
            name='ReferenceDataSignatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('signature', models.CharField(db_index=True, max_length=50)),
                ('build_os_name', models.CharField(db_index=True, max_length=25)),
                ('build_platform', models.CharField(db_index=True, max_length=100)),
                ('build_architecture', models.CharField(db_index=True, max_length=25)),
                ('machine_os_name', models.CharField(db_index=True, max_length=25)),
                ('machine_platform', models.CharField(db_index=True, max_length=100)),
                ('machine_architecture', models.CharField(db_index=True, max_length=25)),
                ('job_group_name', models.CharField(blank=True, db_index=True, max_length=100)),
                ('job_group_symbol', models.CharField(blank=True, db_index=True, max_length=25)),
                ('job_type_name', models.CharField(db_index=True, max_length=100)),
                ('job_type_symbol', models.CharField(blank=True, db_index=True, max_length=25)),
                ('option_collection_hash', models.CharField(blank=True, db_index=True, max_length=64)),
                ('build_system_type', models.CharField(blank=True, db_index=True, max_length=25)),
                ('repository', models.CharField(db_index=True, max_length=50)),
                ('first_submission_timestamp', models.IntegerField(db_index=True)),
            ],
            options={
                'db_table': 'reference_data_signatures',
                'verbose_name_plural': 'reference data signatures',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('dvcs_type', models.CharField(db_index=True, max_length=25)),
                ('url', models.CharField(max_length=255)),
                ('branch', models.CharField(db_index=True, max_length=50, null=True)),
                ('codebase', models.CharField(blank=True, db_index=True, max_length=50)),
                ('description', models.TextField(blank=True)),
                ('active_status', models.CharField(blank=True, db_index=True, default='active', max_length=7)),
                ('performance_alerts_enabled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'repository',
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.CreateModel(
            name='RepositoryGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'repository_group',
            },
        ),
        migrations.CreateModel(
            name='RunnableJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('option_collection_hash', models.CharField(max_length=64)),
                ('ref_data_name', models.CharField(max_length=255)),
                ('build_system_type', models.CharField(max_length=25)),
                ('last_touched', models.DateTimeField(auto_now=True)),
                ('build_platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.BuildPlatform')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.JobType')),
                ('machine_platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.MachinePlatform')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository')),
            ],
            options={
                'db_table': 'runnable_job',
            },
        ),
        migrations.CreateModel(
            name='TextLogError',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('line', models.TextField()),
                ('line_number', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'text_log_error',
            },
        ),
        migrations.CreateModel(
            name='TextLogStep',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('started', models.DateTimeField(null=True)),
                ('finished', models.DateTimeField(null=True)),
                ('started_line_number', models.PositiveIntegerField()),
                ('finished_line_number', models.PositiveIntegerField()),
                ('result', models.IntegerField(choices=[(0, 'success'), (1, 'testfailed'), (2, 'busted'), (3, 'skipped'), (4, 'exception'), (5, 'retry'), (6, 'usercancel'), (7, 'unknown')])),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Job')),
            ],
            options={
                'db_table': 'text_log_step',
            },
        ),
        migrations.CreateModel(
            name='TextLogSummary',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('job_guid', models.CharField(max_length=50)),
                ('text_log_summary_artifact_id', models.PositiveIntegerField(blank=True, null=True)),
                ('bug_suggestions_artifact_id', models.PositiveIntegerField(blank=True, null=True)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository')),
            ],
            options={
                'db_table': 'text_log_summary',
            },
        ),
        migrations.CreateModel(
            name='TextLogSummaryLine',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('line_number', models.PositiveIntegerField(blank=True, null=True)),
                ('bug_number', models.PositiveIntegerField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('failure_line', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_log_line', to='model.FailureLine')),
                ('summary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='model.TextLogSummary')),
            ],
            options={
                'db_table': 'text_log_summary_line',
            },
        ),
        migrations.CreateModel(
            name='UserExclusionProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(db_index=True, default=True)),
                ('exclusion_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='model.ExclusionProfile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exclusion_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_exclusion_profile',
            },
        ),
        migrations.AddField(
            model_name='textlogerror',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='model.TextLogStep'),
        ),
        migrations.AddField(
            model_name='repository',
            name='repository_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.RepositoryGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='referencedatasignatures',
            unique_together=set([('name', 'signature', 'build_system_type', 'repository')]),
        ),
        migrations.AddField(
            model_name='push',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository'),
        ),
        migrations.AlterUniqueTogether(
            name='machineplatform',
            unique_together=set([('os_name', 'platform', 'architecture')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobgroup',
            unique_together=set([('name', 'symbol')]),
        ),
        migrations.AddField(
            model_name='jobduration',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository'),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.JobType'),
        ),
        migrations.AddField(
            model_name='job',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Machine'),
        ),
        migrations.AddField(
            model_name='job',
            name='machine_platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.MachinePlatform'),
        ),
        migrations.AddField(
            model_name='job',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Product'),
        ),
        migrations.AddField(
            model_name='job',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Push'),
        ),
        migrations.AddField(
            model_name='job',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository'),
        ),
        migrations.AddField(
            model_name='job',
            name='signature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.ReferenceDataSignatures'),
        ),
        migrations.AddField(
            model_name='failurematch',
            name='matcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Matcher'),
        ),
        migrations.AddField(
            model_name='failureline',
            name='job_log',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.JobLog'),
        ),
        migrations.AddField(
            model_name='failureline',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Repository'),
        ),
        migrations.AddField(
            model_name='exclusionprofile',
            name='exclusions',
            field=models.ManyToManyField(related_name='profiles', to='model.JobExclusion'),
        ),
        migrations.AddField(
            model_name='commit',
            name='push',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commits', to='model.Push'),
        ),
        migrations.AddField(
            model_name='classifiedfailure',
            name='failure_lines',
            field=models.ManyToManyField(related_name='classified_failures', through='model.FailureMatch', to='model.FailureLine'),
        ),
        migrations.AlterUniqueTogether(
            name='buildplatform',
            unique_together=set([('os_name', 'platform', 'architecture')]),
        ),
        migrations.AddField(
            model_name='bugjobmap',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Job'),
        ),
        migrations.AddField(
            model_name='bugjobmap',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userexclusionprofile',
            unique_together=set([('user', 'exclusion_profile')]),
        ),
        migrations.AlterUniqueTogether(
            name='textlogsummary',
            unique_together=set([('job_guid', 'repository')]),
        ),
        migrations.AlterUniqueTogether(
            name='textlogstep',
            unique_together=set([('job', 'started_line_number', 'finished_line_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='textlogerror',
            unique_together=set([('step', 'line_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='runnablejob',
            unique_together=set([('ref_data_name', 'build_system_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='push',
            unique_together=set([('repository', 'revision_hash'), ('repository', 'revision')]),
        ),
        migrations.AlterUniqueTogether(
            name='optioncollection',
            unique_together=set([('option_collection_hash', 'option')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobtype',
            unique_together=set([('name', 'symbol')]),
        ),
        migrations.AlterUniqueTogether(
            name='joblog',
            unique_together=set([('job', 'name', 'url')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobduration',
            unique_together=set([('signature', 'repository')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobdetail',
            unique_together=set([('title', 'value', 'job')]),
        ),
        migrations.AlterUniqueTogether(
            name='job',
            unique_together=set([('repository', 'project_specific_id')]),
        ),
        migrations.AlterIndexTogether(
            name='job',
            index_together=set([('repository', 'option_collection_hash', 'job_type', 'start_time'), ('repository', 'job_type', 'start_time'), ('repository', 'build_platform', 'option_collection_hash', 'job_type', 'start_time'), ('machine_platform', 'option_collection_hash', 'push'), ('repository', 'build_platform', 'job_type', 'start_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='failurematch',
            unique_together=set([('failure_line', 'classified_failure', 'matcher')]),
        ),
        migrations.AlterUniqueTogether(
            name='failureline',
            unique_together=set([('job_log', 'line')]),
        ),
        migrations.AlterIndexTogether(
            name='failureline',
            index_together=set([('job_guid', 'repository')]),
        ),
        migrations.AlterUniqueTogether(
            name='commit',
            unique_together=set([('push', 'revision')]),
        ),
        migrations.AlterUniqueTogether(
            name='bugjobmap',
            unique_together=set([('job', 'bug_id')]),
        ),

        # Manually created migrations.

        # Since Django doesn't natively support creating FULLTEXT indicies.
        migrations.RunSQL(
            ['CREATE FULLTEXT INDEX idx_summary ON bugscache (summary);'],
            reverse_sql=['ALTER TABLE bugscache DROP INDEX idx_summary;'],
        ),
        # Since Django doesn't natively support creating composite prefix indicies.
        migrations.RunSQL(
            [
                'CREATE INDEX failure_line_test_idx ON failure_line (test(50), subtest(25), status, expected, created);',
                'CREATE INDEX failure_line_signature_test_idx ON failure_line (signature(25), test(50), created);',
            ],
            reverse_sql=[
                'DROP INDEX failure_line_test_idx ON failure_line;',
                'DROP INDEX failure_line_signature_test_idx ON failure_line;',
            ],
            state_operations=[
                migrations.AlterIndexTogether(
                    name='failureline',
                    index_together=set([
                        ('test', 'subtest', 'status', 'expected', 'created'),
                        ('job_guid', 'repository'),
                        ('signature', 'test', 'created'),
                    ])
                ),
            ],
        ),
    ]

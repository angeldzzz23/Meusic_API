# Generated by Django 4.1.4 on 2023-02-07 03:53

import authentication.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='user_id')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('about_me', models.CharField(blank=True, max_length=250, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_verified', models.BooleanField(default=False, help_text='Designates whether this users email is verified. ', verbose_name='email_verified')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Genders',
            fields=[
                ('gender_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='gender_id')),
                ('gender_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'Genders',
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('genre_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='genre_id')),
                ('genre_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('nationality_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='nationality_id')),
                ('nationality_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'Nationalities',
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('skill_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='skill_id')),
                ('skill_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('verification_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_artist_id')),
                ('code', models.IntegerField(null=True)),
                ('email', models.EmailField(default='SOME STRING', max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Youtube',
            fields=[
                ('youtube_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='youtube_id')),
                ('video_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Youtube',
            },
        ),
        migrations.CreateModel(
            name='User_Vimeo',
            fields=[
                ('vimeo_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='vimeo_id')),
                ('video_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Vimeo',
            },
        ),
        migrations.CreateModel(
            name='User_Skills',
            fields=[
                ('user_skill_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_skill_id')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.skills', verbose_name='skill_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Skills',
            },
        ),
        migrations.CreateModel(
            name='User_Nationality',
            fields=[
                ('user_nationality_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_nationality_id')),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.nationality', verbose_name='nationality_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Nationalities',
            },
        ),
        migrations.CreateModel(
            name='User_Genres',
            fields=[
                ('user_genre_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_genre_id')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.genres', verbose_name='genre_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Genres',
            },
        ),
        migrations.CreateModel(
            name='User_Artists',
            fields=[
                ('user_artist_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_artist_id')),
                ('artist', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Artists',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.genders'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]

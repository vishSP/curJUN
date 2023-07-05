# Generated by Django 4.2.3 on 2023-07-04 09:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='контактный email')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(verbose_name='Время рассылки')),
                ('frequency', models.CharField(
                    choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')],
                    default='daily', max_length=50, verbose_name='Периодичность')),
                ('mailing_status',
                 models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('finished', 'Завершена')],
                                  default='created', max_length=50, verbose_name='Статус рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'permissions': [('set_mailing_status', 'Can set mailing status')],
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('status', models.CharField(
                    choices=[('sent', 'Отправлено'), ('failed', 'Не удалось отправить'), ('pending', 'В ожидании')],
                    default='pending', max_length=50, verbose_name='статус попытки')),
                ('server_response',
                 models.CharField(blank=True, max_length=150, null=True, verbose_name='ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]

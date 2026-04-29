from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]

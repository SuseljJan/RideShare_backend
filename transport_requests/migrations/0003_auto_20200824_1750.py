# Generated by Django 2.2.7 on 2020-08-24 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport_requests', '0002_remove_transportrequest_locations_were_unchanged'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportrequest',
            name='transport_found',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transportrequest',
            name='inside_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='campaign', to='campaign.Campaign'),
        ),
    ]
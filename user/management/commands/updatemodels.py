from django.core.management.base import BaseCommand

import pandas as pd
from user.models import WeatherClass

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv('bulkcsvdata.csv')
        for TIMERANGE, CONDITION,LOCATION,AVERAGE in zip(df.date,df.condition,df.location,df.temperature):
            models = WeatherClass(timerange = TIMERANGE, condition = CONDITION,location = LOCATION, average = AVERAGE)
            models.save()
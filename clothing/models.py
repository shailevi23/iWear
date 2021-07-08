from datetime import date
from django.db import models
from django.utils import timezone
from iWear.settings import AUTH_USER_MODEL


class ClothCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name 


class ClothingItem(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Item_owner')
    category = models.ForeignKey(ClothCategory, null=True, on_delete=models.SET_NULL, related_name='Item_category')
    tag_id = models.CharField(max_length=10000, primary_key=True)
    image_url = models.TextField(blank=True, default='../../static/img/default_no_img.png')

    def __str__(self):
        return f"{self.name} - {self.owner}"

    @property
    def numOfTimesWorn(self):   
        try:   
            return WornEvent.objects.filter(item=self).count()
        except:
            return 0

    @property
    def dateOfFirstUse(self):   
        try:
            return WornEvent.objects.filter(item=self).earliest('time_stamp').time_stamp
        except:
            return None

    @property
    def dateOfLastUse(self):   
        try:
            return WornEvent.objects.filter(item=self).latest('time_stamp').time_stamp
        except:
            return None

    @property
    def total_worn_events(self):
        try:   
            return WornEvent.objects.filter(item=self).count()
        except:
            return 0

    @property
    def first_worn_event_date(self):
        try:   
            worn_event =  WornEvent.objects.filter(item=self).earliest('time_stamp')
            return worn_event.time_stamp
        except:
            return date.max

    @property
    def last_worn_event_date(self):
        try:   
            worn_event = WornEvent.objects.filter(item=self).latest('time_stamp')
            return worn_event.time_stamp
        except:
            return date.min
    
    @property
    def ideal_temperture(self):
        worn_events = WornEvent.objects.filter(item=self).values()
        ideal_temp = None

        if(worn_events.count() > 0):
            temp_sum = 0

            for event in worn_events:
                temp_sum += event['temperture']
            
            ideal_temp = temp_sum / worn_events.count()
                
        return ideal_temp

class WornEvent(models.Model):
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='Worn_item')
    time_stamp =  models.DateField(default=timezone.now)
    temperture = models.IntegerField()

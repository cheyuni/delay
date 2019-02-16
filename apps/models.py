from django.db import models

class User(models.Model):
    user_num = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    is_delay = models.IntegerField(default=0)
    mail = models.EmailField()

from django.db import models

# Create your models here.
class Topic(models.Model):
    """"""
    text = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        """"""
        return self.text
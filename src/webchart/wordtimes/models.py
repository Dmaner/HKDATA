from django.db import models

# Create your models here.


class WORD(models.Model):
    word_text = models.CharField(max_length=100)
    times = models.IntegerField()

    def __str__(self):
        return self.word_text

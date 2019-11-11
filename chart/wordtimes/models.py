from django.db import models

# Create your models here.


class WORD(models.Model):
    word_text = models.CharField(max_length=100)
    times = models.IntegerField()
    relate_1 = models.CharField(max_length=100)
    relate_2 = models.CharField(max_length=100)
    relate_3 = models.CharField(max_length=100)
    relate_4 = models.CharField(max_length=100)
    relate_5 = models.CharField(max_length=100)
    belong = models.CharField(max_length=100)
    fans = models.CharField(max_length=100)

    def __str__(self):
        return self.word_text

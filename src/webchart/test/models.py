from django.db import models

# Create your models here.


class WORD(models.Model):
    word_text = models.CharField(max_length=100)
    times = models.IntegerField()
    relate_five_word = models.CharField(max_length=200)
    belong = models.CharField(max_length=100)

    def __str__(self):
        return self.word_text

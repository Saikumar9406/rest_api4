from django.db import models

# Create your models here.
class language(models.Model):
    lid=models.CharField(max_length=15,unique=True)
    lname=models.CharField(max_length=50)

    def __str__(self):
        return f'{self.lid}-{self.lname}'

class framework(models.Model):
    fid=models.CharField(max_length=15,unique=True)
    fname=models.CharField(max_length=50)
    languages=models.ForeignKey(language,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fid}-{self.fname}'

class student(models.Model):
    sid=models.CharField(max_length=15,unique=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)

    def __str__(self):
        return f'{self.sid}-{self.name}'


from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

UserModel = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_picture = models.ImageField(upload_to="images")

    def __str__(self):
        return f"{self.name}"


class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    university = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username


class RentedBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'book')



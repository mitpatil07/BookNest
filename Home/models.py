from django.db import models
from django.urls import reverse
# Create your models here.

class books_data(models.Model):
    BookName = models.CharField(max_length=100)
    BookInfo = models.CharField(max_length=100)
    Bookimg = models.ImageField(upload_to="Books", null=True)
    def __str__(self):
        return f"{self.BookName}"
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk, 'book_type': 'books_data'})


class story_book(models.Model):
    str_bookname =models.CharField(max_length=100)
    str_bookinfo =models.CharField(max_length=100)
    str_bookdsc =models.CharField(max_length=100)
    str_bookimg =models.ImageField(upload_to="storyBooks", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk, 'book_type': 'story_book'})

    def __str__(self):
        return f"{self.str_bookname}"

class History_book(models.Model):
    hstr_bookname =models.CharField(max_length=100)
    hstr_bookinfo =models.CharField(max_length=100)
    hstr_bookdsc =models.CharField(max_length=100)
    hstr_bookimg =models.ImageField(upload_to="storyBooks", null=True, blank=True)

    def __str__(self):
        return f"{self.hstr_bookname}"
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk, 'book_type': 'History_book'})
    

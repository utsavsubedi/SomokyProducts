from django.urls import reverse
from django.db import models
import os
import requests
import json
import base64

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200, unique= True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    photo_url = models.TextField(default='https://loisirs.saint-georges.ca/wp-content/uploads/2021/03/Titre-Activites-CSLD.png')

    def save(self):
        encodedString = base64.b64encode(self.cat_image.file.read())
        data = {"key": '49d229e1d79585f1c66bde14cb6e33a7', "image": encodedString.decode("utf-8")}
        uploadedImageInfo = requests.post("https://api.imgbb.com/1/upload", data=data)
        jsonResponse = json.loads(uploadedImageInfo.text)
        self.photo_url = jsonResponse["data"]["display_url"]
        super().save()

    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"
        
    def get_url(self):
        return reverse('products_by_category', args = [self.slug])
    
    def __str__(self):
        return self.category_name
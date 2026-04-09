from django.db import models

class Experience(models.Model):
    role = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='experience_images/')

    def __str__(self):
        return self.role
    
class Idea(models.Model):
    title = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='ideas/')
    
    document = models.FileField(upload_to='ideas_docs/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    short_description = models.TextField()
    content = models.TextField()

    image = models.ImageField(upload_to='articles/')
    external_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class ProjectStats(models.Model):
    projects = models.IntegerField()
    clients = models.IntegerField()
    experience = models.IntegerField()
    certifications = models.IntegerField()

    def __str__(self):
        return "Project Stats"

    class Meta:
        verbose_name_plural = "Project Stats"


class Project(models.Model):
    title = models.CharField(max_length=200)
    purpose = models.CharField(max_length=200)
    description = models.TextField()

    image1 = models.ImageField(upload_to='projects/')
    image2 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image3 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image4 = models.ImageField(upload_to='projects/', blank=True, null=True)

    def __str__(self):
        return self.title
    
# models.py


class Journey(models.Model):
    title = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome class (e.g. fas fa-graduation-cap)")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Purchase(models.Model):
    idea = models.ForeignKey('Idea', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(max_length=20, default="created")  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.idea.title}"




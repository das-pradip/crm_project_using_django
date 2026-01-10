from django.db import models
# import User for lead assignment and creation tracking
from django.contrib.auth.models import User

class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    state = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

   

    
    def __str__(self):

        return self.first_name + "   " + self.last_name
    


# Lead model
class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Who created the lead
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_leads')
    
    # Who is assigned to handle this lead (optional)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    # when lead converted to customer
    is_converted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
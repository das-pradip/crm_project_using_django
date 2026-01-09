# from django.db import models
# from django.contrib.auth.models import User
# from .models import Record   # if Record is in same app, adjust import


# class Lead(models.Model):

#     STATUS_CHOICES = (
#         ('new', 'New'),
#         ('contacted', 'Contacted'),
#         ('qualified', 'Qualified'),
#         ('converted', 'Converted'),
#         ('lost', 'Lost'),
#     )

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default='new'
#     )

#     assigned_to = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='assigned_leads'
#     )

#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='created_leads'
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

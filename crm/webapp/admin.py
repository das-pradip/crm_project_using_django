from django.contrib import admin
# import Lead model
from .models import Lead

# Register your models here.
from .models import Record

admin.site.register(Record)

# Register Lead model
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone', 'status', 'assigned_to', 'created_by')
    list_filter = ('status',)
    search_fields = ('first_name', 'email')
   

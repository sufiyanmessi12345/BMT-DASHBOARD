# bmtapp/models.py

from django.db import models

class Section(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class SectionUser(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128) # Stores hashed password

    def __str__(self):
        return f"{self.username} ({self.section.title})"

class OrderItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='order_items')
    order_id = models.CharField(max_length=100, db_index=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    po_number = models.CharField(max_length=100, blank=True, null=True)
    dc_number = models.CharField(max_length=100, blank=True, null=True)
    po_over_due = models.DateField(blank=True, null=True)
    po_expiry_over_due = models.DateField(blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    expected_date = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    balance_qty = models.IntegerField(blank=True, null=True)
    sent_qty = models.IntegerField(blank=True, null=True)
    uom = models.CharField(max_length=50, blank=True, null=True)
    td = models.CharField(max_length=50, verbose_name="T.D.", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    pending_days = models.IntegerField(blank=True, null=True)
    
    # These fields are added for better data management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # An order ID should be unique within a section to prevent duplicates
        unique_together = ('section', 'order_id')

    def __str__(self):
        return f"Order {self.order_id} in {self.section.title}"

def get_attachment_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/attachments/<order_id>/<filename>
    return f'attachments/{instance.order_item.order_id}/{filename}'

class Attachment(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=get_attachment_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
# bmtapp/models.py

from django.db import models

class Section(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class SectionUser(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128) # Stores hashed password

    def __str__(self):
        return f"{self.username} ({self.section.title})"

class OrderItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='order_items')
    order_id = models.CharField(max_length=100, db_index=True)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    product = models.CharField(max_length=200, blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    po_number = models.CharField(max_length=100, blank=True, null=True)
    dc_number = models.CharField(max_length=100, blank=True, null=True)
    po_over_due = models.DateField(blank=True, null=True)
    po_expiry_over_due = models.DateField(blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    expected_date = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    balance_qty = models.IntegerField(blank=True, null=True)
    sent_qty = models.IntegerField(blank=True, null=True)
    uom = models.CharField(max_length=50, blank=True, null=True)
    td = models.CharField(max_length=50, verbose_name="T.D.", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    pending_days = models.IntegerField(blank=True, null=True)
    
    # These fields are added for better data management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # An order ID should be unique within a section to prevent duplicates
        unique_together = ('section', 'order_id')

    def __str__(self):
        return f"Order {self.order_id} in {self.section.title}"

def get_attachment_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/attachments/<order_id>/<filename>
    return f'attachments/{instance.order_item.order_id}/{filename}'

class Attachment(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=get_attachment_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
# Create your models here.

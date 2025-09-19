# bmtapp/serializers.py

from rest_framework import serializers
from .models import OrderItem, Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='file.name', read_only=True)
    path = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = Attachment
        fields = ['name', 'path']

class OrderItemSerializer(serializers.ModelSerializer):
    # Rename 'id' to '_id' for frontend compatibility
    _id = serializers.IntegerField(source='id', read_only=True)
    
    # Map model fields (snake_case) to JSON fields (kebab-case)
    order_id = serializers.CharField(source='order_id')
    customer_name = serializers.CharField(source='customer_name', required=False, allow_blank=True)
    contact_person = serializers.CharField(source='contact_person', required=False, allow_blank=True)
    assigned_to = serializers.CharField(source='assigned_to', required=False, allow_blank=True)
    po_number = serializers.CharField(source='po_number', required=False, allow_blank=True)
    dc_number = serializers.CharField(source='dc_number', required=False, allow_blank=True)
    po_over_due = serializers.DateField(source='po_over_due', required=False, allow_null=True)
    po_expiry_over_due = serializers.DateField(source='po_expiry_over_due', required=False, allow_null=True)
    order_date = serializers.DateField(source='order_date', required=False, allow_null=True)
    expected_date = serializers.DateField(source='expected_date', required=False, allow_null=True)
    balance_qty = serializers.IntegerField(source='balance_qty', required=False, allow_null=True)
    sent_qty = serializers.IntegerField(source='sent_qty', required=False, allow_null=True)
    td = serializers.CharField(source='td', required=False, allow_blank=True)
    pending_days = serializers.IntegerField(source='pending_days', required=False, allow_null=True)

    # Use the nested serializer for attachments
    files = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        # List all fields the frontend uses, mapping them from the serializer fields above
        fields = [
            '_id', 'order_id', 'customer_name', 'contact_person', 'product', 
            'assigned_to', 'po_number', 'dc_number', 'po_over_due', 
            'po_expiry_over_due', 'order_date', 'expected_date', 'quantity', 
            'balance_qty', 'sent_qty', 'uom', 'td', 'description', 
            'note', 'status', 'pending_days', 'files'
        ]
        
    def to_representation(self, instance):
        """Convert snake_case field names to kebab-case for JSON output."""
        ret = super().to_representation(instance)
        # The serializer handles mapping during input, but we need to format the output keys
        # for fields not explicitly defined above (like 'product', 'quantity', etc.)
        formatted_ret = {
            'order-id': ret.get('order_id'),
            'customer-name': ret.get('customer_name'),
            'contact-person': ret.get('contact_person'),
            'assigned-to': ret.get('assigned_to'),
            'po-number': ret.get('po_number'),
            'dc-number': ret.get('dc_number'),
            'po-over-due': ret.get('po_over_due'),
            'po-expiry-over-due': ret.get('po_expiry_over_due'),
            'order-date': ret.get('order_date'),
            'expected-date': ret.get('expected_date'),
            'balance-qty': ret.get('balance_qty'),
            'sent-qty': ret.get('sent_qty'),
            'pending-days': ret.get('pending_days'),
            'td': ret.get('td'),
             # Fields with matching names
            '_id': ret.get('_id'),
            'product': ret.get('product'),
            'quantity': ret.get('quantity'),
            'uom': ret.get('uom'),
            'description': ret.get('description'),
            'note': ret.get('note'),
            'status': ret.get('status'),
            'files': ret.get('files'),
        }
        return formatted_ret

    def to_internal_value(self, data):
        """Convert kebab-case from JSON to snake_case for the model."""
        # This function is called on POST/PUT requests
        internal_value = {
            'order_id': data.get('order-id'),
            'customer_name': data.get('customer-name'),
            'contact_person': data.get('contact-person'),
            'product': data.get('product'),
            'assigned_to': data.get('assigned-to'),
            'po_number': data.get('po-number'),
            'dc_number': data.get('dc-number'),
            'po_over_due': data.get('po-over-due'),
            'po_expiry_over_due': data.get('po-expiry-over-due'),
            'order_date': data.get('order-date'),
            'expected_date': data.get('expected-date'),
            'quantity': data.get('quantity'),
            'balance_qty': data.get('balance-qty'),
            'sent_qty': data.get('sent-qty'),
            'uom': data.get('uom'),
            'td': data.get('t.d.'), # handle special case from frontend form
            'description': data.get('description'),
            'note': data.get('note'),
            'status': data.get('status'),
            'pending_days': data.get('pending-days'),
        }
        # Filter out None values so model defaults can be used
        return {k: v for k, v in internal_value.items() if v is not None}

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import JSONParser
from .models import Section, SectionUser, OrderItem, Attachment
from .serializers import OrderItemSerializer
import json
from django.shortcuts import render
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            section_id = body.get("section")
            username = body.get("username")
            password = body.get("password")

            user = SectionUser.objects.get(section_id=section_id, username=username)
            
            if check_password(password, user.password):
                return JsonResponse({"success": True, "section": section_id})
            else:
                return JsonResponse({"success": False, "error": "Invalid credentials"}, status=401)
        
        except (SectionUser.DoesNotExist, json.JSONDecodeError):
            return JsonResponse({"success": False, "error": "Invalid credentials or malformed request"}, status=400)
            
    return JsonResponse({"error": "POST required"}, status=405)


@csrf_exempt
def section_data(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({"error": "Section not found"}, status=404)

    if request.method == "GET":
        items = OrderItem.objects.filter(section=section).order_by('-created_at')
        serializer = OrderItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        try:
            data = JSONParser().parse(request)
            serializer = OrderItemSerializer(data=data)
            if serializer.is_valid():
                # Check for existing order_id in the same section
                if OrderItem.objects.filter(section=section, order_id=serializer.validated_data.get('order_id')).exists():
                    return JsonResponse({'error': 'Order ID already exists in this section'}, status=409)
                
                # Save the new item, linking it to the current section
                order_item = serializer.save(section=section)
                
                # Return the newly created item's data
                return JsonResponse(OrderItemSerializer(order_item).data, status=201)
            
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == "PUT":
        # This method is used by the frontend to delete items by sending the whole filtered list
        try:
            data = JSONParser().parse(request)
            
            # Delete existing items for the section
            OrderItem.objects.filter(section=section).delete()
            
            # Create new items from the provided list
            serializer = OrderItemSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save(section=section)
                return JsonResponse(serializer.data, safe=False, status=200)

            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # Handle item deletion via DELETE request
    elif request.method == "DELETE":
        item_id = request.GET.get('item_id')
        if not item_id:
             return JsonResponse({'error': 'item_id query parameter is required'}, status=400)
        try:
            item = OrderItem.objects.get(id=item_id, section=section)
            item.delete()
            return JsonResponse({'success': True, 'message': 'Item deleted'}, status=204)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)


    return JsonResponse({"error": "Method not allowed"}, status=405)
    
@csrf_exempt
def attach_file_view(request, section_id):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        file = request.FILES.get('file')

        if not item_id or not file:
            return JsonResponse({'error': 'item_id and file are required'}, status=400)

        try:
            order_item = OrderItem.objects.get(id=item_id, section_id=section_id)
            attachment = Attachment.objects.create(order_item=order_item, file=file)
            return JsonResponse({'success': True, 'file_url': attachment.file.url}, status=201)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Order item not found'}, status=404)

    return JsonResponse({"error": "POST required"}, status=405)


# This view is needed for the Admin panel user management
@csrf_exempt
def manage_users_view(request):
    # This is a placeholder. A real implementation should have authentication
    # to ensure only an admin can access this.
    if request.method == "GET":
        users = SectionUser.objects.all()
        data = {
            user.section.id: {"username": user.username, "password": ""} for user in users
        }
        # For security, admin user is hardcoded or managed separately
        data["admin"] = {"username": "admin", "password": ""}
        return JsonResponse(data)
    
    # POST to update users is not implemented for security reasons.
    # User management should be done via the Django Admin Panel.
    return JsonResponse({"error": "Method not allowed"}, status=405)


# The correct way


def index(request):
    return render(request, 'index.html')
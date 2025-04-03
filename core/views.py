from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone 
from .models import Schedule, JugReturn
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from datetime import timedelta
# Create your views here.
def get_schedules(request):
    schedules = Schedule.objects.filter(subscription=True)
    data = [s.as_dict(include_internal=True) for s in schedules]
    return JsonResponse(data, safe=False)


@csrf_exempt
def shopify_webhook(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            print("Received webhook: ", payload)

            # Extract Shopify details
            shopify_order_id = payload.get("id")
            customer_data = payload.get("customer", {})
            customer_email = customer_data.get("email")
            shopify_customer_id = str(customer_data.get("id"))

            if not customer_email:
                return JsonResponse({"error": "Missing customer email"}, status=400)

            # Get or create Django user from email
            user, created = User.objects.get_or_create(
                username=customer_email,
                defaults={"email": customer_email, "password": "temporary"}
            )

            # Try to find an existing schedule
            schedule = Schedule.objects.filter(shopify_sub_id=shopify_order_id).first()

            if not schedule:
                print("Creating new Schedule for this customer")

                schedule = Schedule.objects.create(
                    user=user,
                    event_date=timezone.now().date(),
                    next_delivery_date=timezone.now().date() + timedelta(days=14),
                    delivery_status='PENDING',
                    frequency='WEEKLY',  # Default frequency, you can improve this later
                    subscription=True,
                    shopify_sub_id=shopify_order_id,
                    shopify_customer_id=shopify_customer_id,
                    jugs_per_delivery=10  # Default or calculated based on order
                )
            else:
                # Update status if applicable
                new_status = payload.get("status", "").lower()
                if new_status == "paused":
                    schedule.subscription = False
                elif new_status == "active":
                    schedule.subscription = True
                    schedule.delivery_status = "PENDING"
                elif new_status == "skipped":
                    schedule.delivery_status = "SKIPPED"

                schedule.save()
                print(f"Schedule updated for {customer_email} - Status: {schedule.delivery_status}")

            return JsonResponse({"status": "Schedule processed"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)



@csrf_exempt   
@require_POST
def update_jug_returns(request):
    try:
        data = json.loads(request.body)
        sub_id = data.get("shopify_sub_id")
        returned = data.get("returned_jugs")

        if not sub_id or returned is None:
            return JsonResponse({"error": "Missing shopify_sub_id or returned_jugs"}, status=400)

        schedule = Schedule.objects.filter(shopify_sub_id=sub_id).first()
        if not schedule:
            return JsonResponse({"error": "Schedule not found"}, status=404)

        jug_return = JugReturn.objects.create(schedule=schedule, amount=returned)

        return JsonResponse({
            "status": "Jug return recorded",
            "customer": schedule.user.username,
            "returned": returned,
            "return_date": jug_return.return_date.strftime("%Y-%m-%d")
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

def customer_dashboard(request, shopify_sub_id):
    schedule = get_object_or_404(Schedule, shopify_sub_id=shopify_sub_id)
    return render(request, 'core/dashboard.html', {"schedule": schedule})
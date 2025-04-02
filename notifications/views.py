from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .serializers import EmployerNotificationSerializer
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import EmployerNotification, JobPostingNotification 
import json







# @login_required
# def get_notifications(request):
#     user = request.user
#     notifications_list = []  # This will store the notifications data

#     print(f"Fetching notifications for user: {user.username} (Role: {user.role})")

#     # Check if the user has a role attribute and proceed accordingly
#     if hasattr(user, 'role'):
#         # Fetch job seeker notifications
#         if user.role == 'job_seeker':
#             # Fetch general job seeker notifications
#             notifications = fication.objects.filter(applicant=user, is_read=False)
#             print(f"Job seeker notifications count: {notifications.count()}")
#             for notification in notifications:
#                 notifications_list.append({
#                     'id': notification.id,
#                     'message': notification.message,
#                     'job_title': notification.job.title if notification.job else None,
#                     'employer': notification.employer.username,
#                     'timestamp': localtime(notification.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
#                     'is_read': notification.is_read
#                 })

#             # Fetch team join request notifications for the requester
#             team_notifications = TeamJoinRequestNotification.objects.filter(user=user, is_read=False)
#             print(f"Team join request notifications for requester count: {team_notifications.count()}")
#             for notification in team_notifications:
#                 notifications_list.append({
#                     'id': notification.id,
#                     'message': notification.message,
#                     'team': notification.team.name,
#                     'timestamp': localtime(notification.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
#                     'is_read': notification.is_read
#                 })

#         # Fetch employer notifications
#         elif user.role == 'employer':
#             notifications = EmployerNotification.objects.filter(employer=user, is_read=False)
#             print(f"Employer notifications count: {notifications.count()}")
#             for notification in notifications:
#                 notifications_list.append({
#                     'id': notification.id,
#                     'message': notification.message,
#                     'job_title': notification.job.title if notification.job else None,
#                     'applicant': notification.applicant.username if notification.applicant else None,
#                     'timestamp': localtime(notification.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
#                     'is_read': notification.is_read
#                 })

#         else:
#             # If the role is not recognized, return an error
#             return JsonResponse({'error': 'Role not recognized'}, status=400)

#     else:
#         # If the user doesn't have a role, return an error
#         return JsonResponse({'error': 'User does not have a role attribute'}, status=400)

#     print(f"Total notifications to send: {len(notifications_list)}")

#     # Return the list of notifications as JSON
#     return JsonResponse(notifications_list, safe=False)




# @csrf_exempt  # Only if necessary, otherwise remove
# def mark_notification_read(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             notification_id = data.get('id')

#             if not notification_id:
#                 return HttpResponseBadRequest('Notification ID not provided')

#             # Ensure the user is authenticated
#             if request.user.is_authenticated:
#                 notification = None

#                 # Attempt to find the notification in the different models
#                 try:
#                     notification = JobSeekerNotification.objects.get(id=notification_id, applicant=request.user)
#                 except JobSeekerNotification.DoesNotExist:
#                     pass
                
#                 try:
#                     notification = EmployerNotification.objects.get(id=notification_id, employer=request.user)
#                 except EmployerNotification.DoesNotExist:
#                     pass
                
#                 try:
#                     notification = TeamJoinRequestNotification.objects.get(id=notification_id, user=request.user)
#                 except TeamJoinRequestNotification.DoesNotExist:
#                     pass

#                 if not notification:
#                     return JsonResponse({'error': 'Notification not found or not accessible by this user'}, status=404)

#                 # Mark the notification as read
#                 notification.is_read = True
#                 notification.save()

#                 return JsonResponse({'status': 'success'})

#             return JsonResponse({'error': 'User not authenticated'}, status=403)

#         except json.JSONDecodeError:
#             return HttpResponseBadRequest('Invalid JSON')
        
#         except Exception as e:
#             return HttpResponseBadRequest(f'An error occurred: {str(e)}')

#     return HttpResponseBadRequest('Invalid request method')
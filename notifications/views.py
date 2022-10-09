from django.contrib import messages
from django.shortcuts import redirect

from . import models


def set_notification_as_seen(request, notification_pk):
    url = request.META.get("HTTP_REFERER")
    try:
        notification = models.Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        url = notification.url
    except Exception:
        messages.error(request, "Couldn't complete request")
        pass
    return redirect(url)


def mark_all_as_read(request):
    url = request.META.get("HTTP_REFERER")
    user = request.user
    try:
        if user.designation == "132":
            models.Notification.objects.filter(to_station_132=user.station_132).filter(user_has_seen=False).update(
                user_has_seen=True
            )
        if user.designation == "330":
            models.Notification.objects.filter(to_station_330=user.station_330).filter(user_has_seen=False).update(
                user_has_seen=True
            )
        messages.info(request, "All notifications marked as read")
    except Exception:
        messages.error(request, "Could't complete request")
        pass
    return redirect(url)

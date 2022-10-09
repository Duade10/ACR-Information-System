from . import models


def notification_links(request):
    try:
        if request.user.designation != "330":
            notifications = models.Notification.objects.filter(to_station_132=request.user.station_132).order_by(
                "-created"
            )[:6]
            notifications_not_seen = models.Notification.objects.filter(to_station_132=request.user.station_132).filter(
                user_has_seen=False
            )
            notifications_not_seen_count = notifications_not_seen.count()
        elif request.user.designation != "132":
            notifications = models.Notification.objects.filter(to_station_330=request.user.station_330).order_by(
                "-created"
            )[:6]
            notifications_not_seen = models.Notification.objects.filter(to_station_330=request.user.station_330).filter(
                user_has_seen=False
            )
            notifications_not_seen_count = notifications_not_seen.count()
        return dict(
            notifications=notifications,
            notifications_not_seen_count=notifications_not_seen_count,
        )
    except (TypeError, AttributeError):
        return dict(
            notifications=None,
            notifications_not_seen_count=None,
        )

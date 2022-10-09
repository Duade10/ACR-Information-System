import core.views as core_views
import notifications.models as notifications_models
import stations_330.mixins as stations_330_mixins
import users.mixins as users_mixins
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, UpdateView, View
from schedulers.models import ScheduledReport

from . import forms, models


class ProtetionGuaranteeListView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.designation == "132":
            station = user.station_132
            all_protection_guarantees = models.ProtectionGuarantee.objects.filter(
                applied_to_132=user.station_132
            ).order_by("-created")
        if user.designation == "330":
            station = user.station_330
            all_protection_guarantees = models.ProtectionGuarantee.objects.filter(
                Q(applied_to_330=user.station_330) | Q(applied_to_132_330=user.station_330)
            ).order_by("-created")
        paginator = Paginator(all_protection_guarantees, 20)
        page = request.GET.get("page")
        all_protection_guarantees = paginator.get_page(page)
        context = {
            "reports": all_protection_guarantees,
            "single_station": station,
        }
        return render(request, "reports/protection_guarantee/protection_guarantee_list.html", context)


class Search(users_mixins.LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        user = request.user
        if "keyword" not in request.GET:
            return redirect(url)
        keyword = request.GET.get("keyword", None)
        if user.designation == "132":
            station = user.station_132
            all_protection_guarantees = (
                models.ProtectionGuarantee.objects.filter(applied_to_132=user.station_132)
                .filter(
                    Q(to_be_issued_to__icontains=keyword)
                    | Q(title__icontains=keyword)
                    | Q(department__icontains=keyword)
                    | Q(description_of_apparatus__icontains=keyword)
                    | Q(additional_apparatus__icontains=keyword)
                    | Q(advance_request_name__icontains=keyword)
                    | Q(received_by_name__icontains=keyword)
                    | Q(user__first_name__icontains=keyword)
                )
                .order_by("-created")
            )
        if user.designation == "330":
            station = user.station_330
            all_protection_guarantees = (
                models.ProtectionGuarantee.objects.filter(
                    Q(applied_to_330=user.station_330) | Q(applied_to_132_330=user.station_330)
                )
                .filter(
                    Q(to_be_issued_to__icontains=keyword)
                    | Q(title__icontains=keyword)
                    | Q(department__icontains=keyword)
                    | Q(description_of_apparatus__icontains=keyword)
                    | Q(additional_apparatus__icontains=keyword)
                    | Q(advance_request_name__icontains=keyword)
                    | Q(received_by_name__icontains=keyword)
                )
                .order_by("-created")
            )

        paginator = Paginator(all_protection_guarantees, 20)
        page = request.GET.get("page")
        all_protection_guarantees = paginator.get_page(page)
        context = {
            "reports": all_protection_guarantees,
            "single_station": station,
        }
        return render(request, "reports/protection_guarantee/protection_guarantee_list.html", context)


class ProtectionGuaranteeCreateView(users_mixins.LoggedInOnlyView, CreateView):
    model = models.ProtectionGuarantee
    form_class = forms.ProtectionGuaranteeForm
    template_name = "reports/protection_guarantee/protection_guarantee_create.html"

    def form_valid(self, form):
        data = form.save()
        data.user = self.request.user
        data.save()
        ScheduledReport.objects.get_or_create(protection_guarantee=data)
        core_views.socket_message(self.request, data.created_notification(), "protectionGuarantees")
        return redirect("protection_guarantees:list")


class ProtectionGuaranteeUpdateView(users_mixins.LoggedInOnlyView, UpdateView):
    model = models.ProtectionGuarantee
    form_class = forms.ProtectionGuaranteeForm
    template_name = "reports/protection_guarantee/protection_guarantee_edit.html"
    context_object_name = "single_protection_guarantee"

    def form_valid(self, form):
        data = form.save()
        data.save()
        core_views.socket_message(self.request, data.edited_notification(), "protectionGuarantees")
        return redirect("protection_guarantees:list")


class ProtectionGuaranteeDetailView(users_mixins.LoggedInOnlyView, DetailView):
    model = models.ProtectionGuarantee
    context_object_name = "single_protection_guarantee"
    template_name = "reports/protection_guarantee/protection_guarantee_detail.html"


class ProtectionGuaranteeDeleteView(users_mixins.LoggedInOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        report = models.ProtectionGuarantee.objects.get(pk=pk)
        report.delete()
        messages.warning(request, "Deleted Successfully")
        return redirect("protection_guarantee:list")


class Acknowledge(stations_330_mixins.Station330UsersOnlyView, users_mixins.LoggedInOnlyView, View):
    def get(self, request, pk, *args, **kwargs):
        url = request.META.get("HTTP_REFERER")
        try:
            user = request.user
            protection_guarantee = get_object_or_404(models.ProtectionGuarantee, pk=pk)
            if protection_guarantee.applied_to_132_330:
                if user.station_330.pk is not protection_guarantee.applied_to_132_330.pk:
                    messages.error(request, "Permission Denied!")
                    return redirect(url)
            if protection_guarantee.applied_to_330:
                if user.station_330.pk is not protection_guarantee.applied_to_330.pk:
                    messages.error(request, "Permission Denied!")
                    return redirect(url)
            protection_guarantee.is_acknowledged = True
            protection_guarantee.received_by = user
            protection_guarantee.save()
            station = user.station_330
            notification = notifications_models.Notification.objects.create(
                from_user=user,
                from_station_330=station,
                icon="check",
                text=f"{user.get_full_name()} ({station}) has acknowleged your protection guarantee.",
                url="/reports/protection-guarantees/",
            )
            notification.save()
            if protection_guarantee.applied_to_132 is not None:
                notification.to_station_132.add(protection_guarantee.applied_to_132)
                to_station = protection_guarantee.applied_to_132
            else:
                notification.to_station_330.add(protection_guarantee.applied_to_330)
                to_station = protection_guarantee.applied_to_330
            notification.save()
            core_views.socket_message(request, to_station.id, "protectionGuarantees")
            messages.success(request, "Done!")
        except Exception:
            messages.error(request, "Couldn't acknowlege report")
            pass
        return redirect(url)

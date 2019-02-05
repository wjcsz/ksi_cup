from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from mail import MailSender
from .models import CupOwner, Cup, Event
from qr_code.qrcode.utils import QRCodeOptions


class IndexView(generic.ListView):
    template_name = 'cups_control/index.html'
    context_object_name = 'cups_owners_list'

    def get_queryset(self):
        """Return all cup owners"""
        return CupOwner.objects.all()


class LatestDirty(generic.ListView):
    template_name = 'cups_control/dirty.html'
    context_object_name = 'latest_cups_list'

    def get_queryset(self):
        """Return the last five dirty cups"""
        return CupOwner.objects.filter(Cup.objects.get(is_dirty=True))


def detail(request, cup_owner_id):
    cup_owner = CupOwner.objects.get(pk=cup_owner_id)
    qr_code_url = request.build_absolute_uri(reverse('cups_control:detail', args=[cup_owner_id]))
    return render(request, 'cups_control/detail.html', {
        'cup_owner': cup_owner,
        'qr_code_url': qr_code_url,
    })


def rebuke(request, cup_owner_id):
    cup_owner = get_object_or_404(CupOwner, pk=cup_owner_id)
    cup = cup_owner.cup_set.get()
    # Event.objects.create(
    #     event_type='rebuke',
    #     user=cup_owner_id,
    #     event_performer=user_logged_in
    # )
    if cup.can_be_rebuked():
        MailSender(cup_owner).send_rebuke()
        messages.success(request, 'Wysłano maila z naganą.')
    else:
        messages.error(request, 'Wysłano już dzisiaj jedną naganę. Spróbuj jutro.')
    return redirect('cups_control:detail', cup_owner_id=cup_owner_id)


def mark_as_clean(request, cup_owner_id):
    cup_owner = get_object_or_404(CupOwner, pk=cup_owner_id)
    cup = cup_owner.cup_set.get()
    cup.reset_rebuke_count()
    messages.success(request, 'Cup marked as clean.')
    # Event.objects.create(
    #     event_type='cleaning',
    #     user=cup_owner_id,
    #     event_performer=user_logged_in
    # )
    return redirect('cups_control:detail', cup_owner_id=cup_owner_id)


def qr_code(request, cup_owner_id):
    context = dict(
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )
    return render(request, 'cups_control/detail.html', context=context)

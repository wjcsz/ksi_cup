from django.core.mail import send_mail
from cups_control.models import CupOwner, Cup

#facade
class MailSender():
    def __init__(self, cup_owner):
        self.cup_owner = cup_owner
        self.mail_address = cup_owner.mail
        self.cup = cup_owner.cup_set.get()


    def send_rebuke(self):
        subject = 'Nieumyty kubek'

        if self.cup.should_be_removed():
            message = "Drogi kołowiczu,\n dostajesz trzecią reprymendę, co oznacza konieczność usuniącia Twojego kubka oraz zostajesz zawieszony w prawach członka."
            self.cup.reset_rebuke_count()
        else:
            message = "Drogi kołowiczu,\n Twój kubek został zakwalfikowany jako nieumyty po raz {}. Proszę go niezwłocznie umyć".format(self.cup.rebukes_count)
            self.cup.increase_rebuke_count()
            self.cup.mark_as_dirty()

        send_mail(
            subject=subject,
            message=message,
            from_email='wojciech.sabala@sfi.pl',
            recipient_list=(self.mail_address,)
        )




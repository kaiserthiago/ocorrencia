from django.core.mail import send_mail
from django.template.loader import render_to_string

from ocorrencia.settings import MAIL_REPLY


class Maiable:
    def sendMail(self, from_email, to, cc, cco, subject, template, context=None):
        if context is None:
            context = {}
        html = render_to_string(template, context)
        send_mail(from_email=from_email,
                  recipient_list=(to,cc,cco),
                  subject=subject,
                  message=subject,
                  html_message=html
                  )


class RegistraOcorrenciaMail(Maiable):
    def __init__(self, ocorrencia):
        self.ocorrencia = ocorrencia

    def send(self, to, cc, cco):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            cc=cc,
            cco=cco,
            subject='SIGO - Registro de ocorrência #'+str(self.ocorrencia.id),
            template='emails/registra-ocorrencia.html',
            context={'ocorrencia': self.ocorrencia}
        )


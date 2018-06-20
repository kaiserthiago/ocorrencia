from django.core.mail import send_mail
from django.template.loader import render_to_string

from ocorrencia.settings import DEFAULT_FROM_EMAIL as MAIL_REPLY



class Maiable:
    def sendMail(self, from_email, to, subject, template, context=None):
        if context is None:
            context = {}
        html = render_to_string(template, context)
        send_mail(from_email=from_email,
                  recipient_list=(to),
                  subject=subject,
                  message=subject,
                  html_message=html
                  )


class RegistraEncaminhamentoMail(Maiable):
    def __init__(self, encaminhamento):
        self.encaminhamento = encaminhamento

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SIGO - Registro de encaminhamento #' + str(self.encaminhamento.id),
            template='emails/registra-encaminhamento.html',
            context={'encaminhamento': self.encaminhamento}
        )

class RegistraOcorrenciaMail(Maiable):
    def __init__(self, ocorrencia):
        self.ocorrencia = ocorrencia

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SIGO - Registro de ocorrência #' + str(self.ocorrencia.id),
            template='emails/registra-ocorrencia.html',
            context={'ocorrencia': self.ocorrencia}
        )


class ResponsavelUsuarioMail(Maiable):
    def __init__(self, usuario):
        self.usuario = usuario

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SIGO - Nova solicitação usuário',
            template='emails/responsavel-usuario.html',
            context={'usuario': self.usuario}
        )


class ConfirmaUsuarioMail(Maiable):
    def __init__(self, usuario):
        self.usuario = usuario

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SIGO - Acesso autorizado',
            template='emails/confirma-usuario.html',
            context={'usuario': self.usuario}
        )

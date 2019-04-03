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
            subject='SGE - Registro de encaminhamento #' + str(self.encaminhamento.id),
            template='emails/registra-encaminhamento.html',
            context={'encaminhamento': self.encaminhamento}
        )


class RegistraEncaminhamentoProvidenciasMail(Maiable):
    def __init__(self, encaminhamento):
        self.encaminhamento = encaminhamento

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Atualização de encaminhamento #' + str(self.encaminhamento.id),
            template='emails/registra-encaminhamento-providencias.html',
            context={'encaminhamento': self.encaminhamento}
        )


class RegistraOcorrenciaMail(Maiable):
    def __init__(self, ocorrencia):
        self.ocorrencia = ocorrencia

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Registro de ocorrência #' + str(self.ocorrencia.id),
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
            subject='SGE - Novo usuário cadastrado',
            template='emails/responsavel-usuario.html',
            context={'usuario': self.usuario}
        )


class RegistraUsuarioMail(Maiable):
    def __init__(self, usuario):
        self.usuario = usuario

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Confirmação de cadastro',
            template='emails/registra-usuario.html',
            context={'usuario': self.usuario}
        )


class ConfirmaUsuarioMail(Maiable):
    def __init__(self, usuario):
        self.usuario = usuario

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Acesso autorizado',
            template='emails/confirma-usuario.html',
            context={'usuario': self.usuario}
        )


class NegaUsuarioMail(Maiable):
    def __init__(self, usuario):
        self.usuario = usuario

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Acesso negado',
            template='emails/nega-usuario.html',
            context={'usuario': self.usuario}
        )


class RegistraAutorizacaoSaidaMail(Maiable):
    def __init__(self, autorizacao):
        self.autorizacao = autorizacao

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='SGE - Registro de saída - ' + str(self.autorizacao.matricula.aluno),
            template='emails/registra-saida.html',
            context={'autorizacao': self.autorizacao}
        )

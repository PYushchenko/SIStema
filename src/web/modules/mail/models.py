from django.db import models
from django.conf import settings
import django.db.migrations.writer

from polymorphic.models import PolymorphicModel
from relativefilepathfield.fields import RelativeFilePathField

from users.models import User
from schools.models import Session


class EmailUser(PolymorphicModel):
    def __str__(self):
        return str(self.get_real_instance())


class SisEmailUser(EmailUser):
    user = models.ForeignKey(User, related_name='email_user')

    @property
    def display_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def email(self):
        return self.user.email  # TODO figure out what email to return

    def __str__(self):
        return '%s %s %s' % (self.user.first_name, self.user.last_name, self.user.email)


class ExternalEmailUser(EmailUser):
    display_name = models.TextField()

    email = models.EmailField()

    def __str__(self):
        return '%s %s' % (self.display_name, self.email)


class Attachment(models.Model):
    content_type = models.CharField(max_length=100)

    original_file_name = models.TextField()  # TODO: check max length

    file_size = models.PositiveIntegerField()

    file = RelativeFilePathField(path=django.db.migrations.writer.SettingsReference(
        settings.SISTEMA_MAIL_ATTACHMENTS_DIR,
        'SISTEMA_MAIL_ATTACHMENTS_DIR'
    ), recursive=True)


class EmailMessage(models.Model):
    sender = models.ForeignKey(EmailUser, related_name='sent_emails')

    recipients = models.ManyToManyField(EmailUser, related_name='received_emails', blank=True)

    cc_recipients = models.ManyToManyField(EmailUser, related_name='cc_received_emails', blank=True)

    reply_to = models.ForeignKey(EmailUser, related_name='+', blank=True, null=True, default=None)

    subject = models.TextField(blank=True)

    html_text = models.TextField(blank=True)

    attachments = models.ManyToManyField(Attachment, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    headers = models.TextField(blank=True)


class ContactList(models.Model):
    owner = models.ForeignKey(SisEmailUser)

    def __str__(self):
        return 'List of user ' + self.owner.__str__()


class ContactRecord(models.Model):
    contact_list = models.ForeignKey(ContactList, related_name='contacts')

    person = models.ForeignKey(EmailUser)

    def __str__(self):
        return self.person.__str__()


class PersonalEmail(models.Model):
    email_name = models.CharField(max_length=100, help_text='Например, ivan-ivanov')

    hash = models.CharField(
        max_length=20,
        unique=True,
        help_text='Добавляется к email-name для идентификации пользователя'
    )

    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(SisEmailUser)

    sessions = models.ManyToManyField(Session)

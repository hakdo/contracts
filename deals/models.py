from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=128)
    orgnr = models.CharField(max_length=9, blank=True)
    active = models.BooleanField(default=True)
    trial = models.BooleanField(default=True)
    accepting_members = models.BooleanField(default=True)
    orgsecret = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)

    def __str__(self):
        return self.name + ' (Active: ' + str(self.active) + ')'

class Partner(models.Model):
    owner = models.ForeignKey(Organization, on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=255, choices=(('individual','Individual'),('company', 'Company'),('government', 'Government'),), default='company')

    def __str__(self):
        return self.name

class Contract(models.Model):
    foreign_contract_number = models.CharField(max_length=200, default="N/A")
    contract_number = models.UUIDField(_('contract_number'), primary_key=False, default=uuid.uuid4, editable=False)
    contract_party = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name=_('contract party'))
    contract_type = models.CharField(_('contract_type'), max_length=200, choices=(('employment',_('Employment')),('sales',_('Sales')),('LOI',_('Letter of intent')),('NDA',_('Non-disclosure agreement')),('partnership',_('Partnership')),('DPA',_('Data Protection Agreement')),('other',_('Other')),))
    description = models.CharField(_('description'), max_length=255)
    valid_from = models.DateField(_('valid_from'), blank=True, null=True)
    expires = models.DateField(_('expires'), blank=True, null=True)
    owner = models.CharField(_('owner'), max_length=128, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    status = models.CharField(_('status'), max_length=20, choices=(('negotiation', _('Negotiation')), ('active',_('Active')),('cancelled',_('Cancelled')),('terminated', _('Terminated')),('expired',_('Expired')),), blank=True)
    document_link = models.URLField(_('document_link'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'contract',
        verbose_name_plural = 'contracts'

    def __str__(self):
        return self.contract_party.name + ': ' + self.contract_type + ' (' + self.status + ')'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + ' (PROFILE)'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
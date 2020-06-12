from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    contract_number = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    contract_party = models.ForeignKey(Partner, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=200, choices=(('employment','Employment'),('sales','Sales'),('LOI','Letter of intent'),('NDA','Non-disclosure agreement'),('partnership','Partnership'),('DPA','Data Protection Agreement'),('other','Other'),))
    description = models.CharField(max_length=255)
    valid_from = models.DateField(blank=True, null=True)
    expires = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=(('negotiation', 'Negotiation'), ('active','Active'),('cancelled','Cancelled'),('terminated', 'Terminated'),('expired','Expired'),), blank=True)
    document_link = models.URLField(max_length=255, null=True, blank=True)

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
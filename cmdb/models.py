from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.db.models import Model, TextChoices
from django.db.models import CharField, PositiveIntegerField, TextField, DateField, URLField, EmailField, BooleanField, DateTimeField
from django.db.models import ForeignKey, CASCADE, PROTECT, RESTRICT, SET, SET_NULL, SET_DEFAULT, DO_NOTHING
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
class Usuario(AbstractUser):
    username = CharField(_('username'), max_length=150, unique=True)
    password = CharField(_('password'), max_length=128, null=True, blank=True)
    name = CharField(_('name'), max_length=255, null=True, blank=True)
    social_name = CharField(_('social name'), max_length=255, null=True, blank=True)
    email = EmailField(_('email address'), null=True, blank=True)
    scholar_email = EmailField(_('scholar email address'), null=True, blank=True)
    academic_email = EmailField(_('academic email address'), null=True, blank=True)
    campus = CharField(_('campus'), max_length=255, null=True, blank=True)
    is_staff = BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'),)
    is_active = BooleanField(_('active'), default=True, help_text=_( 'Designates whether this user should be treated as active. ' 'Unselect this instead of deleting accounts.'),)
    created_at = DateTimeField(_('date created'), auto_now_add=True)
    changed_at = DateTimeField(_('date changed'), auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['name']

    def __str__(self):
        return f'{self.name}' 
    pass


class StringField(CharField):
    def __init__(self, verbose_name, max_length=250, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, *args, **kwargs)


class NullStringField(StringField):
    def __init__(self, verbose_name, max_length=250, null=True, blank=True, *args, **kwargs):
        super().__init__(verbose_name=verbose_name, max_length=max_length, null=True, blank=True, *args, **kwargs)


class FK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE, 
                 related_name=None, related_query_name=None, limit_choices_to=None, 
                 parent_link=False, to_field=None, db_constraint=True, **kwargs):
        super().__init__(to, on_delete, related_name, related_query_name, 
                         limit_choices_to, parent_link, to_field, db_constraint, verbose_name=verbose_name, **kwargs)


class NullFK(ForeignKey):
    def __init__(self, verbose_name, to, on_delete=CASCADE,  
                 related_name=None, related_query_name=None, limit_choices_to=None, 
                 parent_link=False, to_field=None, db_constraint=True, null=True, blank=True,**kwargs):
        super().__init__(to, on_delete, related_name, related_query_name, 
                         limit_choices_to, parent_link, to_field, db_constraint, verbose_name=verbose_name, null=null, blank=blank, **kwargs)


class Service(Model):
    name = StringField(_("Name"))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return "%s" % self.name


class OperationSystemFamily(Model):
    name = StringField(_("Name"))

    class Meta:
        verbose_name = _('Operation system family')
        verbose_name_plural = _('Operation system families')

    def __str__(self):
        return "%s" % self.name


class OperationSystem(Model):
    name = StringField(_("Name"))
    family = FK(_("Family"), OperationSystemFamily)
    end_of_life = DateField(_("End of life"), null=True, blank=True)

    class Meta:
        verbose_name = _('Operation system')
        verbose_name_plural = _('Operation systems')

    def __str__(self):
        return "%s (%s)" % (self.name, self.family)


class OperationSystemVersion(Model):
    version = StringField(_("Name"))
    operation_system = FK(_("Operation system"), OperationSystem)

    class Meta:
        verbose_name = _('Operation system version')
        verbose_name_plural = _('Operation system versions')

    def __str__(self):
        return "%s (%s)" % (self.operation_system, self.version)


class AssetKind(Model):
    name = StringField(_("Name"))

    class Meta:
        verbose_name = _('Asset kind')
        verbose_name_plural = _('Assets kind')

    def __str__(self):
        return "%s" % self.name


class Machine(Model):
    class Kind(TextChoices):
        PHYSICAL = 'Physical', _('Physical')
        VIRTUAL = 'Virtual', _('Virtual')

    kind = StringField(_("Kind"), choices=Kind.choices, default=Kind.VIRTUAL,)
    name = StringField(_("Name"))
    url = URLField(_("URL"))
    serial = NullStringField(_("Service tag or serial"))
    license = NullStringField(_("Key or license"))
    patrimony = NullStringField(_("Patrimony ID"))
    purpose = StringField(_("Purpose"))
    cpu = PositiveIntegerField(_("CPU"))
    ram = PositiveIntegerField(_("RAM in GB"))
    physical_machine = NullFK(_("Physical machine"), 'Machine')
    operation_system_version = FK(_("Operation system version"), OperationSystemVersion)
    last_operation_system_upgrade = DateField(_("Last operation system upgrade"), null=True, blank=True)
    comments = TextField(_("Comments"), null=True, blank=True)

    class Meta:
        verbose_name = _('Machine')
        verbose_name_plural = _('Machines')

    def __str__(self):
        return "%s" % self.name


class ExecutedCommands(Model):
    machine = NullFK(_("Machine"), Machine)
    commands = TextField(_("Commands"))
    date = DateField(_("Date"))

    class Meta:
        verbose_name = _('Executed commands')
        verbose_name_plural = _('Executed commands')

    def __str__(self):
        return _("%s at %s") % (self.machine, self.date)


class ConfiguredAsset(Model):
    machine = FK(_("Machine"), Machine)
    asset = FK(_("Asset"), AssetKind)
    comments = TextField(_("Comments"), null=True, blank=True)

    class Meta:
        verbose_name = _('Configured asset')
        verbose_name_plural = _('Configured assets')

    def __str__(self):
        return _("%s at %s") % (self.machine, self.asset)


class Credential(Model):
    class Kind(TextChoices):
        LOCAL = 'Local', _('Local')
        SERVICE = 'Service', _('Service')
        LDAP = 'LDAP', _('LDAP')
    machine = FK(_("Machine"), Machine)
    kind = StringField(_("Kind"), choices=Kind.choices, default=Kind.LOCAL,)
    username = StringField(_("Username"))
    password = StringField(_("Password"))

    class Meta:
        verbose_name = _('Credential')
        verbose_name_plural = _('Credentials')

    def __str__(self):
        return "%s (%s)" % (self.username, self.kind)

        
class Storage(Model):
    class Kind(TextChoices):
        SSD = 'SSD', _('SSD')
        HD = 'HD', _('HD')
        VHD = 'VHD', _('VHD')
    machine = FK(_("Machine"), Machine)
    kind = StringField(_("Kind"), choices=Kind.choices, default=Kind.VHD,)
    capacity = PositiveIntegerField(_("Capacity (in GB)"))

    class Meta:
        verbose_name = _('Storage')
        verbose_name_plural = _('Storages')

    def __str__(self):
        return "%s: %s" % (self.kind, self.capacity)

        
class NetworkInterface(Model):
    machine = FK(_("Machine"), Machine)
    purpose = NullStringField(_("Purpose"))
    interface_name = NullStringField(_("Interface name"))
    interface_number = PositiveIntegerField(_("Interface number"), null=True, blank=True)
    ipv4_address = NullStringField(_("IPv4 address"))
    ipv4_mask = NullStringField(_("IPv4 mask"))
    ipv6_address = NullStringField(_("IPv6 address"))
    switch_port = NullStringField(_("Switch port"))
    pvid = NullStringField(_("PVID"))
    untag = NullStringField(_("Untag"))
    tag = NullStringField(_("Tag"))
    service = NullFK(_("Service"), Service)

    class Meta:
        verbose_name = _('Network interface')
        verbose_name_plural = _('Network interfaces')

    def __str__(self):
        return "%s: %s/%s" % (self.purpose, self.ipv4_address, self.ipv4_mask)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_socialauth_suap_user(sender, instance=None, created=False, **kwargs):
    from social_django.models import UserSocialAuth
    UserSocialAuth.objects.update_or_create(user=instance, defaults={'provider': 'suap', 'uid': instance.username})

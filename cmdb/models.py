from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.db.models import Model, TextChoices
from django.db.models import CharField, TextField, DateField, BooleanField, DateTimeField
from django.db.models import PositiveIntegerField, PositiveSmallIntegerField
from django.db.models import URLField, EmailField, IPAddressField, GenericIPAddressField, ImageField
from django.db.models import ForeignKey, CASCADE, PROTECT, RESTRICT, SET, SET_NULL, SET_DEFAULT, DO_NOTHING, ManyToManyField
from django.contrib.auth.models import AbstractUser
from markdownx.models import MarkdownxField
from .fields import StringField, NullStringField, FK, NullFK


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


class Contact(Model):
    class Kind(TextChoices):
        MANAGER = 'Manager', _('Manager')
        TECHNICIAN = 'Technician', _('Technician')
        CLIENT = 'Client', _('Client')
        KEY_USER = 'Key user', _('Key user')

    kind = StringField(_("Kind"), choices=Kind.choices, default=Kind.MANAGER,)
    name = CharField('Nome', max_length=250)
    comments = MarkdownxField(_('Comments'), null=True, blank=True)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return f"{self.name} ({self.kind})"


class Channel(Model):
    class Kind(TextChoices):
        PERSONAL_EMAIL = 'Personal e-Mail', _('Personal e-Mail')
        ENTERPRISE_EMAIL = 'Enterprise e-Mail', _('Enterprise e-Mail')
        WHATSAPP = 'WhatsApp', _('WhatsApp')
        PERSONAL_PHONE = 'Personal phone', _('Personal phone')
        ENTERPRISE_PHONE = 'Enterprise phone', _('Enterprise phone')

    Contact = ForeignKey(_('Contact'), Contact)
    kind = StringField(_("Kind"), choices=Kind.choices, default=Kind.ENTERPRISE_EMAIL,)
    content = StringField(_('Content'), max_length=250)
    comments = MarkdownxField(_('Comments'), null=True, blank=True)

    class Meta:
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        return f"{self.kind} - {self.content}"


class ServiceGroup(Model):
    name = StringField(_("Name"))
    comments = MarkdownxField(_("Comments"), null=True, blank=True)

    class Meta:
        verbose_name = _('Service group')
        verbose_name_plural = _('Services groups')

    def __str__(self):
        return "%s" % self.name


class Service(Model):
    name = StringField(_("Name"))
    service_group = FK(_("Service group"), ServiceGroup)
    contacts = ManyToManyField(Contact)
    comments = MarkdownxField(_('Comments'), null=True, blank=True)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return "%s" % self.name

        
class VisualTest(Model):
    service = FK(_('Service'), Service)
    name = StringField(_('Name'))
    url = URLField(_('URL'))
    screenshot = ImageField(_('Screenshot'), upload_to='visual')
    order = PositiveSmallIntegerField(_('Order'), default=1)
    how_to_test = MarkdownxField('How to test', null=False, blank=False)

    class Meta:
        verbose_name = _('Visual test')
        verbose_name_plural = _('Visual tests')

    def __str__(self):
        return self.name


class AutomatedTest(Model):
    service = FK(_('Service'), Service)
    url = URLField(_('URL'))
    http_code = PositiveSmallIntegerField(_('HTTP Code'), default=200)
    regex = CharField(_('RegEx'), max_length=250, null=True, blank=True)
    timeout = PositiveSmallIntegerField(_('Timeout (s)'))
    interval = PositiveSmallIntegerField(_('Intervalo (m)'))
    order = PositiveSmallIntegerField(_('Order'), default=1)
    comments = MarkdownxField(_('Comments'), null=True, blank=True)

    class Meta:
        verbose_name = _('Automated test')
        verbose_name_plural = _('Automated tests')

    def __str__(self):
        return self.url

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
    comments = MarkdownxField(_("Comments"), null=True, blank=True)

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
    url = URLField(_("URL"), null=True, blank=True)
    serial = NullStringField(_("Service tag or serial"))
    license = NullStringField(_("Key or license"))
    patrimony = NullStringField(_("Patrimony ID"))
    purpose = StringField(_("Purpose"))
    cpu = PositiveIntegerField(_("CPU"))
    ram = PositiveIntegerField(_("RAM in GB"))
    physical_machine = NullFK(_("Physical machine"), 'Machine')
    operation_system_version = FK(_("Operation system version"), OperationSystemVersion)
    last_operation_system_upgrade = DateField(_("Last operation system upgrade"), null=True, blank=True)
    comments = MarkdownxField(_("Comments"), null=True, blank=True)

    class Meta:
        verbose_name = _('Machine')
        verbose_name_plural = _('Machines')

    def __str__(self):
        return "%s" % self.name


class ExecutedCommands(Model):
    machine = NullFK(_("Machine"), Machine)
    subject = StringField(_("Subject"))
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
    comments = MarkdownxField(_("Comments"), null=True, blank=True)

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
    mount_point = StringField(_("Mount point"))

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
    ipv4_address = GenericIPAddressField(_("IPv4 address"), protocol='IPv4', null=True, blank=True)
    ipv4_mask = NullStringField(_("IPv4 mask"))
    ipv6_address = GenericIPAddressField(_("IPv6 address"), protocol='IPv6', null=True, blank=True)
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

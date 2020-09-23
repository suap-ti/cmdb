from django.utils.translation import gettext as _
from django.db.models import TextField
from django.forms.widgets import Textarea
from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from tabbed_admin import TabbedModelAdmin
from markdownx.models import MarkdownxField
from markdownx.widgets import MarkdownxWidget
from .models import Usuario
from .models import Contact, Channel, ServiceGroup, Service, VisualTest, AutomatedTest
from .models import OperationSystemFamily, OperationSystem, OperationSystemVersion, AssetKind
from .models import Machine, ExecutedCommands, ConfiguredAsset, Credential, Storage, NetworkInterface


class ChannelInline(TabularInline):
    model = Channel
    fields = ['kind', 'content', 'comments']
    extra = 0


@register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'comments']
    inlines = [ChannelInline]
   

@register(ServiceGroup)
class ServiceGroupAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'comments']


class VisualTestInline(StackedInline):
    model = VisualTest
    fields = ['order', 'name', 'url', 'screenshot', 'how_to_test']
    ordering = ['order']
    extra = 0


class AutomatedTestInline(StackedInline):
    model = AutomatedTest
    fields = ['order', 'url', 'http_code', 'regex', 'timeout', 'interval', 'comments']
    ordering = ['order']
    extra = 0


@register(Service)
class ServiceAdmin(TabbedModelAdmin):
    list_display = ['name', 'service_group']
    search_fields = ['name', 'comments']
    list_filter = ['service_group']
    autocomplete_fields = ['contacts']
    tabs = [
        ( _('Identification'), ((None, {'fields': ['name', 'contacts', 'comments',]}),) ),
        ( _('Visual test'), (VisualTestInline,) ),
        ( _('Automated test'), (AutomatedTestInline,) ),
    ]


@register(OperationSystemFamily)
class OperationSystemFamilyAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class OperationSystemVersionInline(TabularInline):
    model = OperationSystemVersion
    fields = ['version']
    ordering = ['version']
    extra = 0
    

@register(OperationSystem)
class OperationSystemAdmin(ModelAdmin):
    list_display = ['name', 'family', 'end_of_life']
    search_fields = ['name']
    list_filter = ['family']
    inlines = [OperationSystemVersionInline]


@register(AssetKind)
class AssetKindAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ExecutedCommandsInline(StackedInline):
    model = ExecutedCommands
    fields = ['date', 'commands']
    ordering = ['date', 'id']
    extra = 0
    formfield_overrides = {TextField: {'widget': Textarea(attrs={'class': "vLargeTextField", 'style':"font-family: monospace; background: #333; color: lime;"})}}
    # cols="40" rows="10" style="background: red;" id="id_executedcommands_set-0-commands"
    # cols="40" rows="10" class="vLargeTextField" id="id_executedcommands_set-0-commands"



class ConfiguredAssetInline(TabularInline):
    model = ConfiguredAsset
    fields = ['asset', 'comments']
    ordering = ['asset']
    extra = 0


class CredentialInline(TabularInline):
    model = Credential
    fields = ['kind', 'username', 'password']
    ordering = ['kind', 'username']
    extra = 0


class StorageInline(TabularInline):
    model = Storage
    fields = ['kind', 'capacity', 'mount_point']
    ordering = ['kind', 'capacity']
    extra = 0


class NetworkInterfaceInline(StackedInline):
    model = NetworkInterface
    fields = ['purpose', 'service', 'interface_name', 'interface_number', 'ipv4_address', 'ipv4_mask', 'ipv6_address', 'switch_port', 'pvid', 'untag', 'tag']
    extra = 0


@register(Machine)
class MachineAdmin(TabbedModelAdmin):
    list_display = ['name', 'kind', 'purpose', 'last_operation_system_upgrade']
    search_fields = ['name', 'url', 'patrimony', 'purpose', 'comments']
    list_filter = ['kind', 'physical_machine', 'operation_system_version']
    date_hierarchy = 'last_operation_system_upgrade'
    tabs = [
        ( 
            _('Overview'),
            ( 
                (
                    None,
                    {'fields':
                        (
                            ('kind', 'operation_system_version', 'last_operation_system_upgrade', ), 
                            ('name', 'physical_machine',), 
                            ('purpose', 'url'), 
                            ('cpu', 'ram'), 
                        )
                    }
                ),
                StorageInline
            )
        ),
        ( _('Network'), (NetworkInterfaceInline,) ),
        ( _('Credentials'), (CredentialInline,) ),
        ( _('Assets'), (ConfiguredAssetInline,) ),
        ( _('Commands'), (ExecutedCommandsInline,) ),
        ( _('Licenses'), ((None, {'fields': ('serial', 'license', 'patrimony')}),) ),
        ( _('Comments'), ((None, { 'fields': ('comments', ) }),) ),
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "physical_machine":
            kwargs["queryset"] = Machine.objects.filter(kind=Machine.Kind.PHYSICAL)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@register(Usuario)
class UsuarioAdmin(TabbedModelAdmin):
    list_display = ('username', 'name', 'email', 'campus', 'grupos',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups',) 
    search_fields = ('username', 'name', 'email')
    ordering = ('name',)

    readonly_fields = ['created_at', 'changed_at', ]
    tabs = [
        (None, ((None, {'fields': [('username', 'campus'), ('name', 'social_name'), ('created_at', 'changed_at',),]}),) ),
        (_('E-Mails'), ((None, {'fields': ['email', 'academic_email', 'scholar_email',]}),) ),
        ( _('Permissions'), ((None, {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups',]}),) ),
    ]

    def grupos(self, instance):
        result = ', '.join([x.name for x in instance.groups.all()])
        return f'{result}'

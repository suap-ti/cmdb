from django.utils.translation import gettext as _
from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from .models import Usuario
from .models import Service, OperationSystemFamily, OperationSystem, OperationSystemVersion, AssetKind
from .models import Machine, ExecutedCommands, ConfiguredAsset, Credential, Storage, NetworkInterface
from tabbed_admin import TabbedModelAdmin


@register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


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
    ordering = ['date']
    extra = 0


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
    fields = ['kind', 'capacity']
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

    tab_overview = (
        (None, {'fields': (
                ('kind', 'operation_system_version', 'last_operation_system_upgrade', ), 
                ('name', 'physical_machine',), 
                ('purpose', 'url'), 
                ('cpu', 'ram'), 
            )}),
        StorageInline
    )

    tabs = [
        ( _('Overview'), tab_overview ),
        ( _('Licenses'), ((None, {'fields': ('serial', 'license', 'patrimony')}),) ),
        ( _('Network'), (NetworkInterfaceInline,) ),
        ( _('Credentials'), (CredentialInline,) ),
        ( _('Assets'), (ConfiguredAssetInline,) ),
        ( _('Commands'), (ExecutedCommandsInline,) ),
        ( _('Comments'), ((None, { 'fields': ('comments', ) }),) ),
    ]

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

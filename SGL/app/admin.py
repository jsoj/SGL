# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db.models import Q
from app.models import ( Tecnologia, Cultivo, Marcador, Projeto, Status, 
                        Protocolo, Etapa, User,  Amostra, Placa96, 
                        Placa384, Placa1536, Empresa,  Poco96, Poco384, Poco1536,    
                        PlacaMap384, PlacaMap1536, Resultado)

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'empresa', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups', 'empresa')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'telefone', 'empresa')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'empresa'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "empresa" and not request.user.is_superuser:
            kwargs["queryset"] = Empresa.objects.filter(id=request.user.empresa.id)
            kwargs["initial"] = request.user.empresa
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'cnpj', 'is_active', 'data_cadastro')
    list_filter = ('is_active',)
    search_fields = ('nome', 'codigo', 'cnpj')
    ordering = ('nome',)
    
    fieldsets = (
        (None, {'fields': ('nome', 'codigo', 'cnpj', 'is_active')}),
        ('Informações de Contato', {'fields': ('email', 'telefone')}),
        ('Endereço', {'fields': ('cep', 'endereco', 'complemento', 'bairro', 'cidade', 'estado')}),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Apenas superuser pode deletar empresas
        return request.user.is_superuser

class EmpresaAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.empresa:
            return qs.filter(empresa=request.user.empresa)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.empresa and not request.user.is_superuser:
            obj.empresa = request.user.empresa
        super().save_model(request, obj, form, change)

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request) or [])
        if request.user.is_superuser:
            if 'empresa' not in list_filter:
                list_filter.append('empresa')
        return list_filter

@admin.register(Projeto)
class ProjetoAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('codigo_projeto', 'empresa', 'status', 'cultivo', 'created_at')
    list_filter = ('empresa', 'status', 'cultivo')  # Empresa primeiro para facilitar filtragem
    search_fields = ('codigo_projeto', 'nome_projeto_cliente', 'empresa__nome')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.select_related('empresa', 'status', 'cultivo')
        if request.user.empresa:
            return qs.filter(empresa=request.user.empresa).select_related('empresa', 'status', 'cultivo')
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "empresa":
                kwargs["queryset"] = Empresa.objects.filter(id=request.user.empresa.id)
                kwargs["initial"] = request.user.empresa
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class Poco96Inline(admin.TabularInline):
    model = Poco96
    extra = 1
    autocomplete_fields = ['amostra']

class Poco384Inline(admin.TabularInline):
    model = Poco384
    extra = 1
    autocomplete_fields = ['amostra']

class Poco1536Inline(admin.TabularInline):
    model = Poco1536
    extra = 1
    autocomplete_fields = ['amostra']

class PlacaMap384Inline(admin.TabularInline):
    model = PlacaMap384
    extra = 1
    autocomplete_fields = ['placa_origem']

class PlacaMap1536Inline(admin.TabularInline):
    model = PlacaMap1536
    extra = 1
    autocomplete_fields = ['placa_origem']

@admin.register(Amostra)
class AmostraAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('empresa', 'empresa__nome','projeto','codigo_amostra',  'data_cadastro')
    list_filter = ('projeto', 'empresa', 'data_cadastro')
    search_fields = ('codigo_amostra', 'projeto__codigo_projeto')
    autocomplete_fields = ['projeto']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('projeto', 'empresa')

@admin.register(Placa96)
class Placa96Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('codigo_placa', 'projeto', 'empresa','empresa__nome', 'data_criacao', 'get_amostras_count', 'is_active')
    list_filter = ('projeto', 'empresa', 'data_criacao', 'is_active')
    search_fields = ('codigo_placa', 'projeto__codigo_projeto')
    inlines = [Poco96Inline]
    autocomplete_fields = ['projeto']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('projeto', 'empresa')

@admin.register(Placa384)
class Placa384Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('codigo_placa', 'projeto', 'empresa', 'data_criacao', 'get_amostras_count', 'is_active')
    list_filter = ('projeto', 'empresa', 'data_criacao', 'is_active')
    search_fields = ('codigo_placa', 'projeto__codigo_projeto')
    inlines = [Poco384Inline, PlacaMap384Inline]
    autocomplete_fields = ['projeto']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('projeto', 'empresa')

@admin.register(Placa1536)
class Placa1536Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('codigo_placa', 'projeto', 'empresa', 'data_criacao', 'get_amostras_count', 'is_active')
    list_filter = ('projeto', 'empresa', 'data_criacao', 'is_active')
    search_fields = ('codigo_placa', 'projeto__codigo_projeto')
    inlines = [Poco1536Inline, PlacaMap1536Inline]
    autocomplete_fields = ['projeto']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('projeto', 'empresa')

@admin.register(PlacaMap384)
class PlacaMap384Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('placa_origem', 'placa_destino', 'quadrante', 'empresa')
    list_filter = ('placa_destino__projeto', 'empresa', 'quadrante')
    search_fields = ('placa_origem__codigo_placa', 'placa_destino__codigo_placa')
    autocomplete_fields = ['placa_origem', 'placa_destino']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'placa_origem', 'placa_destino', 'empresa'
        )

@admin.register(PlacaMap1536)
class PlacaMap1536Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('placa_origem', 'placa_destino', 'quadrante', 'empresa')
    list_filter = ('placa_destino__projeto', 'empresa', 'quadrante')
    search_fields = ('placa_origem__codigo_placa', 'placa_destino__codigo_placa')
    autocomplete_fields = ['placa_origem', 'placa_destino']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'placa_origem', 'placa_destino', 'empresa'
        )

@admin.register(Resultado)
class ResultadoAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('amostra', 'get_poco_display', 'valor', 'empresa', 'data_resultado')
    list_filter = ('amostra__projeto', 'empresa', 'data_resultado')
    search_fields = (
        'amostra__codigo_amostra',
        'poco_96__placa__codigo_placa',
        'poco_384__placa__codigo_placa',
        'poco_1536__placa__codigo_placa'
    )
    autocomplete_fields = ['amostra', 'poco_96', 'poco_384', 'poco_1536']
    
    def get_poco_display(self, obj):
        if obj.poco_96:
            return f"P96: {obj.poco_96}"
        elif obj.poco_384:
            return f"P384: {obj.poco_384}"
        elif obj.poco_1536:
            return f"P1536: {obj.poco_1536}"
        return "-"
    get_poco_display.short_description = "Poço"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'amostra', 'poco_96', 'poco_384', 'poco_1536', 
            'empresa', 'amostra__projeto'
        )

# Registrar os modelos Poco individualmente caso precise de acesso direto
@admin.register(Poco96)
class Poco96Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('empresa__nome', 'placa__projeto', 'placa', 'posicao', 'amostra',)
    list_filter = ('placa__projeto', 'empresa', 'placa')
    search_fields = ('placa__codigo_placa', 'posicao', 'amostra__codigo_amostra')
    autocomplete_fields = ['placa', 'amostra']

@admin.register(Poco384)
class Poco384Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('placa', 'posicao', 'amostra', 'empresa')
    list_filter = ('placa__projeto', 'empresa')
    search_fields = ('placa__codigo_placa', 'posicao', 'amostra__codigo_amostra')
    autocomplete_fields = ['placa', 'amostra']

@admin.register(Poco1536)
class Poco1536Admin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('placa', 'posicao', 'amostra', 'empresa')
    list_filter = ('placa__projeto', 'empresa')
    search_fields = ('placa__codigo_placa', 'posicao', 'amostra__codigo_amostra')
    autocomplete_fields = ['placa', 'amostra']

@admin.register(Tecnologia)
class TecnologiaAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome', 'caracteristica', 'vencimento_patente', 'data_cadastro')
    search_fields = ('nome',)

@admin.register(Cultivo)
class CultivoAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome', 'nome_cientifico', 'data_cadastro')
    search_fields = ('nome',)

@admin.register(Marcador)
class MarcadorAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome', 'cultivo', 'is_customizado')
    search_fields = ('nome',)

@admin.register(Status)
class StatusAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Protocolo)
class ProtocoloAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Etapa)
class EtapaAdmin(EmpresaAdminMixin, admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Manter apenas este registro do User
admin.site.register(User, CustomUserAdmin)
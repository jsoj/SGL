# Generated by Django 5.1.5 on 2025-03-12 20:36

import app.funcoes
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=5)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('endereco', models.CharField(blank=True, max_length=100, null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=2, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Cultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('nome_cientifico', models.CharField(blank=True, max_length=40, null=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Cultivos',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuarios', to='app.empresa')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Etapas',
            },
        ),
        migrations.CreateModel(
            name='Marcador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('caracteristica', models.TextField(blank=True, null=True)),
                ('is_customizado', models.BooleanField(default=False)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('cultivo', models.ForeignKey(help_text='Escolha ou cadastre um cultivo para este marcador. Exemplo: Soja', on_delete=django.db.models.deletion.CASCADE, to='app.cultivo')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Marcadores',
            },
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_projeto', models.CharField(help_text='Código do projeto são 5 números sequenciais e únicos para o cliente. Exemplo: 00001', max_length=5)),
                ('quantidade_amostras', models.PositiveIntegerField(help_text='Quantidade de amostras deste projeto. Exemplo: 15.000')),
                ('origem_amostra', models.CharField(blank=True, choices=[('FOLHA', 'FOLHA'), ('SEMENTE', 'SEMENTE')], default=1, help_text='Origem da amostra no cliente. Exemplo: Planta, Linha, Semente', max_length=10)),
                ('quantidade_traits', models.PositiveSmallIntegerField(blank=True, help_text='Quantidade de traits a serem avaliados neste projeto. Exemplo: 1, 2', null=True)),
                ('quantidade_marcador_customizado', models.PositiveSmallIntegerField(blank=True, help_text='Quantidade de marcadores customizados a serem analisados neste projeto. Exmmplo: 2', null=True)),
                ('nome_projeto_cliente', models.CharField(blank=True, help_text='Nome de guerra do projeto. Exemplo: RV_CZF4_MULTIPGN_1x3_02_01', max_length=100, null=True)),
                ('numero_placas_96', models.PositiveSmallIntegerField(blank=True, help_text='O número de Placas de 96 será calculado automaticamente com base no número de amostras', null=True)),
                ('placas_inicial', models.CharField(blank=True, help_text='Placa inicial. Exemplo: 1', max_length=10, null=True)),
                ('placas_final', models.CharField(blank=True, help_text='Placa final. Exemplo: 96', max_length=10)),
                ('responsavel', models.CharField(blank=True, help_text='Nome do responsável pelo projeto no cliente. Exemplo: Osmaria', max_length=100)),
                ('prioridade', models.PositiveSmallIntegerField(default=0, help_text='Prioridade do projeto. Exemplo: 01 prioridade máxima, 09 baixa prioridade')),
                ('codigo_ensaio', models.CharField(blank=True, help_text='Código de ensaio do cliente. Exemplo: 51899137 ', max_length=10)),
                ('setor_cliente', models.CharField(blank=True, help_text='Setor interno do cliente. Exemplo: Nursery, Pureza, Produção, QAQC', max_length=40)),
                ('local_cliente', models.CharField(blank=True, help_text='Local de referência do cliente. Exemplo: Porto Nacional, Rio Verde', max_length=40)),
                ('ano_plantio_ensaio', models.IntegerField(blank=True, help_text='Ano do plantio com 4 dígitos. Exemplo: 2024', null=True)),
                ('numero_discos', models.CharField(blank=True, help_text='Números de discos. Exemplo: TRIFÓLIO #4 PUNCHS ou TRIFÓLIO #8 PUNCHS', max_length=40)),
                ('data_planejada_envio', models.DateField(blank=True, null=True)),
                ('data_envio', models.DateField(blank=True, null=True)),
                ('data_planejada_liberacao_resultados', models.DateField(blank=True, null=True)),
                ('data_recebimento_laboratorio', models.DateField(blank=True, null=True, validators=[app.funcoes.validar_data_recebimento])),
                ('data_liberacao_resultados', models.DateField(blank=True, null=True, validators=[app.funcoes.validar_data_liberacao])),
                ('data_validacao_cliente', models.DateField(blank=True, null=True)),
                ('data_prevista_destruicao', models.DateField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('data_alteracao', models.DateField(auto_now=True)),
                ('tem_template', models.BooleanField(default=False)),
                ('ativo', models.BooleanField(default=True)),
                ('destruido', models.BooleanField(default=False)),
                ('data_destruicao', models.DateField(auto_now=True)),
                ('comentarios', models.TextField(blank=True, help_text='Registre toda e qualquer informação acessória para este projeto', null=True)),
                ('cultivo', models.ForeignKey(blank=True, default=1, help_text='Escolha ou cadastre um cultivo. Exemplo: Soja', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cultivo')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('etapa', models.ForeignKey(blank=True, default=1, help_text='Escolha a estapa da amostra do projeto', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.etapa')),
                ('marcador', models.ManyToManyField(blank=True, help_text='Escolha ou cadastre os marcadores que serão analisados neste projeto. Exemplo: RR2BT1, E3BT, RGH1-2', to='app.marcador')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
            },
        ),
        migrations.CreateModel(
            name='Placa96',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_placa', models.CharField(help_text='Código identificador da placa de 96 poços', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Placa   96',
                'verbose_name_plural': 'Placas   96',
                'unique_together': {('empresa', 'projeto', 'codigo_placa')},
            },
        ),
        migrations.CreateModel(
            name='Placa384',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_placa', models.CharField(help_text='Código identificador da placa de 384 poços', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Placa  384',
                'verbose_name_plural': 'Placas  384',
                'unique_together': {('empresa', 'projeto', 'codigo_placa')},
            },
        ),
        migrations.CreateModel(
            name='Placa1536',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_placa', models.CharField(help_text='Código identificador da placa de 1536 poços', max_length=30)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Placa 1536',
                'verbose_name_plural': 'Placas 1536',
                'unique_together': {('empresa', 'projeto', 'codigo_placa')},
            },
        ),
        migrations.CreateModel(
            name='Amostra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_amostra', models.CharField(db_index=True, help_text='Código único da amostra no projeto', max_length=50)),
                ('barcode_cliente', models.CharField(blank=True, help_text='Código único da amostra no projeto controle do cliente', max_length=50, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Amostra',
                'verbose_name_plural': 'Amostras',
            },
        ),
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Protocolos',
            },
        ),
        migrations.AddField(
            model_name='projeto',
            name='protocolo',
            field=models.ForeignKey(blank=True, default=1, help_text='Escolha o protocolo ex. PCR em tempo real, microsatelites', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.protocolo'),
        ),
        migrations.CreateModel(
            name='ResultadoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='resultados/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('processado', models.BooleanField(default=False)),
                ('marcador_fh', models.CharField(blank=True, help_text='Identificador do marcador FH usado no experimento', max_length=50, null=True)),
                ('marcador_aj', models.CharField(blank=True, help_text='Identificador do marcador AJ usado no experimento', max_length=50, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa_1536', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa1536')),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.projeto')),
            ],
            options={
                'verbose_name': 'Upload de Resultado',
                'verbose_name_plural': 'Uploads de Resultados',
                'ordering': ['-data_upload'],
            },
        ),
        migrations.CreateModel(
            name='ResultadoAmostra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_processamento', models.DateTimeField(auto_now_add=True)),
                ('resultado_fh', models.CharField(blank=True, max_length=20, null=True)),
                ('coordenada_x_fh', models.FloatField(blank=True, null=True)),
                ('coordenada_y_fh', models.FloatField(blank=True, null=True)),
                ('resultado_aj', models.CharField(blank=True, max_length=20, null=True)),
                ('coordenada_x_aj', models.FloatField(blank=True, null=True)),
                ('coordenada_y_aj', models.FloatField(blank=True, null=True)),
                ('dados_adicionais', models.JSONField(blank=True, null=True)),
                ('amostra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.amostra')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.resultadoupload')),
            ],
            options={
                'verbose_name': 'Resultado por Amostra',
                'verbose_name_plural': 'Resultados por Amostra',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.AddField(
            model_name='projeto',
            name='status',
            field=models.ForeignKey(blank=True, default=1, help_text='Escolha o status do projeto', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.status'),
        ),
        migrations.CreateModel(
            name='Tecnologia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('caracteristica', models.TextField(blank=True, max_length=100)),
                ('vencimento_patente', models.DateField(blank=True, null=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
            ],
            options={
                'verbose_name_plural': 'Tecnologias',
            },
        ),
        migrations.AddField(
            model_name='projeto',
            name='tecnologia',
            field=models.ForeignKey(blank=True, help_text='Escolha ou cadastre um evento biotecnológico deste projeto. Exemplo: RR, CE3, I2X', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tecnologia'),
        ),
        migrations.CreateModel(
            name='PlacaMap1536',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quadrante', models.IntegerField(choices=[(1, 'Quadrante 1'), (2, 'Quadrante 2'), (3, 'Quadrante 3'), (4, 'Quadrante 4')], help_text='Quadrante da placa 1536 (1-4)')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa1536')),
                ('placa_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa384')),
            ],
            options={
                'verbose_name': 'Mapeamento 384->1536',
                'verbose_name_plural': 'Mapeamentos 384->1536',
                'unique_together': {('placa_destino', 'quadrante'), ('placa_origem', 'placa_destino')},
            },
        ),
        migrations.CreateModel(
            name='PlacaMap384',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quadrante', models.IntegerField(choices=[(1, 'Quadrante 1'), (2, 'Quadrante 2'), (3, 'Quadrante 3'), (4, 'Quadrante 4')], help_text='Quadrante da placa 384 (1-4)')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa384')),
                ('placa_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa96')),
            ],
            options={
                'verbose_name': 'Mapeamento 96->384',
                'verbose_name_plural': 'Mapeamentos 96->384',
                'unique_together': {('placa_destino', 'quadrante'), ('placa_origem', 'placa_destino')},
            },
        ),
        migrations.CreateModel(
            name='PlacaMap384to384',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_transferencia', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino_maps', to='app.placa384')),
                ('placa_origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origem_maps', to='app.placa384')),
            ],
            options={
                'verbose_name': 'Mapeamento 384->384',
                'verbose_name_plural': 'Mapeamentos 384->384',
                'unique_together': {('empresa', 'placa_destino'), ('placa_origem', 'placa_destino')},
            },
        ),
        migrations.CreateModel(
            name='Poco1536',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicao', models.CharField(help_text='Posição do poço (ex: A01, AF48)', max_length=4)),
                ('amostra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.amostra')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa1536')),
            ],
            options={
                'verbose_name': 'Poço de placa 1536',
                'verbose_name_plural': 'Poços de Placas 1536',
                'unique_together': {('placa', 'posicao')},
            },
        ),
        migrations.CreateModel(
            name='Poco384',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicao', models.CharField(help_text='Posição do poço (ex: A01, P24)', max_length=3)),
                ('amostra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.amostra')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa384')),
            ],
            options={
                'verbose_name': 'Poço de placa  384',
                'verbose_name_plural': 'Poços de Placas  384',
                'unique_together': {('placa', 'posicao')},
            },
        ),
        migrations.CreateModel(
            name='Poco96',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicao', models.CharField(help_text='Posição do poço (ex: A01, H12)', max_length=3)),
                ('amostra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.amostra')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.placa96')),
            ],
            options={
                'verbose_name': 'Poço de Placa   96',
                'verbose_name_plural': 'Poços de Placas   96',
                'unique_together': {('placa', 'posicao')},
            },
        ),
        migrations.AddIndex(
            model_name='amostra',
            index=models.Index(fields=['codigo_amostra'], name='app_amostra_codigo__f56783_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='amostra',
            unique_together={('empresa', 'projeto', 'codigo_amostra')},
        ),
        migrations.AddIndex(
            model_name='resultadoamostra',
            index=models.Index(fields=['amostra', 'upload'], name='app_resulta_amostra_a598e7_idx'),
        ),
        migrations.AddIndex(
            model_name='resultadoamostra',
            index=models.Index(fields=['resultado_fh'], name='app_resulta_resulta_d3945f_idx'),
        ),
        migrations.AddIndex(
            model_name='resultadoamostra',
            index=models.Index(fields=['resultado_aj'], name='app_resulta_resulta_909b02_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='resultadoamostra',
            unique_together={('upload', 'amostra')},
        ),
        migrations.AlterUniqueTogether(
            name='projeto',
            unique_together={('empresa', 'codigo_projeto')},
        ),
    ]

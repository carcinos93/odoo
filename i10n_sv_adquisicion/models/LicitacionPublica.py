from odoo import fields, models, api


class LicitacionPublica(models.Model):
    _name = 'adquisicion.licitacion_publica'
    _description = 'Licitación pública'

    # datos generales
    numeroRequisicion = fields.Char(string='Número requisición')
    nombreSolicitante = fields.Char(string='Nombre solicitante')
    fechaSolicitud = fields.Datetime(string='Fecha solicitud')
    nombreProyecto = fields.Char(string='Nombre del proyecto')
    insumo = fields.Char(string='Insumo')
    actividad = fields.Char(string='Actividad')
    fechaEntrega = fields.Datetime(string='Fecha máxima de entrega')
    lugarEntrega = fields.Char(string='Lugar de entrega')
    codigoActividad = fields.Selection(string='Código de actividad', selection=[])
    paisBeneficiario = fields.Selection(string='Nombre autorizado', selection=[])
    cantidad = fields.Integer(string='Cantidad', required=False)
    descripcion = fields.Text(string='Descripción completa', required=False)
    montoPresupuestado = fields.Float(string='Monto presupuestado', required=False)
    lineaPresupuestaria = fields.Selection(string='Línea presupuestaria', selection=[])
    categoriaGasto = fields.Selection(string='Categoría del gasto', selection=[])
    lineaPresupuestariaPOA = fields.Selection(string='Línea presupuestaria POA', selection=[])
    nombreSolicitanteLista = fields.Selection(string='Nombre solicitante', selection=[])
    nombreAutorizado = fields.Selection(string='Nombre autorizado', selection=[])
    fechaRecibida = fields.Datetime(string='Fecha máxima de entrega', required=False)
    nombre = fields.Char(string='Nombre', required=False)
    comentario = fields.Text(string='Comentario', required=False)
    documentosBases = fields.One2many(comodel_name='adquisicion.documentos_bases_licitacion_publica', inverse_name='licitacionPublica_ids', string='Documentos bases')
    documentosParticipantes = fields.One2many(comodel_name='adquisicion.documentos_participantes_licitacion_publica', inverse_name='licitacionPublica_ids', string='Documentos participantes')
    documentosAdjudicaciones = fields.One2many(comodel_name='adquisicion.documentos_adjudicacion_licitacion_publica', inverse_name='licitacionPublica_ids', string='Documentos adjucicación')


class DocumentosBasesLicitacion(models.Model):
    _name = 'adquisicion.documentos_bases_licitacion_publica'
    codigoTipoDocumento = fields.Selection(string='Código tipo documento', selection=[])
    archivo = fields.Binary(string="Carga de archivo")
    palabrasClave = fields.Char(string='Palabras clave', required=False)
    licitacionPublica_ids = fields.Many2one(comodel_name='adquisicion.licitacion_publica', string='Licitación pública')


class DocumentosParticipantesLicitacion(models.Model):
    _name = 'adquisicion.documentos_participantes_licitacion_publica'
    codigoTipoDocumento = fields.Selection(string='Código tipo documento', selection=[])
    archivo = fields.Binary(string="Carga de archivo")
    palabrasClave = fields.Char(string='Palabras clave', required=False)
    licitacionPublica_ids = fields.Many2one(comodel_name='adquisicion.licitacion_publica', string='Licitación pública')


class DocumentosParticipantesLicitacion(models.Model):
    _name = 'adquisicion.documentos_adjudicacion_licitacion_publica'
    codigoTipoDocumento = fields.Selection(string='Código tipo documento', selection=[])
    archivo = fields.Binary(string="Carga de archivo")
    palabrasClave = fields.Char(string='Palabras clave', required=False)
    licitacionPublica_ids = fields.Many2one(comodel_name='adquisicion.licitacion_publica',
                                                string='Licitación pública')

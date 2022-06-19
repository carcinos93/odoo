from odoo import fields, models, api


class LicitacionPrivada(models.Model):
    _name = 'adquisicion.licitacion_privada'
    _description = 'Licitación privada'

    # Datos generales
    numeroRequisicion = fields.Integer(string='Número requisición',required=False)
    nombreSolicitante = fields.Char(string='Nombre solicitante', required=False)
    fecha = fields.Datetime(string='Fecha', required=False)
    nombreProyecto = fields.Char(string='Nombre de proyecto', required=False)
    insumo = fields.Char(string='Insumo', required=False)
    actividad = fields.Char(string='Insumo', required=False)
    fechaEntrega = fields.Datetime(string='Fecha máxima de entrega', required=False)
    lugarEntrega = fields.Char(string='Lugar de entrega', required=False)
    codigoActividad = fields.Selection(string='Código de actividad', selection=[])
    paisBeneficiario = fields.Selection(string='Nombre autorizado', selection=[])
    cantidad = fields.Integer(string='Cantidad',required=False)
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
    documentos = fields.One2many(comodel_name='adquisicion.documentos_licitacion_privada', inverse_name='licitacionPrivada_ids', string='Documentos')


class DocumentosLicitacionPrivada(models.Model):
    _name = 'adquisicion.documentos_licitacion_privada'
    codigoTipoDocumento = fields.Char(string='Código tipo documento', required=False)
    archivo = fields.Binary(string="Carga de archivo" )
    licitacionPrivada_ids = fields.Many2one(comodel_name='adquisicion.licitacion_privada', string='Licitación privada')

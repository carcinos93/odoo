from odoo import fields, models, api


class CompraDirecta(models.Model):
    _name = 'adquisicion.compra_directa'
    _description = 'Compra directa'
    # pestaña 1
    numero_requisicion = fields.Integer(string='Numero requisición')
    nombre_solicitante = fields.Char(string='Nombre solicitante')
    fecha_solicitud = fields.Datetime(string='Fecha solicitud')
    nombre_proyecto = fields.Char(string='Nombre del proyecto')
    insumo = fields.Char(string='Insumo')
    actividad = fields.Char(string='Actividad')
    fecha_entrega = fields.Datetime(string='Fecha máxima de entrega')
    lugar_entrega = fields.Text(string="Lugar entrega")
    codigo_actividad = fields.Selection(string='Código de actividad', selection=[])
    pais_beneficiario = fields.Selection(string='País Beneficiario', selection=[])
    cantidad = fields.Integer(string='Cantidad')
    descripcion_completa = fields.Text(string="Descripción completa ")
    monto_presupuestado = fields.Float(string='Monto presupuestado', required=False)
    linea_presupuestaria = fields.Selection(string='Línea presupuestaria', selection=[])
    categoria_gasto = fields.Selection(string='Categoría del gasto', selection=[])
    linea_presupuestaria_poa = fields.Selection(string='Línea presupuestaria POA', selection=[])
    nombre_autorizado = fields.Selection(string='Nombre autorizado', selection=[])
    fecha_recibida = fields.Datetime(string='Fecha recibida')
    nombre = fields.Char(string='Nombre')
    comentario = fields.Text(string="Comentario")
    documentos = fields.One2many(comodel_name='adquisicion.compra_directa_documentos', inverse_name='compraDirecta_ids',
                                        string='Documentos')
    estado = fields.Boolean(string='Estado')


class DocumentosCompraDirecta(models.Model):
    _name = 'adquisicion.compra_directa_documentos'
    codigo_tipo_documento = fields.Selection(string='Codigo tipo documento', selection=[])
    carga_achivo = fields.Binary(string="Carga de archivo")
    palabras_clave = fields.Char(string='Palabras clave')
    compraDirecta_ids = fields.Many2one(comodel_name='adquisicion.compra_directa', string='Compra directa')

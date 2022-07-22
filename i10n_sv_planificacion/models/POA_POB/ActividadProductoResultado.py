from odoo import fields, models, api, exceptions
import re


class ActividadProductoResultado(models.Model):
    _name = 'planificacion.actividad_producto_resultado'
    # _inherit = 'base.auditoria'
    # _rec_name = "nombreActividad"

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    @api.depends('detalle', 'detalle.montoAsignado')
    def _compute_actividad_producto_detalle(self):
        for record in self:
            total = 0.0
            for item in record.detalle:
                total += item.montoAsignado
            record.total_monto = total

    def _codigo_generador(self):
        prefijo = "A"
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        parent_codigo = re.sub("^([A-Za-z\\.]*)", "", parent_codigo)  # Se elimina el prefijo
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo =(prefijo + "." if prefijo else "") + parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)
    total_monto = fields.Float(string='Total', store=True, readonly=True, compute=_compute_actividad_producto_detalle)
    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )
    codigoActividad = fields.Char(string='Código actividad', required=False, default=_codigo_generador)
    nombreActividad = fields.Text(string='Nombre de actividad', required=False)
    responsable = fields.Many2one('hr.employee', 'Responsable de actividad')
    detalle = fields.One2many(comodel_name='planificacion.actividad_producto_resultado_detalle',inverse_name='actividad_resultado_ids',string=' Detalle', copy=True)
    indicadores = fields.One2many(comodel_name='planificacion.indicador_actividad_producto_resultado',inverse_name='actividad_resultado_ids',string='Indicadores', copy=True)
    metas = fields.One2many(comodel_name='planificacion.meta_actividad_producto_resultado', inverse_name='actividad_resultado_ids',string='Metas', copy=True)
    avances = fields.One2many(comodel_name='planificacion.avance_indicador_actividad', inverse_name='actividad_resultado_ids',string='Metas', copy=True)
    peso = fields.Float(string='Peso', required=False, default=0.00)
    # modelo Padre
    productoResultado_ids = fields.Many2one(comodel_name='planificacion.producto_resultado_efecto_impacto', string='Producto resultado', required=True, ondelete='cascade')

    # dummy
    fuenteFinanciamiento = fields.Integer(string='Fuente Financiamiento', required=False)
    # _rec_name = 'nombre del campo que desea que se muestre' # listas

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigoActividad, data.nombreActividad)
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        res = super(ActividadProductoResultado, self).create(vals)
        if 'nombreActividad' in vals:
            message = "Creación de actividad %s %s" % (res.codigoActividad, res.nombreActividad)
            objetivo = res.productoResultado_ids.resultadoEfectoImpacto_ids.objetivoEstrategicoDetalle_ids
            objetivo.eje_ids.poa_ids.message_post(body=message)
        return res


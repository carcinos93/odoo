from odoo import fields, models, api


class EjeEstrategico(models.Model):
    _name = 'planificacion.eje_estrategico'
    # _inherit = 'base.auditoria' # No funciona?

    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    @api.depends('objetivos_estrategicos','objetivos_estrategicos.resultados.productos.presupuesto')
    def _compute_total_presupuesto_asignado(self):
        for record in self:
            total = 0.0
            for objetivo in record.objetivos_estrategicos:
                for resultado in objetivo.resultados:
                    for producto in resultado.productos:
                        total += producto.presupuesto
            record.totalPresupuesto = total

    def _codigo_generador(self):
        prefijo = "E"
        parent = self._context.get('items')
        total = len(parent) + 1
        return (prefijo + "." if prefijo else "") + str(total)

    codigo = fields.Char(string='Código de eje estratégico', readonly=False, default=_codigo_generador) #  default=_default_codigo
    descripcion = fields.Text(string="Nombre del eje estratégico", required=False)
    # Modelo padre
    periodo_ids = fields.Many2one(comodel_name='planificacion.periodo', string='Período')
    codigoPeriodo = fields.Char(related="periodo_ids.codigo")
    objetivos_estrategicos = fields.One2many(comodel_name='planificacion.objetivo_estrategico',copy=True, inverse_name='ejes_estrategicos_ids', string='Objetivos estratégicos')
    totalPresupuesto = fields.Float(string='Presupuesto total', required=False, compute=_compute_total_presupuesto_asignado)
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % ( data.codigo, data.descripcion, )
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        res = super(EjeEstrategico, self).create(vals)
        if 'descripcion' in vals:
            message = "Creación de eje estratégico %s %s" % (vals['codigo'], vals['descripcion'])
            res.periodo_ids.message_post(body=message)
        return res







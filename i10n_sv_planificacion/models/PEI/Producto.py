from odoo import fields, models, api


class Producto(models.Model):
    _name = 'planificacion.producto'
    # _inherit = 'base.auditoria'
    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    def _codigo_generador(self):
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        # se filtran los registros que tengan estado borrado
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de producto', readonly=False, default=_codigo_generador) # default=_default_codigo
    descripcion = fields.Text(string="Descripción de producto",required=False)
    presupuesto = fields.Float(string='Presupuesto por año', required=False)
    indicadoresProducto = fields.One2many(comodel_name='planificacion.indicador_producto',copy=True, inverse_name='producto_ids', string='Indicadores producto')
    metas = fields.One2many(comodel_name='planificacion.meta_producto',copy=True, inverse_name='producto_ids', string='Indicadores producto')
    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )
    resultado_ids = fields.Many2one(comodel_name='planificacion.resultado', string='Resultado')


    # @api.model
    # def create(self, vals):
    #     vals['codigo'] = self._codigo_generador(vals)
    #     records = super(Producto, self).create(vals)
    #     return records
    #
    # def _codigo_generador(self, vals):
    #     parent = self.env['planificacion.resultado'].search([('id', '=', str(vals['resultado_ids'] ))])
    #     total = self.env['planificacion.producto'].search_count([('resultado_ids', '=', vals['resultado_ids'] )]) + 1
    #     return str( parent.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion)
            result.append((data.id, name,))
        return result

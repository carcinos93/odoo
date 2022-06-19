from odoo import fields, models, api


class IndicadorProducto(models.Model):
    _name = 'planificacion.indicador_producto'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de indicador de producto ', readonly=False, default=_codigo_generador) # default=_default_codigo
    descripcion = fields.Text(string="Descripción de indicador de producto",required=False)
    producto_ids = fields.Many2one(comodel_name='planificacion.producto', string='Producto')


    # @api.model
    # def create(self, vals):
    #     vals['codigo'] = self._codigo_generador(vals)
    #     records = super(IndicadorProducto, self).create(vals)
    #     return records
    #
    # def _codigo_generador(self, vals):
    #     parent = self.env['planificacion.producto'].search([('id', '=', str(vals['producto_ids'] ))])
    #     total = self.env['planificacion.indicador_producto'].search_count([('producto_ids', '=', vals['producto_ids'] )]) + 1
    #     return str( parent.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion, )
            result.append((data.id, name,))
        return result
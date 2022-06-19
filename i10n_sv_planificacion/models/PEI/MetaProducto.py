from odoo import fields, models, api


class MetaProducto(models.Model):
    _name = 'planificacion.meta_producto'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        # se filtran los registros que tengan estado borrado
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de meta', readonly=False, default=_codigo_generador)  # default=_default_codigo
    descripcion = fields.Text(string="Descripción de la meta", required=False)
    tipoValor = fields.Selection(string='Tipo valor', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    valor = fields.Float(string='Meta', required=False)
    # resultados = fields.One2many(comodel_name='planificacion.resultado', inverse_name='meta_ids', string='Resultados')
    producto_ids = fields.Many2one(comodel_name='planificacion.producto', string='Producto')

    # @api.model
    # def create(self, vals):
    #     vals['codigo'] = self._codigo_generador(vals)
    #     records = super(MetaProducto, self).create(vals)
    #     return records
    #
    # def _codigo_generador(self, vals):
    #     parent = self.env['planificacion.producto'].search([('id', '=', str(vals['producto_ids'] ))])
    #     total = self.env['planificacion.meta_producto'].search_count([('producto_ids', '=', vals['producto_ids'] )]) + 1
    #     return str( parent.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion)
            result.append((data.id, name,))
        return result

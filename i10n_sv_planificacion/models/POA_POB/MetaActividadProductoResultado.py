from odoo import fields, models, api, exceptions


class MetaActividadProductoResultado(models.Model):
    _name = 'planificacion.meta_actividad_producto_resultado'

    def _codigo_generador(self):
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de meta', default=_codigo_generador)  # default=_default_codigo
    descripcion = fields.Text(string="Meta", required=False)
    tipoValor = fields.Selection(string='Tipo valor', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    valor = fields.Float(string='Valor', required=False)
    actividad_resultado_ids = fields.Many2one(comodel_name='planificacion.actividad_producto_resultado', string='Actividad producto resultado', required=True, ondelete='cascade')

    #@api.model
    #def create(self, vals):
    #    vals['codigo'] = self._codigo_generador(vals)
    #    records = super(IndicadorActividadProductoResultado, self).create(vals)
    #    return records

    #def _codigo_generador(self, vals):
    #    parent = self.env['planificacion.producto'].search([('id', '=', str(vals['producto_ids']))])
    #    total = self.env['planificacion.indicador_producto'].search_count(
    #        [('producto_ids', '=', vals['producto_ids'])]) + 1
    #    return str(parent.codigo) + "." + str(total)
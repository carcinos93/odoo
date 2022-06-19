from odoo import fields, models, api


class MetaProductoResultado(models.Model):
    _name = 'planificacion.meta_producto_resultado'

    def _codigo_generador(self):
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    meta = fields.Many2one(comodel_name='planificacion.meta_producto', string='Meta', required=False)
    codigoMeta = fields.Char(string='Código meta', required=False, default=_codigo_generador)
    descripcionMeta = fields.Text(string="Descripción meta", required=False)
    tipoValor = fields.Selection(string='Tipo valor', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    valor = fields.Float(string='Meta', required=False)
    #tipoValor = fields.Selection(related="meta.tipoValor")
    #valor = fields.Float(related="meta.valor")

    # Modelo padre
    productoResultado_ids = fields.Many2one(comodel_name='planificacion.producto_resultado_efecto_impacto', string='Producto resultado', required=True, ondelete='cascade')
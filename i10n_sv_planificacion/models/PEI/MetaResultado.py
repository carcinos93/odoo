from odoo import fields, models, api


class MetaResultado(models.Model):
    _name = 'planificacion.meta_resultado'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter(lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de meta', readonly=False, default=_codigo_generador)  # default=_default_codigo
    descripcion = fields.Text(string="Descripción de la meta", required=False)
    tipoValor = fields.Selection(string='Tipo valor', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    valor = fields.Float(string='Meta', required=False)
    # resultados = fields.One2many(comodel_name='planificacion.resultado', inverse_name='meta_ids', string='Resultados')
    resultado_ids = fields.Many2one(comodel_name='planificacion.resultado', string='Resultado')

    # @api.model
    # def create(self, vals):
    #     vals['codigo'] = self._codigo_generador(vals)
    #     records = super(MetaResultado, self).create(vals)
    #     return records
    #
    # def _codigo_generador(self, vals):
    #     parent = self.env['planificacion.resultado'].search([('id', '=', str(vals['resultado_ids'] ))])
    #     total = self.env['planificacion.meta_resultado'].search_count([('resultado_ids', '=', vals['resultado_ids'] )]) + 1
    #     return str( parent.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion)
            result.append((data.id, name,))
        return result

from odoo import fields, models, api

# descartado
class Resultado(models.Model):
    _name = 'planificacion.resultado'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        # los items aparecen de la siguiente forma [2, 6, False] = [Estado, ID, ?]
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        # se filtran los registros que tengan estado borrado
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de resultado', readonly=False, default=_codigo_generador) # default=_default_codigo
    descripcion = fields.Text(string="Descripción de resultados",required=False)
    responsable = fields.Many2one('hr.employee', 'Responsable')
    indicadorResultados = fields.One2many(comodel_name='planificacion.indicador_resultado',copy=True, inverse_name='resultado_ids', string='Indicador de resultado')
    productos = fields.One2many(comodel_name='planificacion.producto',copy=True, inverse_name='resultado_ids', string='Productos')
    metas = fields.One2many(comodel_name='planificacion.meta_resultado',copy=True, inverse_name='resultado_ids', string='Metas')
    objetivoEstrategico_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico', string='Objetivo estrategico')


    # @api.model
    # def create(self, vals):
    #     vals['codigo'] = self._codigo_generador(vals)
    #     records = super(Resultado, self).create(vals)
    #     return records
    #
    # def _codigo_generador(self, vals):
    #     parent = self.env['planificacion.objetivo_estrategico'].search([('id', '=', str(vals['objetivoEstrategico_ids'] ))])
    #     total = self.env['planificacion.resultado'].search_count([('objetivoEstrategico_ids', '=', vals['objetivoEstrategico_ids'] )]) + 1
    #     return str( parent.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % ( data.codigo, data.descripcion, )
            result.append((data.id, name,))
        return result
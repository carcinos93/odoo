from odoo import fields, models, api
import re


class ObjetivoEstrategico(models.Model):
    _name = 'planificacion.objetivo_estrategico'
    # _inherit = 'base.auditoria' # No funciona?

    def _codigo_generador(self):
        prefijo = "O"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        parent_codigo = re.sub("^([A-Za-z\\.]*)", "", parent_codigo)  # Se elimina el prefijo
        # se filtran los registros que tengan estado borrado
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = (prefijo + "." if prefijo else "") + parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de objetivo', readonly=False, default=_codigo_generador) # default=_default_codigo
    descripcion = fields.Text(string="Nombre de objetivo",required=False)
    indicadores_objetivos = fields.One2many(comodel_name='planificacion.indicador_objetivo',copy=True, inverse_name='objetivo_estrategicos_ids', string='Indicador de objetivos')
    resultados = fields.One2many(comodel_name='planificacion.resultado',copy=True, inverse_name='objetivoEstrategico_ids', string='Resultados')
    metas = fields.One2many(comodel_name='planificacion.meta',copy=True, inverse_name='objetivo_estrategico_ids', string='Metas')
    # Modelo padre
    ejes_estrategicos_ids = fields.Many2one(comodel_name='planificacion.eje_estrategico', string='Eje estratégico')

    #@api.model
    #def create(self, vals):
    #    vals['codigo'] = self._codigo_generador(vals)
    #    records = super(ObjetivoEstrategico, self).create(vals)
    #    return records

   # def _codigo_generador(self, vals):
   #     eje = self.env['planificacion.eje_estrategico'].search([('id', '=', str(vals['ejes_estrategicos_ids'] ))])
   #     total = self.env['planificacion.objetivo_estrategico'].search_count([('ejes_estrategicos_ids', '=', vals['ejes_estrategicos_ids'] )]) + 1
   #     return str( eje.codigo) + "." + str(total)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % ( data.codigo, data.descripcion, )
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        res = super(ObjetivoEstrategico, self).create(vals)
        if 'descripcion' in vals:
            message = "Creación de objetivo estratégico %s %s" % (vals['codigo'], vals['descripcion'])
            if res.ejes_estrategicos_ids:
                periodo_ids = res.ejes_estrategicos_ids.periodo_ids
                if periodo_ids:
                    periodo_ids.message_post(body=message)
        return res
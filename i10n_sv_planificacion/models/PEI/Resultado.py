from odoo import fields, models, api
import re


class Resultado(models.Model):
    _name = 'planificacion.resultado'

    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        prefijo = "R"
        # los items aparecen de la siguiente forma [2, 6, False] = [Estado, ID, ?]
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        parent_codigo = re.sub("^([A-Za-z\\.]*)", "", parent_codigo) # Se elimina el prefijo
        # se filtran los registros que tengan estado borrado
        filtrados = list(filter(lambda x: x[0] != 2, items))
        codigo = (prefijo + "." if prefijo else "") + parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de resultado', readonly=False,
                         default=_codigo_generador)  # default=_default_codigo
    descripcion = fields.Text(string="Nombre de resultado", required=False)
    responsable = fields.Many2one('hr.employee', 'Responsable')
    indicadorResultados = fields.One2many(comodel_name='planificacion.indicador_resultado', copy=True,
                                          inverse_name='resultado_ids', string='Indicador de resultado')
    productos = fields.One2many(comodel_name='planificacion.producto', copy=True, inverse_name='resultado_ids',
                                string='Productos')
    metas = fields.One2many(comodel_name='planificacion.meta_resultado', copy=True, inverse_name='resultado_ids',
                            string='Metas')
    objetivoEstrategico_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico',
                                              string='Objetivo estrategico')

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion,)
            result.append((data.id, name,))
        return result

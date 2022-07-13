from odoo import fields, models, api, exceptions
import re


class IndicadorActividadProductoResultado(models.Model):
    _name = 'planificacion.indicador_actividad_producto_resultado'

    def _codigo_generador(self):
        prefijo = "A.I"
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        parent_codigo = re.sub("^([A-Za-z\\.]*)", "", parent_codigo)  # Se elimina el prefijo
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo =(prefijo + "." if prefijo else "") + parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código del indicador', default=_codigo_generador )
    nombre = fields.Char(string="Nombre del indicador", required=False)
    descripcion = fields.Text(string="Definición detallada", required=False)
    tipoValor = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    fechaPrevista = fields.Selection( string='Fecha prevista de consecución',selection=[('1', 'I Trimestre'),('2', 'II Trimestre'),('3', 'III Trimestre'),('4', 'IV Trimestre')], required=False)

    # Modelo padre
    actividad_resultado_ids = fields.Many2one(comodel_name='planificacion.actividad_producto_resultado', string='Actividad producto resultado', required=True, ondelete='cascade')

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.nombre if data.nombre else data.descripcion)
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        res = super(IndicadorActividadProductoResultado, self).create(vals)
        # Al crear indicador actividad se crea la linea del avance
        data = {
            'actividad_resultado_ids': vals['actividad_resultado_ids'],
            'indicadorActividad': res.id
        }
        self.env['planificacion.avance_indicador_actividad'].create(data)

        return res




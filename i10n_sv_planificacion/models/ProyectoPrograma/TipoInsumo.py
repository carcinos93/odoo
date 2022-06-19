from odoo import fields, models, api


class TipoInsumo(models.Model):
    _name = 'planificacion.tipo_insumo'
    descripcion = fields.Text(string="Descripción", required=True)

    def name_get(self):
        result = []
        for data in self:
            name = '%s' % data.descripcion
            result.append((data.id, name,))
        return result
from odoo import fields, models, api


class ActivoFijo(models.Model):
    _name = 'ac.activo_fijo'
    # _description = 'Description'

    numero_factura = fields.Integer(string='Numero factura')
    fecha_compra = fields.Datetime(string='Fecha compra', required=False)
    descripcion = fields.Text(string="Descripcion", required=False)

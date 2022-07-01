from odoo import fields, models, api


class Factura(models.Model):
    _name = 'libro_modulo.factura'
    _description = 'Factura de libros'
    _rec_name = 'noFactura'

    noFactura = fields.Char(string='No factura',  required=False)
    nombreDe = fields.Char(string='Nombre de',  required=False)
    fecha = fields.Date(string='Fecha', required=False)
    descripcion = fields.Text(string="Descripcion",required=False)
    detalles = fields.One2many(comodel_name='libro_modulo.factura_detalle',inverse_name='factura_ids',string='Detalles', required=False)

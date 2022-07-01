from odoo import fields, models, api


class Detalle(models.Model):
    _name = 'libro_modulo.factura_detalle'
    _description = 'Detalle Factura de libros'


    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.cantidad * record.precio


    producto = fields.Char(string='Producto', required=False)
    precio = fields.Float(string='Precio', required=False)
    # cantidad = fields.Integer(string='Cantidad', required=False)
    subtotal = fields.Float(string='Subtotal', required=False, compute=_compute_subtotal)
    # Modelo padre
    factura_ids = fields.Many2one(comodel_name='libro_modulo.factura',string='Factura_ids',required=False, ondelete='cascade')


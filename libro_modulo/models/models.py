from odoo import fields, models, api


class Libro(models.Model):
    _name = 'libro_modulo.libro'
    _description = 'Modulo para registrar libros'

    titulo = fields.Char()
    fecha = fields.Datetime(string='Fecha',  required=False)
    descripcion = fields.Text(string="Descripcion", required=False)
    portada = fields.Binary(string="Portada" )
    precio = fields.Float(string='Precio', required=False)
    autor = fields.Many2one(comodel_name='res.partner', string='Autor')






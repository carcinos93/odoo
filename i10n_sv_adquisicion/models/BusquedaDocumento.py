from odoo import fields, models, api


class BusquedaDocumento(models.Model):
    _name = 'adquisicion.busqueda_documento'
    numeroCompra = fields.Char(string='Número compra', required=False)
    numeroDocumento = fields.Char(string='Número documento', required=False)



from odoo import fields, models, api


class TipoDocumento(models.Model):
    _name = 'adquisicion.tipo_documento'
    # _description = 'Description'

    codigo_TipoDocumento = fields.Char(string='Código tipo tocumento',required=False)
    tipoDocumento = fields.Char(string='Tipo documento',required=False)
    nombreTipoDocumento = fields.Char(string='Nombre tipo documento',required=False)
    tipoCompra = fields.Selection(string='Tipo compra', selection=[])
    tieneFechaVencimiento = fields.Boolean(string='Tiene fecha vencimiento',required=False)
    


from odoo import fields, models, api


class Proveedor(models.Model):
    _name = 'adquisicion.proveedor'
    _description = 'Proveedor'

    codigo_proveedor = fields.Char(string='Codigo proveedor')
    direccion = fields.Text(string="Dirección física del Proveedor")
    identificacion_tributaria = fields.Char(string='Identificación tributaria')
    direccion_electronica = fields.Text(string="Dirección electrónica")
    nombre_contacto = fields.Char(string='Nombre de la persona contacto')
    telefono_contacto = fields.Char(string='Teléfonos de contacto')
    actividad_economica = fields.Selection(string='Actividad económica', selection=[])
    bienes_servicios = fields.Text(string="Bienes o servicios ofrecidos")
    cumple_oferta = fields.Boolean(string='Cumple oferta')
    cuenta_bancaria = fields.Char(string='Cuenta bancaria')
    nombre_banco = fields.Selection(string='Nombre del Banco', selection=[])
    beneficiario = fields.Char(string='Beneficiario')
    swift = fields.Char(string='Swift')





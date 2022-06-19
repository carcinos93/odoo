from odoo import fields, models, api


class Contrato(models.Model):
    _name = 'adquisicion.contrato'
    # _description = 'Description'

    noCorrelativo = fields.Char(string='N° Correlativo', required=False)
    nombre = fields.Char(string='Nombre', required=False)
    fechaInicio = fields.Datetime(string='Fecha inicio', required=False)
    fechaTerminacion = fields.Datetime(string='Fecha terminación', required=False)
    actividad = fields.Char(string='Actividad', required=False)
    monto = fields.Float(string='Monto', required=False)
    planPagos = fields.Char(string='Plan de pagos', required=False)
    montoGarantia = fields.Float(string='Monto de garantía', required=False)
    nombreSolicitante = fields.Selection(string='Nombre solicitante', selection=[])
    nombreAutorizado = fields.Selection(string='Nombre autorizado', selection=[])
    archivo = fields.Binary(string="Carga de archivo")




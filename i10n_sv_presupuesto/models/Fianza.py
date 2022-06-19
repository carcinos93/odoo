from odoo import fields, models, api


class Fianza(models.Model):
    _name = 'presupuesto.fianza'
    # _description = 'Description'

    numeroRequisicion = fields.Char(string='Numero requisición', required=False)
    nombreProyecto = fields.Char(string='Numero requisición', required=False)
    montoFianza = fields.Float(string='Monto de la fianza', required=False)
    archivo = fields.Binary(string="Carga de archivo" )


from odoo import fields, models, api


class Adenda(models.Model):
    _name = 'presupuesto.adenda'
    # _description = 'Description'

    nCorrelativoAdenda = fields.Char(string='N° correlativo de Adenda', required=False)
    nCorrelativoContrato = fields.Char(string='N° correlativo de contrato', required=False)
    nombreSolicitante = fields.Selection(string='Nombre solicitante', selection=[])
    nombreAutorizado = fields.Selection(string='Nombre autorizado', selection=[])
    archivo = fields.Binary(string="Carga de archivo")


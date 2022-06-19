from odoo import fields, models, api


class ChangeBudget(models.Model):
    _name = 'bg.change_budget'
    # _description = 'Description'
    # Informacion a modificar
    numeroSolicitud = fields.Char(string='Número solicitud', required=False)
    fechaSolicitud = fields.Datetime(string='Fecha solicitud', required=False)
    fuentesFinanciamiento = fields.Selection(string='Fuentes de financiamiento', selection=[], required=False)
    actividad = fields.Selection(string='Actividad', selection=[], required=False)
    codigInsumo = fields.Selection(string='Código de insumo', selection=[], required=False)
    unidadMedida = fields.Selection(string='Unidad de medida', selection=[], required=False)
    cantidad = fields.Integer(string='Cantidad', required=False)
    costoUnitario = fields.Float(string='Costo unitario', required=False)
    costoTotal = fields.Float(string='Costo total', required=False)
    # presupuesto
    correlativo = fields.Char(string='Correlativo', required=False)
    trimestre1 = fields.Float(string='Trimestre I', required=False)
    trimestre2 = fields.Float(string='Trimestre II', required=False)
    trimestre3 = fields.Float(string='Trimestre III', required=False)
    trimestre4 = fields.Float(string='Trimestre IV', required=False)


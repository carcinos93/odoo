from odoo import fields, models, api


class ParametroMontos(models.Model):
    _name = 'presupuesto.parametro_monto'
    # _description = 'Description'
    # Bienes y suministros (BM)
    libreGestionBM = fields.Float(string='Libre gestión')
    licitacionPrivadaBM = fields.Float(string='Licitación privada')
    licitacionPublicaBM = fields.Float(string='Licitación pública')
    otrosProcedimientoBM = fields.Float(string='Otros Procedimientos ')

    # Servicios
    libreGestionServ = fields.Float(string='Libre gestión')
    licitacionPrivadaServ = fields.Float(string='Licitación privada')
    licitacionPublicaServ = fields.Float(string='Licitación pública')
    otrosProcedimientoServ = fields.Float(string='Otros Procedimientos ')

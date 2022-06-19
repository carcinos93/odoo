 # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date, datetime
class purchaseType(models.Model):
    _name = 'purchase.type'

    code = fields.Char('Codigo')
    name = fields.Char('Descripcion', size=120)
    doc_details_ids = fields.One2many('purchase.type.doc', 'type_id', 'Documentos')
    range_ids = fields.One2many('purchase.type.range', 'type_id', '')
    used_comite = fields.Boolean(string='Utiliza Cómite Evaluador')

class purchaseTypeDoc(models.Model):
    _name = 'purchase.type.doc'

    corr = fields.Char('Correlativo')
    type_id = fields.Many2one('purchase.type')
    name = fields.Char('Nombre documento', size=120)
    mandatory = fields.Boolean('Mandatorio')
    state_author = fields.Selection([('1', 'Requisicion'),
                                     ('2', 'Ofertas'),
                                     ('3', 'Orden de Compra')], 'estado donde Es Requerido')
class purchaseTypeRange(models.Model):

    _name = 'purchase.type.range'

    type_id = fields.Many2one('purchase.type')
    amount_one = fields.Float('Desde')
    amount_two = fields.Float('Hasta')
    type = fields.Selection([('1', 'Bien'),
                             ('2', 'Servicio')], 'Tipo')
    code = fields.Char('Numero Transaccion')
# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _, tools, exceptions
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError


class ERPAssetCategory(models.Model):
    _name = 'erp.asset.category'

    name = fields.Char(string='Nombre', select=1)
    note = fields.Text(string='Comentario')
    account_asset_id = fields.Many2one('account.account', string='Cuenta de Activo')
    account_depreciation_id = fields.Many2one('account.account', string='Cuenta de Depreciación')
    account_expense_id = fields.Many2one('account.account', string='Cuenta de Gastos')
    journal_id = fields.Many2one('account.journal', string='Tipo de Partida')
    method = fields.Selection([('linear', 'Lineal'), ('degressive', 'Decreciente')], string='Metodo de Cálculo',
                              help="Choose the method to use to compute the amount of depreciation lines.\n" \
                                        "  * Linear: Calculated on basis of: Gross Value / Number of Depreciations\n" \
                                        "  * Degressive: Calculated on basis of: Residual Value * Degressive Factor", default='linear')
    factor_degressive = fields.Float(string='Factor Decreciente', default=0.3)
    method_number = fields.Integer(string='Número de Depreciaciones', default=5)
    method_period = fields.Integer(string='Número de Meses en Periodo', default=12)
    method_time = fields.Selection([('number', 'Número de Depreciaciones'), ('end', 'Fecha Finalizacion')], string='Método de Tiempo', default='number')
    method_end = fields.Date(string='Fecha Finalización')

ERPAssetCategory()
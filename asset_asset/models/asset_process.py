# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _, tools, exceptions
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError


class ERPAssetAsset(models.Model):
    _name = 'erp.asset.asset'

    name = fields.Char(string='Nombre', select=1)
    code = fields.Char(string='Referencia')
    category_id = fields.Many2one('erp.asset.category', string='Categoria Activos')
    asset_id = fields.Many2one('erp.asset.asset', string='Activo Padre')
    date_purchase = fields.Date(string='Fecha de Compra')
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
    employee_id = fields.Many2one('hr.employee', string='Responsable')
    department_id = fields.Many2one('hr.department', string='Departamento')
    purchase_value = fields.Float(string='Valor Compra')
    salvage_value = fields.Float(string='Valor Salvaguarda')
    residual_value = fields.Float(string='Valor Residual')
    depreciate_value = fields.Float(string='Valor Depreciar')
    depreciation_annual = fields.Float(string='Depreciación Anual')
    monthly_cost = fields.Float(string='Costo Mensual')
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
    line_ids = fields.One2many('erp.asset.depreciation.line', 'asset_id', string='Lineas')

ERPAssetAsset()

class ERPAssetDepreciationLine(models.Model):
    _name = 'erp.asset.depreciation.line'

    name = fields.Char(string='Nombre Depreciación')
    sequence = fields.Integer(string='Secuencia')
    asset_id = fields.Many2one('erp.asset.asset', string='Activo Fijo')
    amount = fields.Float(string='Monto Depreciación')
    depreciated_value = fields.Float(string='Monto Depreciado')
    remaining_value = fields.Float(string='Monto Pendiente Depreciar')
    depreciation_date = fields.Date(string='Fecha Depreciación')
    move_id = fields.Many2one('account.move', string='Partida Contable')
    move_check = fields.Boolean(string='Depreciación Contabilizada')


ERPAssetDepreciationLine()
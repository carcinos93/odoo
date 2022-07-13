# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime


class CuentaBanco(models.Model):
    _name = 'budget.cuenta_banco'
    _description = 'Cuentas de banco de proyectos'

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    bank = fields.Many2one('res.bank', string='Banco')
    bankAccount = fields.Char(string='Cuenta bancaria')
    saldoBanco = fields.Float(string='Saldos')
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)
    # Modelo padre
    program_ids = fields.Many2one(comodel_name='budget.program', string='Proyecto', required=True, ondelete='cascade')

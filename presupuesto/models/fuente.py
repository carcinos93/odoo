# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Source(models.Model):
    _name = 'budget.source'
    _description = 'Fuente Financiamiento'


    sourceId = fields.Char(string='Código', size=6, readonly=True)
    name = fields.Char(string='Nombre Cooperante', size=120)
    contact = fields.Char(string='Representante Legal', size=80)
    contact_movile = fields.Char(string='Teléfono', size=12)
    contact_email = fields.Char(string='Email')
    logo = fields.Binary(string='Logo')
    address = fields.Text(string='Direccion')
    country = fields.Many2one(comodel_name='res.country', string='País')
    identification = fields.Char(string='Número de Identificacion', size=40)
    programs = fields.One2many(comodel_name='budget.program', inverse_name='sourceId', string='Proyectos', required=False)

    _sql_constraints = [
        ('number_plate_unique', 'UNIQUE(sourceId)', 'La Fuente de Financiamiento debe de ser única'),
    ]

    @api.model
    def create(self, vals):
        rec = super(Source, self).create(vals)
        strId = '000' + str(rec.id)
        rec['sourceId'] = strId[-3:]
        super(Source, self).write(rec)
        return rec







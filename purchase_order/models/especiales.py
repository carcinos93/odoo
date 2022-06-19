 # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import date, datetime
class especial1(models.Model):
    _name = 'budget.program'

    name = fields.Char('Nombre')

class especiales2(models.Model):
    _name = 'planificacion.actividad_producto_resultado'

    name = fields.Char('Nombre')

class especial3(models.Model):
    _name = 'budget.programa_line'

    name = fields.Char('Nombre')

class especial4(models.Model):
    _name = 'budget.linea'

    name = fields.Char('name')



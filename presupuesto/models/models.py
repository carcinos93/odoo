# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Line(models.Model):
    _name = 'budget.line'
    _description = 'Linea Presupuestaria'
    codeId = fields.Char(string='Código')
    name = fields.Char(string='Nombre Línea')
    codeId_parent = fields.Char(string='Línea Padre')
    is_mov = fields.Boolean(string='Tiene Movimiento')
    status = fields.Boolean(string='Habilitado')
    tipo = fields.Selection(string='Tipo insumo', selection=[('1', 'actividad'), ('2', 'gastos operativos'), ('3', 'ambos') ] )

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codeId, data.name)
            result.append((data.id, name,))
        return result

    _sql_constraints = [
        ('number_plate_unique', 'UNIQUE(codeId)', 'La línea debe de ser única'),
    ]






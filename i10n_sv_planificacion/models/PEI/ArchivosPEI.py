from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'planificacion.TableName'
    _description = 'Description'

    name = fields.Char()

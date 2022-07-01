from odoo import fields, models, api


class Empleado(models.Model):
    _name = 'i10n_sv_invoice.empleado'
    _description = 'Datos de empleado'
    _rec_name = 'nombre'

    nombre = fields.Char( string='Nombre',  required=False)
    apellido = fields.Char( string='Apellido',  required=False)
    fechaNacimiento = fields.Date(string='Fecha nacimiento', required=False)
    nacionalidad = fields.Many2one(comodel_name='res.country',string='Nacionalidad', required=False)
    habilidades = fields.One2many(comodel_name='i10n_sv_invoice.habilidades',inverse_name='empleado_ids',string='Habilidades', required=False)


class Habilidades(models.Model):
    _name = 'i10n_sv_invoice.habilidades'
    _description = 'Habilidades de empleado'
    _rec_name = 'habilidad'

    habilidad = fields.Char(string='Habilidad', required=False)
    empleado_ids = fields.Many2one(comodel_name='i10n_sv_invoice.empleado',string='Empleado_ids', required=False)
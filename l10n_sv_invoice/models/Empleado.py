from odoo import fields, models, api, exceptions
import datetime


class Empleado(models.Model):
    _name = 'i10n_sv_invoice.empleado'
    _description = 'Datos de empleado'
    _rec_name = 'nombre'

    @api.onchange('fechaNacimiento')
    def onchange_fecha(self):
        if self.fechaNacimiento:
            if self.fechaNacimiento > datetime.date.today():
                return {"warning": {'title': 'Error de validación',
                                'message': "Fecha nacimineto no puede ser mayor a la fecha actual"},
                                "value": {"fechaNacimiento": datetime.date.today()}}

    # Calculo total de meses
    def _compute_total_meses(self):
        di = self.fechafin - self.fechainicio
        if di == 0:
            self.totalmeses = 0
        else:
            self.totalmeses = di.total_seconds() / 60 / 60 / 24 / 30

    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    nombre = fields.Char(string='Nombre', required=False)
    apellido = fields.Char(string='Apellido', required=False)
    fechaNacimiento = fields.Date(string='Fecha nacimiento', required=False)
    nacionalidad = fields.Many2one(comodel_name='res.country', string='Nacionalidad', required=False)
    estado = fields.Selection(string='Estado',selection= [('empleado', 'Empleado'),('desempleado', 'Desempleado'), ],required=False, )

    habilidades = fields.One2many(comodel_name='i10n_sv_invoice.habilidades', inverse_name='empleado_ids',
                                  string='Habilidades', required=False)
    codigo = fields.Char(string='Codigo', required=False)
    fechainicio = fields.Date(string='Fecha inicio', required=True)
    fechafin = fields.Date(string='Fecha fin', required=True)
    salario = fields.Float(string='Salario',  required=False)
    totalmeses = fields.Integer(string='Total meses', required=False, compute=_compute_total_meses)

    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )

    @api.constrains('fechainicio')
    def _constrain_fechainicio(self):
        if self.fechainicio > self.fechafin:
            raise exceptions.ValidationError('Fecha inicio no puede ser mayor a la fecha fin')

    @api.constrains('fechafin')
    def _constrain_fechafin(self):
        if self.fechafin < self.fechainicio:
            raise exceptions.ValidationError('Fecha fin no puede ser menor a la fecha inicio')

    @api.model
    def create(self, vals):
        rec = super(Empleado, self).create(vals)
        rec['codigo'] = "0000" + str(rec['id'])
        super(Empleado, self).write(rec)
        return rec


# Habilidades
class Habilidades(models.Model):
    _name = 'i10n_sv_invoice.habilidades'
    _description = 'Habilidades de empleado'
    _rec_name = 'habilidad'

    habilidad = fields.Char(string='Habilidad', required=False)
    empleado_ids = fields.Many2one(comodel_name='i10n_sv_invoice.empleado', string='Empleado_ids', required=False)

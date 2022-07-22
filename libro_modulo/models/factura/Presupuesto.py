from odoo import fields, models, api


class Presupuesto(models.Model):
    _name = 'libro_modulo.presupuesto'
    _description = 'Description'

    presupuesto = fields.Many2one(comodel_name='budget.program',string='Presupuesto', required=False)
    presupuesto_detalle = fields.Many2one(comodel_name='budget.program_detail',string='Presupuesto detalle', required=False)
    presupuesto_anio = fields.Many2one(comodel_name='budget.program_year',string='Presupuesto año', required=False)
    monto = fields.Float(string='Monto',  required=False)
    campo = fields.Char(string='Campo', required=False)

    def write(self, vals):
        print(vals)
        rec = super(Presupuesto, self).write(vals)
        obj = {}
        if self.campo:
            obj[ self.campo ] = self.monto
            self.presupuesto_anio.write(obj)
        return rec

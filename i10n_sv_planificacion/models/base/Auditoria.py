from odoo import fields, models, api
from datetime import date, datetime

class BaseAuditoria(models.AbstractModel):
    _name = 'base.auditoria'
    _abstract = True

    @api.model
    def _default_user(self):
        return self._uid

    @api.model
    def _default_date(self):
        return datetime.today()

    usuarioAgrega = fields.Char(string='Usuario agrega',required=False, default=_default_user, invisible=True)
    fechaAgrega = fields.Datetime(string='Fecha agrega', required=False, invisible=True)


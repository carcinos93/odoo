from odoo import fields, models, api


class Periodo(models.Model):
    _name = 'planificacion.periodo'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    # _inherit = 'base.auditoria' # No funciona?

    @api.depends('ejes_estrategicos', 'ejes_estrategicos.totalPresupuesto')
    def _compute_total_presupuesto_asignado(self):
        for record in self:
            total = 0.0
            for eje in record.ejes_estrategicos:
                total += eje.totalPresupuesto
            record.totalPresupuesto = total

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    codigo = fields.Char(string='Código período', required=False, readonly=True)
    periodo = fields.Char(string='Período', required=True)
    titulo = fields.Char(string='Título', required=False)
    ejes_estrategicos = fields.One2many(comodel_name='planificacion.eje_estrategico', inverse_name='periodo_ids', string='Ejes estratégicos', copy=True, tracking=True)
    totalPresupuesto = fields.Float(string='Presupuesto total', required=False, compute=_compute_total_presupuesto_asignado)
    archivos = fields.One2many(comodel_name='planificacion.periodo_archivos', inverse_name='periodo_ids', string='Archivos', copy=True, tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)

    state = fields.Selection([('1', 'Formulación'),
                              ('2', 'Revisión y/o ajustes'),
                              ('3', 'Aprobación')], 'Estado', default='1', tracking=True)

    vigente = fields.Boolean(string='Vigente', required=False, default=True)
    esNuevo = fields.Boolean(string='Es nuevo', required=False, default=True)

    def reporte(self):
        url = "http://72.167.53.164:8080/birt/frameset?__report=planificacion_pei.rptdesign&id_periodo=%s" % str(self.id)
        return { 'name': 'Reporte',
                  'res_model': 'ir.actions.act_url',
                  'type' : 'ir.actions.act_url',
                  'target': 'blank',
                  'url' : url
               }

    def aprobar(self):
        super(Periodo, self).write( { "state" : "3" })
        self.state = "3"

    def siguiente_etapa(self):
        for env in self:
            env.write({'state': '2'})
        return True

    @api.model
    def create(self, vals):
        # vals['state'] = "2" # Al crearse para a revisión y/o ajustes
        rec = super(Periodo, self).create(vals)
        if 'codigo' not in vals:
            strId = '0' + str(rec.id)
            codigo = "%s-%s" % (strId, vals['periodo'])
            rec['codigo'] = codigo
            super(Periodo, self).write(rec)
        return rec

    def modificar(self):
        # super(Periodo, self).write({ "vigente": False })
        self.ensure_one()
        if self.vigente:
            self.env['planificacion.periodo'].browse(self.id).write( { "vigente": False } )
            self.env['planificacion.periodo'].browse(self.id).copy({'vigente': True, 'esNuevo': False })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Notificación',
                    'message': 'Modificación realizada de PEI "%s"' % self.titulo,
                    'sticky': False,
                    'target': 'new'
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Notificación',
                    'message': 'PEI "%s" ya ha sido modificado' % self.titulo,
                    'sticky': False,
                    'target': 'new'
                }
            }

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.titulo)
            result.append((data.id, name,))
        return result

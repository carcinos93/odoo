from odoo import fields, models, api, exceptions
from odoo.http import request

class PoaPob(models.Model):
    _name = 'planificacion.poa_pob'
    _rec_name = "nombreCorto"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    #@api.onchange('eje')
    #def onchange_eje(self):
    #    for rec in self:
    #        return { 'domain' : { 'objetivoEstrategico': [ ('ejes_estrategicos_ids.id', '=', rec.eje.id ) ]}}

    pei = fields.Many2one(comodel_name='planificacion.periodo', string='PEI', required=True)
    nombreCorto = fields.Char(string='Nombre', required=False)
    periodo = fields.Char(string='Periodo', size=4)
    fechaDesde = fields.Date(string='Desde')
    fechaHasta = fields.Date(string='Hasta')
    state = fields.Selection([('1', 'Formulación'),
                              ('2', 'Revisión y/o ajustes'),
                              ('3', 'Aprobación')], 'Estado', default='1', tracking=True)
    # objetivoEstrategico = fields.Many2one(comodel_name='planificacion.objetivo_estrategico', string='Objetivo estratégico',required=True)
    # codigoObjetivo = fields.Char(related="objetivoEstrategico.codigo")
    # descripcionObjetivo = fields.Text(related="objetivoEstrategico.descripcion")
    tipo = fields.Selection(string='Tipo',selection=[('1', 'POB'),('2', 'POA'), ], required=True, )
    vinculacion = fields.Text(string="Vinculación entre el objetivo estratégico de Cenpromype y el efecto")
    efectoImpactos = fields.One2many(comodel_name='planificacion.efecto_impacto',inverse_name='pobpob_ids',string=' Efecto impacto',required=False, copy=True)

    # resultados = fields.One2many(comodel_name='planificacion.resultado_efecto_impacto',inverse_name='pobpob_ids',string='Resultados',required=False)

    ejesEstrategicos = fields.One2many(comodel_name='planificacion.eje_estrategico_detalle',inverse_name='poa_ids',string=' Eje estratégico',required=False, copy=True)
    archivos = fields.One2many(comodel_name='planificacion.poa_pob_archivos',inverse_name='poa_ids',string=' Archivos',required=False, copy=True)

    fichaIndicadores = fields.One2many(comodel_name='planificacion.ficha_indicador',inverse_name='pobpob_ids',string=' Ficha indicador',required=False, copy=True)

    vigente = fields.Boolean(string='Vigente', required=False, default=True)
    esNuevo = fields.Boolean(string='Es nuevo', required=False, default=True)

    def aprobar(self):
        super(PoaPob, self).write( { "state" : "3" })
        self.state = "3"

    def reporte(self):
        base_url = request.httprequest.environ['HTTP_REFERER']
        base_url = base_url.replace(":8069/web", "")
        url = "%s:8080/birt/frameset?__report=planificacion_poa.rptdesign&id_poa=%s" % (base_url, str(self.id))
        # url = "http://72.167.53.164:8080/birt/frameset?__report=planificacion_poa.rptdesign&id_poa=%s" % str(self.id)
        return { 'name': 'Reporte',
                  'res_model': 'ir.actions.act_url',
                  'type' : 'ir.actions.act_url',
                  'target': 'blank',
                  'url' : url
               }


    def reporte_insumos(self):
        base_url = request.httprequest.environ['HTTP_REFERER']
        base_url = base_url.replace(":8069/web", "")
        url = "%s:8080/birt/frameset?__report=planificacion_poa_fuente.rptdesign&id_poa=%s" % ( base_url, str(self.id) )
        return { 'name': 'Reporte','res_model': 'ir.actions.act_url','type' : 'ir.actions.act_url','target': 'blank','url' : url }

    @api.model
    def create(self, vals):
        vals['state'] = "2"  # Al crearse para a revisión y/o ajustes
        rec = super(PoaPob, self).create(vals)
        return rec

    def modificar(self):
        # super(Periodo, self).write({ "vigente": False })
        self.ensure_one()
        if self.vigente:
            self.env['planificacion.poa_pob'].browse(self.id).write( { "vigente": False } )
            self.env['planificacion.poa_pob'].browse(self.id).copy({'vigente': True, 'esNuevo': False })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Notificación',
                    'message': 'Modificación realizada de POA "%s"' % self.nombreCorto,
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
                    'message': 'POA "%s" ya ha sido modificado' % self.nombreCorto,
                    'sticky': False,
                    'target': 'new'
                }
            }
        #return super(Periodo, self).copy(default={ "vigente": True })
        #return super(Periodo, self).write({ "vigente": False })

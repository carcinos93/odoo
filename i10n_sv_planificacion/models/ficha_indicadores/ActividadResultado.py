from odoo import fields, models, api


class ActividadResultado(models.Model):
    _name = 'planificacion.actividad_resultado'
    _description = 'Actividades para lograr el resultado'
    # _inherit = 'base.auditoria'

    @api.onchange('objetivoEstrategico')
    def onchange_objetivo(self):
        for rec in self:
            return {'domain': {'meta': [('objetivo_estrategico_ids.id', '=', rec.objetivoEstrategico.id)],
                               'resultado': [('objetivoEstrategico_ids.id', '=', rec.objetivoEstrategico.id)]
                               }}

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    objetivoEstrategico = fields.Many2one(comodel_name='planificacion.objetivo_estrategico', string='Objetivo estratégico', required=False)
    meta = fields.Many2one(comodel_name='planificacion.meta', string='Meta', required=False)
    resultado = fields.Many2one(comodel_name='planificacion.resultado', string='Resultado', required=False)
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True, default=_compute_default_currencyid)
    actividadesResultado = fields.Text(string="Actividades necesarias para lograr el resultado", required=True)
    descripcion = fields.Text(string="Descripción", required=False)
    indicador = fields.Char(string="Indicador", required=False)
    metaProgramada = fields.Char(string="Meta programada", required=False)
    fechaConsecucion = fields.Date(string='Fecha estimada de consecución', required=False)
    pesoContribucion = fields.Char(string="Peso respecto a su contribución al producto", required=False)
    tipoProducto = fields.Char(string="Tipo de producto", required=False)
    tipoProductoConocimiento = fields.Char(string="Tipo de producto de conocimiento", required=False)
    numeroProductoConocimiento = fields.Char(string="N° de producto de conocimiento", required=False)
    grupoMeta = fields.Char(string="Grupo meta", required=False)
    numeroGrupoMeta = fields.Char(string="N° de Grupo meta", required=False)
    paisGrupoMeta = fields.Char(string="País Grupo Meta", required=False)
    insumos = fields.Float(string="Monto", required=False)
    proyecto = fields.Char(string="Proyecto", required=False) # seleccionar proyecto
    servicio = fields.Char(string="Servicio que mejora", required=False) # seleccionar proyecto
    tipoPsde = fields.Char(string="Tipo de PSDE que participa en la mejora", required=False) # seleccionar proyecto
    numeroPsde = fields.Char(string="N° de PSDE que participa en la mejora", required=False)
    paisPsde = fields.Char(string="País de PSDE que participa en la mejora", required=False)
    objetivoConvenio = fields.Text(string="Objetivo del convenio constitutivo", required=False)
    ejeAgenda = fields.Char(string="Eje de la agenda", required=False)
    # vinculacionEntregaFondos = fields.Boolean(string="Vinculación con entrega de fondos", required=False)
    vinculacionEntregaFondos = fields.Selection( string='Vinculación con entrega de fondos',selection=[('1', 'SI'), ('0', 'NO'), ],required=False, )

    # Modelo padre
    indicador_ids = fields.Many2one(comodel_name='planificacion.ficha_indicador', string='Ficha indicador', required=False)
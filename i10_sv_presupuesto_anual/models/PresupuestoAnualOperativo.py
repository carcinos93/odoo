from odoo import fields, models, api, exceptions


class PresupuestoOperativo(models.Model):
    _name = 'budget.presupuesto_operativo'
    _description = 'Presupuesto anual gasto operativo'

    @api.onchange('insumo')
    def onchange_insumo(self):
        for rec in self:
            return {'domain': {'proyecto': [('program_details_ids.lineId', '=', rec.insumo.id)]}}

    @api.onchange('proyecto')
    def onchange_proyecto(self):
        for rec in self:
            return {'domain': {'detalleProyecto': [('details_id.id', '=', rec.proyecto.id), ('lineId.tipo', 'in', ('2','3') )]}}

    @api.onchange('montoAsignado')
    def onchange_montoAsignado(self):
        if self.detalleProyecto is None:
            raise exceptions.ValidationError('Debe seleccionar un presupuesto de proyecto')
        if self.montoAsignado > self.detalleProyecto.available:
            raise exceptions.ValidationError('El monto asignado no puede ser mayor al disponible')


    @api.depends('detalle', 'detalle.gastoDirecto', 'detalle.gastoIndirecto')
    def _total_gasto(self):
        total = 0.0
        for item in self.detalle:
            total += item.gastoDirecto + item.gastoIndirecto
        self.totalDetalle = total

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    poa = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA', required=True)
    periodo = fields.Char(related='poa.periodo', string='Periodo')
    insumo = fields.Many2one(comodel_name='budget.line', string='Insumo', required=True)
    proyecto = fields.Many2one(comodel_name='budget.program', string='Proyecto', required=True)
    detalleProyecto = fields.Many2one(comodel_name='budget.program_detail', string='Detalle de proyecto', required=True)
    montoFuenteFinanciamiento = fields.Float(related='detalleProyecto.available', string='Monto disponible')
    reservadoFuenteFinanciamiento = fields.Float(related='detalleProyecto.reservado', string='Reservado')
    comprometidoFuenteFinanciamiento = fields.Float(related='detalleProyecto.total_amount', string='Comprometido')
    montoAsignado = fields.Float(string='Monto asignado', required=False)
    detalle = fields.One2many(comodel_name='budget.presupuesto_operativo_detalle',inverse_name='presupuestoAnual_ids',string='Detalle', copy=True)
    totalDetalle = fields.Float(string='Total gasto', store=True, readonly=True, compute=_total_gasto)
    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )


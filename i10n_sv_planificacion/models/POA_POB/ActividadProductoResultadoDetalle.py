from odoo import fields, models, api, exceptions


class ActividadProductoResultadoDetalle(models.Model):
    _name = 'planificacion.actividad_producto_resultado_detalle'
    # _inherit = 'base.auditoria'
    #@api.onchange('insumo')
    #def onchange_insumo(self):
    #    for rec in self:
    #        return { 'domain' : { 'fuenteFinanciamiento': [ ('program_details_ids.lineId', '=', rec.insumo.id )]}}

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    @api.onchange('detalleFuenteFinanciamiento')
    def onchange_detalleFuenteFinanciamiento(self):
        for rec in self:
            return { 'domain' : { 'insumo': [ ('id', '=', rec.detalleFuenteFinanciamiento.lineId.id )]}}

    #@api.onchange('fuenteFinanciamiento')
    #def onchange_fuenteFinanciamiento(self):
    #    for rec in self:
    #        return {'domain': {'detalleFuenteFinanciamiento': [('details_id.id', '=', rec.fuenteFinanciamiento.id), ('lineId.tipo', 'in', ('1', '3'))]}}

    @api.onchange('monto1', 'monto2','monto3', 'monto4')
    def onchange_montos(self):
        total = self.monto1 + self.monto2 + self.monto3 + self.monto4
        if total > 0 and total > self.proyecto_anio.amount:
            return { "warning": { 'title': 'Error de validación', 'message': 'Total trimestre es mayor a monto total'},
                     'value': {'monto1': 0.00 ,'monto2': 0.00, 'monto3' : 0.00, 'monto4': 0.00 }}


    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id


    def _compute_default_monto(self):
        return 0.00



    @api.depends('monto1', 'monto2', 'monto3', 'monto4', 'reservado', 'comprometido')
    def _compute_total_asignado(self):
        for record in self:
            monto1 = 0 if record.monto1 is None else record.monto1
            monto2 = 0 if record.monto2 is None else record.monto2
            monto3 = 0 if record.monto3 is None else record.monto3
            monto4 = 0 if record.monto4 is None else record.monto4
            reservado = 0 if record.reservado is None else record.reservado
            comprometido = 0 if record.comprometido is None else record.comprometido
            total = monto1 + monto2 + monto3 + monto4
            disponible = total - reservado - comprometido
            record.update({'montoAsignado': total, 'disponible': disponible})

    fuenteFinanciamiento = fields.Many2one(comodel_name='budget.program', string='Fuente de financiamiento', required=False)
    detalleFuenteFinanciamiento = fields.Many2one(comodel_name='budget.program_detail', string='Presupuesto de proyecto', required=False)
    proyecto_anio = fields.Many2one('budget.program_year', string='Año')
    disponible = fields.Float(string='Monto disponible', required=False, compute=_compute_total_asignado, store=True)
    reservado = fields.Float(string='Reservado', required=False, default=0.00)
    comprometido = fields.Float(string='Comprometido', required=False, default=0.00)
    disponibleFuenteFinanciamiento = fields.Float(related='detalleFuenteFinanciamiento.available', string='Monto disponible', readonly=True)
    montoTotalFuenteFinanciamiento = fields.Float(related='proyecto_anio.amount', string='Monto total', readonly=True)
    reservadoFuenteFinanciamiento = fields.Float(related='detalleFuenteFinanciamiento.reservado', string='Reservado',readonly=True)
    comprometidoFuenteFinanciamiento = fields.Float(related='detalleFuenteFinanciamiento.total_amount', string='Comprometido', readonly=True)
    insumo = fields.Many2one(comodel_name='budget.line', string='Insumo', required=True)
    montoAsignado = fields.Float(string='Total trimestre', required=False, compute=_compute_total_asignado, store=True)
    monto1 = fields.Float(string='Monto Trimestre I', required=False, default=_compute_default_monto)
    monto2 = fields.Float(string='Monto Trimestre II', required=False, default=_compute_default_monto)
    monto3 = fields.Float(string='Monto Trimestre III', required=False, default=_compute_default_monto)
    monto4 = fields.Float(string='Monto Trimestre IV', required=False, default=_compute_default_monto)
    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )
    # Modelo padre
    actividad_resultado_ids = fields.Many2one(comodel_name='planificacion.actividad_producto_resultado', string='Actividad producto resultado', required=True, ondelete='cascade')
    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.insumo.name, data.fuenteFinanciamiento.name)
            result.append((data.id, name,))
        return result

    @api.model
    def create(self, vals):
        rec = super(ActividadProductoResultadoDetalle, self).create(vals)
        if rec.proyecto_anio:
            rec.proyecto_anio.write({'inicial': rec.montoAsignado})
        return rec

    def write(self, vals):
        rec = super(ActividadProductoResultadoDetalle, self).write(vals)
        if self.proyecto_anio:
            self.proyecto_anio.write({'inicial': self.montoAsignado })
        return rec


    # _rec_name = 'nombre del campo que desea que se muestre' # listas
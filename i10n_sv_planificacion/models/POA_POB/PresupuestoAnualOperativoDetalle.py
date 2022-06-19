from odoo import fields, models, api, exceptions


class PresupuestoOperativoDetalle(models.Model):
    _name = 'planificacion.presupuesto_operativo_detalle'
    _description = 'Detalle presupuesto anual gasto operativo'

    def _default_gasto(self):
        return 0.00

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )
    #Modelo padre
    presupuestoAnual_ids = fields.Many2one(comodel_name='planificacion.presupuesto_operativo',
                                           string='Presupuesto anual gasto operativo', ondelete='cascade')
    gastoDirecto = fields.Float(string='Gasto directo', default=_default_gasto)

    gastoDirecto1 = fields.Float(string='Trimestre I', default=_default_gasto)
    gastoDirecto2 = fields.Float(string='Trimestre II', default=_default_gasto)
    gastoDirecto3 = fields.Float(string='Trimestre III', default=_default_gasto)
    gastoDirecto4 = fields.Float(string='Trimestre IV', default=_default_gasto)

    gastoIndirecto = fields.Float(string='Gasto indirecto', default=_default_gasto)
    gastoIndirecto1 = fields.Float(string='Trimestre I', default=_default_gasto)
    gastoIndirecto2 = fields.Float(string='Trimestre II', default=_default_gasto)
    gastoIndirecto3 = fields.Float(string='Trimestre III', default=_default_gasto)
    gastoIndirecto4 = fields.Float(string='Trimestre IV', default=_default_gasto)

    @api.onchange('gastoDirecto1', 'gastoDirecto2', 'gastoDirecto3', 'gastoDirecto4')
    def onchange_gastoDirecto(self):
        total = self.gastoDirecto1 + self.gastoDirecto2 + self.gastoDirecto3 + self.gastoDirecto4
        self.gastoDirecto = total
        self.validarMonto()

    @api.onchange('gastoIndirecto1', 'gastoIndirecto2', 'gastoIndirecto3', 'gastoIndirecto4')
    def onchange_gastoIndirecto(self):
        total = self.gastoIndirecto1 + self.gastoIndirecto2 + self.gastoIndirecto3 + self.gastoIndirecto4
        self.gastoIndirecto = total
        self.validarMonto()

    def validarMonto(self):
        montoDisponible = self.presupuestoAnual_ids.montoAsignado
        gastoTotal = self.gastoDirecto + self.gastoIndirecto
        if gastoTotal > 0.00:
            if gastoTotal > montoDisponible:
                raise exceptions.ValidationError('El gasto no puede ser superior al monto disponible')
            else:
                total = gastoTotal # inicializamos el total ya que el loop no toma en cuenta el formulario actual abierto
                for detalle in self.presupuestoAnual_ids.detalle:
                    # print( (str(detalle.id), (self._origin.id) ,str(self.id), str(detalle._origin.id)) )
                    # Esta condicion evitar evaluar el registro actual ubicado en el detalle
                    if str(detalle.id) != str(self.id) or str(detalle._origin.id) != str(self._origin.id):
                        # se verifica si el registro existe en bd o esta solamente cargado en formulario (virtual)
                        if str(detalle.id).find("virtual") >= 0 or str(detalle._origin.id).isnumeric():
                            total += detalle.gastoDirecto + detalle.gastoIndirecto
                if total > montoDisponible:
                    raise exceptions.ValidationError('La suma total no puede ser mayor al monto disponible')

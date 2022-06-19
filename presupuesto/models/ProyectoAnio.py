from odoo import fields, models, api, exceptions
from datetime import  datetime


def compute_years():
    limite = range(-2, 5)
    data = []
    for n in limite:
        y = datetime.now().year + n
        data.append( (y, str(y) ))
    print(data)
    return data


class ProyectoAnio(models.Model):
    _name = 'budget.program_year'
    _description = 'monto del proyecto por año'

    #def monto_poa(self):
    #    actividadProducto = self.env['planificacion.actividad_producto_resultado_detalle'].search([( 'proyecto_anio.id', '=', self.id )])
    #    print(actividadProducto)
    #    if actividadProducto:
    #        self.inicial = actividadProducto.montoAsignado
    #    else:
    #        self.inicial = 0

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    years = [(str(num), str(num)) for num in range(datetime.now().year -2 , datetime.now().year + 5)]
    year = fields.Selection( string='Año', selection=years, required=False, )
    # year = fields.Char(string='Año', required=True, size=4)
    inicial = fields.Float(string='Monto POA', default=0.00)
    ajustado = fields.Float(string='Ajustado')
    ejecucion = fields.Float(string='Ejecución real')
    comprometido = fields.Float(string='Comprometido')
    amount = fields.Float(string='Monto', required=True)
    reservado = fields.Float(string='Reservado')
    adjust_up = fields.Float(string='Aumento')
    adjust_down = fields.Float(string='Disminucion')
    available = fields.Float(string='Disponible')
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True, default=_compute_default_currencyid)
    program_details_id = fields.Many2one(comodel_name='budget.program_detail', string='Presupuesto de Proyectos por Cooperante')

    @api.onchange('amount')
    def amount_change(self):
        msj = self.validarMonto()
        if msj is not None:
            return msj

    def validarMonto(self):
        montoDisponible = self.program_details_id.amount
        gastoTotal = self.amount
        if gastoTotal > 0.00:
            if gastoTotal > montoDisponible:
                # raise exceptions.ValidationError('Monto no puede ser superior al monto disponible')
                return {"warning": {'title': 'Error de validación','message': 'El gasto no puede ser superior al monto disponible'}, 'value': {'amount': 0.00}}
            else:
                total = gastoTotal # inicializamos el total ya que el loop se evita tomar en cuenta el formulario actual abierto
                for detalle in self.program_details_id.proyectos_anio:
                    # print((str(detalle.id), (self._origin.id), str(self.id), str(detalle._origin.id), detalle.amount))
                    # Esta condicion evitar evaluar el registro actual ubicado en el detalle
                    if str(detalle.id) != str(self.id) or str(detalle._origin.id) != str(self._origin.id):
                        # se verifica si el registro existe en bd o que no se virutal (temporal en formulario)
                        if str(detalle.id).find("virtual") == 0 or str(detalle._origin.id).isnumeric():
                            total += detalle.amount
                if total > montoDisponible:
                    # raise exceptions.ValidationError('La suma total no puede ser mayor al monto disponible')
                    return {"warning": {'title': 'Error de validación', 'message': 'La suma total no puede ser mayor al monto disponible'},'value': {'amount': 0.00}}
        return None

    def name_get(self):
        result = []
        for data in self:
            # name = '%s (%.2f)' % (data.year, data.amount)
            name = '%s' % data.year
            result.append((data.id, name,))
        return result

    # @api.model
    # def write(self, vals):
    #     if 'amount' in vals:
    #         suma = 0
    #         programaDetalle = self.env['budget.program_year'].search(
    #             [('program_details_id.id', '=', str(self.program_details_id.id))])
    #         for detalle in programaDetalle:
    #             if self.id != detalle.id:
    #                 suma += detalle.amount
    #         program = self.env['budget.program_detail'].search([('id', '=', str(self.program_details_id.id))])
    #         total = suma
    #         amount_program = program.amount
    #
    #         if total + vals['amount'] > amount_program:
    #             raise exceptions.ValidationError(
    #                 'La suma total no puede superar al presupuesto %.2f' % amount_program)
    #     rec = super(ProyectoAnio, self).write(vals)
    #     return rec
    #
    # @api.model
    # def create(self, vals):
    #     if 'amount' in vals:
    #         suma = 0
    #         programaDetalle = self.env['budget.program_year'].search(
    #             [('program_details_id.id', '=', str(vals['program_details_id']))])
    #         for detalle in programaDetalle:
    #             suma += detalle.amount
    #         program = self.env['budget.program_detail'].search([('id', '=', str(vals['program_details_id']))])
    #         total = suma
    #         amount_program = program.amount
    #         if total + vals['amount'] > amount_program:
    #             raise exceptions.ValidationError(
    #                 'La suma total no puede superar al presupuesto %.2f' % amount_program)
    #     rec = super(ProyectoAnio, self).create(vals)
    #     return rec


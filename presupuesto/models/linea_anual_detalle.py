# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class ProgramaDetalle(models.Model):
    _name = 'budget.program_detail'
    _description = 'Presupuesto de Proyectos por Cooperante'

    # _rec_name = 'description1'
    @api.depends('proyectos_anio', 'proyectos_anio.amount')
    def _compute_program_anio(self):
        for record in self:
            total = 0.0
            for item in record.proyectos_anio:
                total += item.amount
            record.total_amount = total

    @api.onchange('amount')
    def _amount_change(self):
        for record in self:
            return {'value': {'available': record.amount}}

    @api.onchange('ajustado')
    def _ajustado_change(self):
        for record in self:
            return {'value': { 'available': record.ajustado }}

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    lineId = fields.Many2one('budget.line', string='Insumo', required=True)
    lineName = fields.Char(related='lineId.name', string='Insumo')
    level1 = fields.Char(string='Nivel 1')
    description1 = fields.Char(string='Descripción 1')

    level2 = fields.Char(string='Nivel 2')
    description2 = fields.Char(string='Descripción 2')

    level3 = fields.Char(string='Nivel 3')
    description3 = fields.Char(string='Descripción 3')

    level4 = fields.Char(string='Nivel 4')
    description4 = fields.Char(string='Descripción 4')

    level5 = fields.Char(string='Nivel 5')
    description5 = fields.Char(string='Descripción 5')

    currency_id = fields.Many2one('res.currency', 'Currency', required=False,
                                  default=_compute_default_currencyid)

    amount = fields.Float(string='Monto inicial')

    ajustado = fields.Float(string='Ajustado')
    ejecucion = fields.Float(string='Ejecución real')
    comprometido = fields.Float(string='Comprometido')
    reservado = fields.Float(string='Reservado')
    adjust_up = fields.Float(string='Aumento')
    adjust_down = fields.Float(string='Disminucion')
    available = fields.Float(string='Disponible')
    total_amount = fields.Float(string='Total de insumo', store=True, compute=_compute_program_anio)
    # Modelo padre
    details_id = fields.Many2one('budget.program', string='Programa', ondelete='cascade')
    numberLines = fields.Integer(related='details_id.numberLines', string="")
    proyectos_anio = fields.One2many(comodel_name='budget.program_year', inverse_name='program_details_id',
                                     string='Monto del proyecto por año', copy=True)

    def name_get(self):
        result = []
        for data in self:
            if data.numberLines:
                formato = "%s %s"
                sw = {
                    1: formato % (data.level1, data.description1),
                    2: formato % (data.level2, data.description2),
                    3: formato % (data.level3, data.description3),
                    4: formato % (data.level4, data.description4),
                    5: formato % (data.level5, data.description5)
                }
                name = sw.get(data.numberLines, formato % (data.level1, data.description1))
            else:
                name = '%s %s' % (data.level1, data.description1)
            result.append((data.id, name,))
        return result

    @api.constrains('amount')
    def amount_change(self):
        if self.amount <= 0:
            raise exceptions.ValidationError('Monto no puede ser menor o igual a cero')

    @api.model
    def create(self, vals):
        vals['available'] = vals['amount']
        if 'amount' in vals:
            suma = 0
            programaDetalle = self.env['budget.program_detail'].search(
                [('details_id.id', '=', str(vals['details_id']))])
            for detalle in programaDetalle:
                suma += detalle.amount
            program = self.env['budget.program'].search([('id', '=', str(vals['details_id']))])
            total = suma
            amount_program = program.amount
            if total + vals['amount'] > amount_program:
                raise exceptions.ValidationError(
                    'La suma total no puede superar al presupuesto %.2f' % amount_program)
        rec = super(ProgramaDetalle, self).create(vals)
        return rec

    def write(self, vals):
        if 'amount' in vals:
            suma = 0
            programaDetalle = self.env['budget.program_detail'].search(
                [('details_id.id', '=', str(self.details_id.id))])
            for detalle in programaDetalle:
                if self.id != detalle.id:
                    suma += detalle.amount
            program = self.env['budget.program'].search([('id', '=', str(self.details_id.id))])
            total = suma
            amount_program = program.amount
            if total + vals['amount'] > amount_program:
                raise exceptions.ValidationError('La suma total no puede superar al presupuesto %.2f' % amount_program)
        rec = super(ProgramaDetalle, self).write(vals)
        return rec

    def default_get(self, fields):
        rec = super(ProgramaDetalle, self).default_get(fields)
        items = self._context.get('items')
        if items:
            filtrados = list(filter(lambda x: x[0] != 2, items)) #Se filtran para no tomar en cuenta los registros con estado "virtual" borrado
            total_items = len( filtrados )
            if total_items > 0:
                ultimo = filtrados[total_items - 1]
                if ultimo[0] in (0, 1):  # Registro nuevo o esta modificado, pero no guardado en la bd
                    detalle = ultimo[2]  # si no esta guardado los valores se almacenan esta la posicion 2
                    rec.update(
                        level1=detalle.get('level1', None),
                        description1=detalle.get('description1', None),
                        level2=detalle.get('level2', None),
                        description2=detalle.get('description2', None),
                        level3=detalle.get('level3', None),
                        description3=detalle.get('description3', None),
                        level4=detalle.get('level4', None),
                        description4=detalle.get('description4', None),
                        level5=detalle.get('level5', None),
                        description5=detalle.get('description5', None))
                elif ultimo[0] == 4: # Registro que guardado en bd
                    detalle = self.env['budget.program_detail'].browse( ultimo[1] ).exists()
                    rec.update(
                        level1=detalle.level1,
                        description1=detalle.description1,
                        level2=detalle.level2,
                        description2=detalle.description2,
                        level3=detalle.level3,
                        description3=detalle.description3,
                        level4=detalle.level4,
                        description4=detalle.description4,
                        level5=detalle.level5,
                        description5=detalle.description5)
        return rec

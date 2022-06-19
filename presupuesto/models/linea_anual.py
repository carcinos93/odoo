# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime


class Program(models.Model):
    _name = 'budget.program'
    _description = 'Proyectos'

    # _rec_name = 'name'
    # _inherit = ['portal.mixin']
    # Función que nos devuelve al usuario que está logueado
    @api.model
    def _default_user(self):
        return self._uid

    # Función que nos devuelve el dia actual
    @api.model
    def _default_date(self):
        return datetime.today()

    # Funciones que cambian el estado del gasto
    def emitir_programa(self):
        for env in self:
            env.write({'state': '1'})
        return True

    def auth_programa(self):
        for env in self:
            env.write({'state': '2'})
        return True

    def fin_programa(self):
        for env in self:
            env.write({'state': '3'})
        return True

    @api.depends('program_details_ids', 'program_details_ids.amount')
    def _compute_program_details_amount(self):
        for record in self:
            total = 0.0
            for items in record.program_details_ids:
                total += items.amount
            record.total_amount = total

    @api.depends('program_details_ids', 'program_details_ids.reservado')
    def _compute_program_details_reservado(self):
        for record in self:
            total = 0.0
            for items in record.program_details_ids:
                total += items.reservado
                record.total_reservado = total

    @api.depends('program_details_ids', 'program_details_ids.available')
    def _compute_program_details_available(self):
        for record in self:
            total = 0.0
            for items in record.program_details_ids:
                total += items.available
            record.total_available = total

    @api.depends('program_details_ids', 'program_details_ids.amount')
    def _compute_total_insumo(self):
        for record in self:
            total_actividad = total_operativo = total_amount = 0.00
            for item in self.program_details_ids:
                total_operativo += item.amount if item.lineId.tipo == "2" else 0  # gastos operativos
                total_actividad += item.amount if item.lineId.tipo == "1" else 0  # actividad
                total_amount += item.amount
            record.update(
                {'total_operativo': total_operativo, 'total_actividad': total_actividad, 'total_amount': total_amount})

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    total_amount = fields.Float(string='Total programa', store=True, readonly=True, compute=_compute_total_insumo)
    total_operativo = fields.Float(string='Total, gastos operativos', store=True, readonly=True,
                                   compute=_compute_total_insumo)
    total_actividad = fields.Float(string='Total, insumos por actividad', store=True, readonly=True,
                                   compute=_compute_total_insumo)
    total_reservado = fields.Float(string='Total reservado', store=True, readonly=True,
                                   compute=_compute_program_details_reservado)
    total_available = fields.Float(string='Total disponible', store=True, readonly=True,
                                   compute=_compute_program_details_available)
    # Datos del Gasto
    meses = [('1', 'enero'), ('2', 'febrero'), ('3', 'marzo'), ('4', 'abril'), ('5', 'mayo'), ('6', 'junio'),
             ('7', 'julio'), ('8', 'agosto'), ('9', 'septiembre'), ('10', 'octubre'), ('11', 'noviembre'),
             ('12', 'diciembre')]

    # Datos generales del programa
    programId = fields.Char(string='Código', size=20)
    sourceId = fields.Many2one('budget.source', string='Cooperante')
    bank = fields.Many2one('res.bank', string='Banco')
    bankAccount = fields.Char(string='Cuenta bancaria')
    saldoBanco = fields.Float(string='Saldos')
    name = fields.Text(string='Descripción')
    shortName = fields.Char(string='Nombre corto')
    dateFrom = fields.Date(string='Fecha desde')
    dateTo = fields.Date(string='Fecha hasta')
    amount = fields.Float(string='Presupuesto')
    numberLines = fields.Integer(string='Número de líneas de nivel y descripción habilitadas', required=True, default=1)
    coordinador = fields.Many2one('hr.employee', 'Coordinadora(or) de proyecto')
    gestor = fields.Many2one('hr.employee', 'Gestora/or administrativa(o)')
    state = fields.Selection([('1', 'Formulación'), ('2', 'Revisión y/o ajustes'), ('3', 'Aprobación')], default='1', string='Estado')
    esCopia = fields.Boolean(string='Es copia', required=False, default=False)

    # Generalidades del proyecto
    logicaIntervencion = fields.Text(string="Lógica de la intervención", required=False)
    indicadoresObjetivamente = fields.Text(string="Indicadores objetivamente", required=False)
    fuenteVerificacion = fields.Text(string="Fuente de verificación", required=False)
    hipotesis = fields.Text(string="Hipótesis", required=False)
    riesgos = fields.Text(string="Riesgos", required=False)

    # Moneda
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)
    # active = ocultar registro
    # Detalle del Programa
    program_details_ids = fields.One2many('budget.program_detail', 'details_id', string='Detalle del Proyecto', copy=True)
    files = fields.One2many('budget.program_files', 'program_ids', string='Versiones de presupuesto', copy=True)
    documentos = fields.One2many('budget.program_documentos', 'program_ids', string='Documentos', copy=True)
    cuentasBaco = fields.One2many('budget.cuenta_banco', 'program_ids', string='Cuentas de banco', copy=True)
    filtro = fields.Char(string='Filtro', required=False, store=False, default="")


    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.programId, data.name)
            result.append((data.id, name,))
        return result

    def modificar(self):
        self.ensure_one()
        self.env['budget.program'].browse(self.id).copy({'esCopia': True})
        self.env['budget.program'].browse(self.id).write({"state": "2"})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Notificación',
                'message': 'Modificación de presupuesto realizada',
                'sticky': False,
                'target': 'new',
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            }
        }

    @api.model
    def create(self, vals):
        vals['state'] = '2'
        rec = super(Program, self).create(vals)
        if 'programId' not in vals:
            strId = '000' + str(rec.id)
            rec['programId'] = strId[-3:]
            super(Program, self).write(rec)
        return rec


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

    lineId = fields.Many2one('budget.line', string='Insumo')
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

    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)

    amount = fields.Float(string='Monto inicial')

    ajustado = fields.Float(string='Ajustado')
    ejecucion = fields.Float(string='Ejecución real')
    comprometido = fields.Float(string='Comprometido')
    reservado = fields.Float(string='Reservado')
    adjust_up = fields.Float(string='Aumento')
    adjust_down = fields.Float(string='Disminucion')
    available = fields.Float(string='Disponible')
    total_amount = fields.Float(string='Total programa', store=True, readonly=True, compute=_compute_program_anio)
    # Modelo padre
    details_id = fields.Many2one('budget.program', string='Programa', ondelete='cascade')
    numberLines = fields.Integer(related='details_id.numberLines', string="")
    proyectos_anio = fields.One2many(comodel_name='budget.program_year', inverse_name='program_details_id',
                                     string='Monto del proyecto por año', copy=True)

    def name_get(self):
        result = []
        for data in self:
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

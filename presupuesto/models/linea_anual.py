# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import datetime


class Program(models.Model):
    _name = 'budget.program'
    _description = 'Proyectos'

    # _rec_name = 'name'
    # _inherit = ['portal.mixin']
    # Función que nos devuelve al usuario que está logueado
    def _default_user(self):
        return self._uid

    # Funciones que cambian el estado del gasto

    def siguiente_etapa(self):
        for env in self:
            env.write({'state': '2'})
        return True

    def aprobacion(self):
        for env in self:
            env.write({'state': '3'})
        return True

    def reestablecer(self):
        for env in self:
            env.write({"activo": True})

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
            lang = self._context.get('lang', 'es_MX')
            res_lang = self.env['res.lang'].search([('code', '=', lang)])
            lang_obj = None
            if res_lang:
                for obj in res_lang:
                    lang_obj = obj
            total_actividad = total_operativo = total_amount = 0.00
            # Niveles actuales
            data_table = {'nivel 1': 0, 'nivel 2': 0, 'nivel 3': 0, 'nivel 4': 0, 'nivel 5': 0}

            for item in record.program_details_ids:
                total_operativo += item.amount if item.lineId.tipo == "2" else 0  # gastos operativos
                total_actividad += item.amount if item.lineId.tipo == "1" else 0  # actividad
                total_amount += item.amount
                # Si hay valor en el nivel se acumula ( aplica para el resto de niveles)

                if item.level5:
                    data_table['nivel 5'] += item.amount
                if item.level4:
                    data_table['nivel 4'] += item.amount
                if item.level3:
                    data_table['nivel 3'] += item.amount
                if item.level2:
                    data_table['nivel 2'] += item.amount
                if item.level1:
                    data_table['nivel 1'] += item.amount

                # if item.level5:
                #     data_table['nivel 5'] += item.amount
                # elif item.level4:
                #     data_table['nivel 4'] += item.amount
                # elif item.level3:
                #     data_table['nivel 3'] += item.amount
                # elif item.level2:
                #     data_table['nivel 2'] += item.amount
                # elif item.level1:
                #     data_table['nivel 1'] += item.amount

            html = "<table class='table table-bordered'>"
            for key in data_table: # Recorrer cada nivel
                valor = data_table[key]
                formatoMonto = "%.2f" % valor  # Formato por defecto
                if lang_obj:
                    formatoMonto = lang_obj.format("%.2f", valor, True, True)
                html += "<tr><td> <b>%s:</b> %s </td> </tr>" % (key, formatoMonto)
            html += "</table>"
            # Se actualizan los valores de totales y el html del total por nivel
            record.update(
                {'total_operativo': total_operativo, 'total_actividad': total_actividad,
                 'total_amount': total_amount, 'totalesHTML': html})

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

    # Campo utilizado para generar suma de grupos por nivel en HTML
    totalesHTML = fields.Text(string="Total por nivel", required=False, compute=_compute_total_insumo, store=True)
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
    # numberLines = fields.Integer(string='Número de líneas de nivel y descripción habilitadas', required=True, default=1)
    numberLines = fields.Selection(string='Número de líneas de nivel y descripción habilitadas',
                                   selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                   required=False)

    coordinador = fields.Many2one('hr.employee', 'Coordinadora(or) de proyecto')
    gestor = fields.Many2one('hr.employee', 'Gestora/or administrativa(o)')
    state = fields.Selection([('1', 'Formulación'), ('2', 'Revisión y/o ajustes'), ('3', 'Aprobación')], default='1',
                             string='Estado')
    esCopia = fields.Boolean(string='Es copia', required=False, default=False)

    # Generalidades del proyecto
    logicaIntervencion = fields.Text(string="Lógica de la intervención", required=False)  # Quitar
    indicadoresObjetivamente = fields.Text(string="Indicadores objetivamente", required=False)
    fuenteVerificacion = fields.Text(string="Fuente de verificación", required=False)  # Quitar
    hipotesis = fields.Text(string="Hipótesis", required=False)
    riesgos = fields.Text(string="Riesgos", required=False)
    paisesBeneficiario = fields.Many2many('res.country', string='Países beneficiarios')
    objetivoGeneral = fields.Text(string="Objetivo general del proyecto", required=False)
    objetivoEspecifico = fields.Text(string="Objetivos específicos", required=False)
    ods = fields.Char(string="ODS", required=False)
    justificacion = fields.Text(string="Justificación del proyecto", required=False)
    # Moneda
    currency_id = fields.Many2one('res.currency', 'Currency', required=False, readonly=True,
                                  default=_compute_default_currencyid)
    # active = ocultar registro
    # Detalle del Programa
    program_details_ids = fields.One2many('budget.program_detail', 'details_id', string='Detalle del Proyecto',
                                          copy=True)
    files = fields.One2many('budget.program_files', 'program_ids', string='Versiones de presupuesto', copy=True)
    documentos = fields.One2many('budget.program_documentos', 'program_ids', string='Documentos', copy=True)
    cuentasBanco = fields.One2many('budget.cuenta_banco', 'program_ids', string='Cuentas de banco', copy=True)
    activo = fields.Boolean(string='Activo', default=True)

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

    def reporte(self):
        url = "http://72.167.53.164:8080/birt/frameset?__report=presupuesto_proyectos.rptdesign&id_proyecto=%s" % str(
            self.id)
        return {'name': 'Reporte',
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'blank',
                'url': url
                }

    @api.model
    def create(self, vals):
        # vals['state'] = '2'
        vals['programId'] = self.env['ir.sequence'].next_by_code('budget.program')
        rec = super(Program, self).create(vals)
        # if 'programId' not in vals:
        #    strId = '000' + str(rec.id)
        #    rec['programId'] = strId[-3:]
        #    super(Program, self).write(rec)
        return rec

    def unlink(self):
        return super(Program, self).write({"activo": False})

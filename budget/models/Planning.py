from odoo import fields, models, api


class Planning(models.Model):
    _name = 'bg.planning'
    # _description = 'Description'
    # datos generales
    nombreInstitucion = fields.Char(string='Nombre de la institución', required=False)
    nombreProyecto = fields.Char(string='Nombre del proyecto', required=False)
    periodoSolicitado = fields.Char(string='Período solicitado', required=False)
    nombreCuenta = fields.Char(string='Nombre de la cuenta', required=False)
    numeroCuenta = fields.Char(string='Número de la cuenta', required=False)
    # planificacion
    logicaIntervencion = fields.Char(string='Lógica de intervención', required=False)
    indicadores = fields.Char(string='Indicadores', required=False)
    fuenteVerificacion = fields.Char(string='Fuente de verificación', required=False)
    hipotesis = fields.Char(string='Hipótesis', required=False)
    riesgos = fields.Char(string='Riesgos', required=False)
    # objetivos
    objetivos = fields.One2many(comodel_name='bg.target', inverse_name='target_ids', string='Objetivos')
    # resultados
    resultados = fields.One2many(comodel_name='bg.results', inverse_name='results_id', string='Resultados')
    # actividades
    actividades = fields.One2many(comodel_name='bg.activities', inverse_name='activity_ids', string='Actividades')
    # insumos
    insumos = fields.One2many(comodel_name='bg.supplies', inverse_name='supplies_ids', string='Insumos')
    # presupuesto
    presupuesto = fields.One2many(comodel_name='bg.budget', inverse_name='budget_ids', string='Insumos')


class Target(models.Model):
    _name = 'bg.target'
    correlativo = fields.Integer(string='Correlativo', required=False)
    objetivo = fields.Text(string="Objetivo",required=False)
    target_ids = fields.Many2one(comodel_name='bg.planning', string='Presupuesto')


class Results(models.Model):
    _name = 'bg.results'
    correlativo = fields.Integer(string='Correlativo', required=False)
    resultado = fields.Text(string="Resultado",required=False)
    results_id = fields.Many2one(comodel_name='bg.planning', string='Presupuesto')

class Activities(models.Model):
    _name = 'bg.activities'
    correlativo = fields.Integer(string='Correlativo', required=False)
    actividades = fields.Text(string="Actividades",required=False)
    activity_ids = fields.Many2one(comodel_name='bg.planning', string='Presupuesto')


class Supplies(models.Model):
    _name = 'bg.supplies'
    codigoInsumo = fields.Char(string='Código de insumo', required=False)
    descripcion = fields.Text(string="Descripción",required=False)
    presupuestoAsignado = fields.Float(string='Presupuesto asignado', required=False)
    montoAsignado = fields.Float(string='Presupuesto asignado', required=False)
    supplies_ids = fields.Many2one(comodel_name='bg.planning', string='Presupuesto')


class Budget(models.Model):
    _name = 'bg.budget'
    total = fields.Float(string='Total', required=False)
    presupuestoTransferido = fields.Float(string='Presupuesto transferido', required=False)
    actividad = fields.Text(string="Actividad", required=False)
    budget_ids = fields.Many2one(comodel_name='bg.planning', string='Presupuesto')
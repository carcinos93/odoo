from odoo import fields, models, api


class Cooperante(models.Model):
    _name = 'planificacion.cooperante'
    # _description = 'Description'

    nombre = fields.Char(string='Nombre del cooperante o Razón Social', required=True)
    numeroIdentificacion = fields.Char(string='Número de Identificación', required=True)
    direccion = fields.Text(string='Dirección', required=True)
    pais = fields.Char(string='País del cooperante', required=False)
    representanteLegal = fields.Char(string='Representante legal', required=False)
    valorProyecto = fields.Float(string='Valor de proyecto/programa', required=False)
    anioFiscal = fields.Char(string='Año fiscal', required=False)

    # todo lista de proyectos

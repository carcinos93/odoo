# -*- coding: utf-8 -*-
from odoo import fields, models , api


class Empleado(models.Model):
    _name = 'hr_recruitment_extender.empleado'
    _description = 'Descripción del empleado'
    #Cargo = fields.Char(string='Nombre de Cargo', required=False)
    gerencia = fields.Char(string='Gerencia', required=False)
    proyecto_a = fields.Char(string='Proyecto', required=False)
    lugartrabajo = fields.Char(string='lugartrabajo', required=False)
    #Cargo_1 = fields.Char(related='hr.job.name', string='Cargo'    , required=False)
    Cargo_1 = fields.Many2one('hr.job', string='Job Position' )

    #proyecto_a = fields.Many2one(comodel_name='budget.program', string='Proyecto', required=False)
    #Cargo = fields.Many2one('hr.job', 'Cargo')


    natura_vacante = fields.Selection(selection=[   ('Nuevo Cargo'           , 'Nuevo Cargo'),
                                                    ('Reemplazo'             , 'Reemplazo'),
                                                    ('Renuncia'              , 'Renuncia'),
                                                    ('Despido'               , 'Despido'),
                                                    ('Fin Contrato'          , 'Fin Contrato'),
                                                    ('Reestructuracion'      , 'Reestructuracion'),
                                                    ('Contrato Temporal'     , 'Contrato Temporal'),
                                                    ('Incapacidad'           , 'Incapacidad'),
                                                    ('Incapacidad Maternidad', 'Incapacidad Maternidad'),
                                                    ('Licencia'              , 'Licencia'),
                                                    ('Incremento Laboral'    , 'Incremento Laboral')
                                                  ],  string='Naturaleza Vacante')

    mod_contra     = fields.Selection(selection=[('Servicios Profesionales'      , 'Servicios Profesionales'),
                                                 ('Planilla Contrato Individual' , 'Planilla Contrato Individual')
                                                ], string='Modalidad Contratacion')
    fec_contra_desde = fields.Date(String='Desde', required=False)
    fec_contra_hasta = fields.Date(String='Hasta', required=False)
    total_meses      = fields.Char(String='Meses', required=False)

    monto_presu_total = fields.Char(String='Monto Total', required = False)
    monto_presu_mes   = fields.Char(String='Monto Mensual', required = False)
    fecha_req_ingreso = fields.Date(String='Fecha Contratacion', required=False)

    lin_presu_pro     = fields.Char(String='Linea Presupuestaria Proyecto', required=False)
    categoria_gasto   = fields.Char(String='Categoría del Gasto'          , required=False)
    lin_presu_pob     = fields.Char(String='Linea Presupuestaria POB/POA' , required=False)

    justificacion     = fields.Char(String='Justificación Contratación'   , required=False)
    beneficios        = fields.Char(String='Beneficios Adicionales'       , required=False)
    observaciones     = fields.Char(String='Observaciones'                , required=False)

    jefe_solicitante = fields.Char(String='Jefe Solicitante' , required=False)
    jefe_inmediato   = fields.Char(String='Jefe Inmediato'   , required=False)

    req_estado = fields.Selection( 
         [  ('1','Autorización 1' )  ,
            ('2','Autorización 2' )  ,
            ('3','Aut Director  ' )
         ] , string='Nivel_Autorizado')
    req_estado1 = fields.Selection( 
         [  ('1','Autorización 1' )  ,
            ('2','Autorización 2' )  ,
            ('3','Aut Director  ' )
         ] , string='Nivel_Autorizado')
    req_estado2 = fields.Selection( 
         [  ('1','1' )  ,
            ('2','2' )  ,
            ('3','3' )
         ] , string='Nivel_Autorizado')
   
    state = fields.Selection( [ 
         ('1','Ingresado'),
         ('2','Autorización Jefe') ,
         ('3','Autorización Jefe Inmediato'),
         ('4','Autorización Director')     ] , default='1', string="Estado")

    def enviado(self):
         for env in self:
          env.write({'state':'1'})
          return True

    def enviado2(self):
         for env in self:
          env.write({'state':'2'})
          return True

    def enviado3(self):
         for env in self:
          env.write({'state':'3'})
          return True

    def enviado4(self):
         for env in self:
          env.write({'state':'4'})
          return True

   
#def escalar(self):
#     for env in self:
#      env.write({'state':2})
#      return True
#def escalar(self):
#   return True
    


    
    



  

    


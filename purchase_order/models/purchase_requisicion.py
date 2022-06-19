 # -*- coding: utf-8 -*-
from odoo import models, fields, api , _, tools, exceptions
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    requisicion_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseSequences(models.Model):
    _name = 'purchase.sequences'

    program_id = fields.Many2one('budget.program', 'Proyecto')
    correlative_id = fields.Char('Correlativo')

    def next_correlativo(self):
        self.correlative_id = str(int(self.correlative_id) + 1)

purchaseSequences()

class purchaseRequisicion(models.Model):
    _name = 'purchase.order.requisitions'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    @api.depends('program_id', 'state')
    def _compute_name(self):
        if self.program_id:
            if self.state == '0':
                self.name = 'Requisición borrador'
                self.name_corto_program = self.program_id.shortName
            else:
                corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
                correlativo = 'NE'
                if corre_this:
                    correlativo = corre_this.correlative_id
                axo = date.today().year
                self.name = self.program_id.shortName + '/' + correlativo + '/' + str(axo)
                self.name_corto_program = self.program_id.shortName

    name = fields.Char('Correlativo', compute='_compute_name', store=True, readonly=True)
    program_id = fields.Many2one('budget.program', 'Proyecto')
    name_corto_program = fields.Char('Proyecto')
    solicitante = fields.Many2one('hr.employee', 'Autorizador')
    type = fields.Many2one('purchase.type', 'Tipo de Compra')
    activity_id = fields.Many2one('planificacion.actividad_producto_resultado', 'Actividad')
    date_order = fields.Date('Fecha de Entrega', help='Fecha Maxima de Entrega')
    place_delivery = fields.Text('Lugar de Entrega')
    activity = fields.Char('Actividad Nombre')
    country_id = fields.Many2one('res.country', 'Pais Beneficiario')
    state = fields.Selection([('1', 'Requisicion'),
                              ('2', 'Selección'),
                              ('3', 'Formalización'),
                              ('4', 'Recepcion'),
                              ('5', 'Pago')], default='1', string='Estado',  tracking=True)
    doc_formalizar = fields.Selection([('1', 'Orden de Compra'),
                              ('2', 'Orden de Servicio'),
                              ('3', 'Contrato')], 'Documento para Formalizar', tracking=True)
    applicant = fields.Char('Autorizador')
    evento = fields.Char(string='Actividad / Evento')
    comment = fields.Text(string='Comentarios')
    date_applicant = fields.Datetime('Fecha Solicitante')
    authorizer = fields.Char('Autorizador')
    nombre_solicitante = fields.Char('Autorizador')
    date_authorizer = fields.Datetime('Fecha de Autorizacion')
    purchase_author = fields.Char('Autoriza Compras')
    date_purchase_author = fields.Datetime('Fecha Compras Autoriza')
    purchase_docs_ids = fields.One2many('purchase.order.docs', 'requisition_id', 'doc')
    purchase_requi_line_ids = fields.One2many('purchase.order.requisition.line', 'requisition_id', 'Lineas')
    authorizer_ids = fields.One2many('purchase.order.autorizacion', 'requisition_id', 'Autorizacion')
    lineas_order_ids = fields.One2many('purchase.line.requisicion', 'requisition_id', 'Lineas de Orden de Compra')
    lineas_oferta_ids = fields.One2many('purchase.order.ofertas', 'requisition_id', 'Lineas de Ofertas')
    lineas_adjudicacion = fields.One2many('purchase.order.adjudicacion', 'requisition_id', 'Lineas Adjudicacion')
    lineas_proveedores = fields.Many2many('res.partner', 'reequisicion_partner_rel', 'rquisicion_id', 'partner_ids', 'Proveedores')
    orden_compra_ids = fields.One2many('purchase.order', 'requisicion_id', 'Ordenes de Compra')
    orden_servicio_ids = fields.One2many('purchase.order.service', 'requisicion_id', 'Ordenes de Servicio')
    used_comite = fields.Boolean(string='Utiliza Cómite Evaluador')
    date_requisicion = fields.Date(string='Fecha Requisición')
    evaluacion_ids = fields.One2many('purchase.order.evaluacion', 'order_id', string='Evalaución')

    comite_ids = fields.Many2many('hr.employee', 'comite_requision_employee_rel', 'order_id', 'employee_id', string='Comité')
    filename_comite = fields.Char(string='Nombre Archivo')
    file_comite = fields.Binary('Nombramiento Comité')
    filename_comite_form = fields.Char(string='Nombre Archivo')
    file_comite_form = fields.Binary('Formulario de Comité')
    proceso_iniciado = fields.Boolean(string='Proceso Iniciado', tracking=True)
    proceso_autorizado = fields.Boolean(string='Proceso Autorizado', tracking=True)

    @api.onchange('program_id')
    def onchange_program(self):
        #corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        if self.program_id:
            self.name = self.program_id.shortName

    @api.onchange('type')
    def onchange_type(self):
        self.used_comite = self.type.used_comite

    @api.onchange('activity_id')
    def onchange_activity(self):
        self.activity = self.activity_id.nombreActividad

    def RetornarEtapa(self):
        estado = '1'
        obj_val = self.env['purchase.order.autorizacion']
        if self.state == '2':
            estado = '1'
            vals = {'name': 'Regresa a etapa de Requisición',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '3':
            estado = '2'
            vals = {'name': 'Regresa a etapa de Selección',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '4':
            estado = '3'
            vals = {'name': 'Regresa a etapa de Formalización',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        if self.state == '5':
            estado = '4'
            vals = {'name': 'Regresa a etapa de Recepción',
                    'type': 'auto',
                    'user_id': self.env.uid,
                    'date_acc': datetime.today(),
                    'requisition_id': self.id}
            obj_val.create(vals)
        self.write({'state': estado})

    def IniciarProceso(self):
        corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        corre_this.next_correlativo()
        self.write({'proceso_iniciado': True})
        vals = {'name': 'Inicio del Proceso',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        return True

    def AutorizarRequisicion(self):
        if not self.proceso_iniciado:
            raise ValidationError(
                _('El proceso no se puede autorizar, sino se ha iniciado. Comuniquese con el Solicitante'))

        self.write({'proceso_autorizado': True})
        vals = {'name': 'Autoriza Requisición',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        return True

    def autorizacion_partner(self):
        if not self.proceso_autorizado:
            raise ValidationError(
                _('No se puede aceptar la compra, si su debida autorización. Comuniquese con el encargado de autorizar.'))

        today = date.today()
        if self.date_order < today:
            raise ValidationError(
                _('La fecha de entrega, no puede ser menor a la fecha actual.'))

        documentos1 =''
        for documentos in self.purchase_docs_ids:
            if documentos.name.mandatory is True:
                documentos1 += ' ' + documentos.name.name
        ducumentos2 = ''

        libres = self.env['purchase.type.doc'].search([('type_id', '=', self.type.id), ('state_author', '=', self.state)])
        for documentos in libres:
            if documentos.mandatory is True:
                ducumentos2 += ' ' + documentos.name
        if documentos1 == ducumentos2:
            raise exceptions.ValidationError('Debe seleccionar los documentos del proyecto')


        vals2 = {'name': 'Aceptación de Compra',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}
        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals2)
        self.write({
                    'state': '2',
                    'date_requisicion': date.today()
                    })
        #### Actualizando los valores de la actividad
        for item in self.purchase_requi_line_ids:
            if item.insumo_id:
                reservado = item.insumo_id.reservado + item.monto
                item.insumo_id.write({'reservado': reservado})

        return True

    def pasoFormalizacion(self):
        today = date.today()
        if self.date_requisicion < today:
            raise ValidationError(
                _('La fecha de requisición, no puede ser menor a la fecha actual.'))

        user_browse = self.env['res.users'].browse(self.env.uid)
        vals = {'name': 'Paso a Formalización',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        self.write({'state': '3'})

    def ordenes_compras(self):
        orden_compra = self.env['purchase.order']
        orden_compra_lineas = self.env['purchase.order.line']
        if self.lineas_adjudicacion:
            for adj in self.lineas_adjudicacion:
                if adj.adjudication == True:
                    crea_order = {
                        'requisicion_id': self.id,
                        'partner_id': adj.name.id,
                        'date_order': datetime.today(),
                        'currency_id': adj.name.property_purchase_currency_id.id or 2,
                        'state': 'purchase',
                        'user_id': self.env.uid
                    }
                    order = orden_compra.create(crea_order)
                    for items in adj.lineas_adjudicacion:
                        crea_lineas = {
                            'order_id': order.id,
                            'name': items.name,
                            'product_id': items.product_id.id,
                            'product_qty': items.cantidad,
                            'product_uom_qty': items.cantidad,
                            'price_unit': items.price_unitary,
                            'price_subtotal': items.monto,
                            'price_total': items.monto,
                            'company_id': 1,
                            'state': 'purchase'
                        }
                        orden_compra_lineas.create(crea_lineas)

        vals = {'name': 'Cierre del Proceso',
                'type': 'auto',
                'user_id': self.env.uid,
                'date_acc': datetime.today(),
                'requisition_id': self.id}

        obj_val = self.env['purchase.order.autorizacion']
        obj_val.create(vals)
        self.write({'state': '4'})

        #### Actualizando los valores de la actividad
        for item in self.purchase_requi_line_ids:
            if item.insumo_id:
                reservado = item.insumo_id.reservado - item.monto
                comprometido = item.insumo_id.comprometido + item.monto
                item.insumo_id.write({'reservado': reservado, 'comprometido': comprometido})

class purchaseRequisicionLine(models.Model):
    _name = 'purchase.order.requisition.line'

    actividad_id = fields.Many2one('planificacion.actividad_producto_resultado', string='Actividad')
    employee_id = fields.Many2one('hr.employee', string='Responsable Actividad')
    insumo_id = fields.Many2one('planificacion.actividad_producto_resultado_detalle', string='Insumo')

    @api.depends('requisition_id.program_id')
    def _default_program(self):
        if self.requisition_id.program_id:
           self.program_id = self.requisition_id.program_id.id

    program_id = fields.Many2one(comodel_name='budget.program', string='Fuente de financiamiento', compute='_default_program', store=True, readonly=True)
    presupuesto_id = fields.Many2one(comodel_name='budget.program_detail', string='Presupuesto de proyecto')

    # ('program_id', 'in', [g.fuenteFinanciamiento for g in planificacion.actividad_producto_resultado_detalle])]

    @api.depends('insumo_id')
    def _compute_name(self):
        if self.insumo_id:
            self.monto_asignado = self.insumo_id.montoAsignado
            self.disponible = self.insumo_id.disponible


    monto = fields.Float(string='Monto Utilizar')
    disponible = fields.Float(string='Monto Disponible', compute='_compute_name', store=True, readonly=True)
    monto_asignado = fields.Float(string='Monto Asignado', compute='_compute_name', store=True, readonly=True)

    @api.onchange('insumo_id')
    def onchange_program(self):
        # corre_this = self.env['purchase.sequences'].search([('program_id', '=', self.program_id.id)])
        if self.insumo_id:
            self.program_id = self.insumo_id.fuenteFinanciamiento.id
            self.presupuesto_id = self.insumo_id.detalleFuenteFinanciamiento.id

    # codigo_actividad = fields.Char(string='Código actividad')
    # name = fields.Text(string='Nombre de actividad')
    # insumo = fields.Many2one(comodel_name='budget.line', string='Insumo')
    # fuente_financiamiento = fields.Many2one(comodel_name='budget.program', string='Fuente de financiamiento')
    # detalle_fuente_financiamiento = fields.Many2one(comodel_name='budget.program_detail',
    #                                               string='Presupuesto de proyecto')
    # monto_fuente_financiamiento = fields.Float(string='Monto disponible')
    # monto_asignado = fields.Float(string='Monto asignado')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'id Linea')

class purchaseOrderDocs(models.Model):
    _name = 'purchase.order.docs'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Many2one('purchase.type.doc', 'Tipo de Documento')
    namefile = fields.Binary('Nombre Archivo')
    files = fields.Binary('Archivos')
    description = fields.Text('Comentario')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

    filename_adjunto = fields.Char(string='Nombre Archivo')
    file_adjunto = fields.Binary('Archivo')

class purchaseOrderAutorizaciones(models.Model):
    _name = 'purchase.order.autorizacion'

    name = fields.Char('Accion')
    type = fields.Selection([('creacion', 'Creacion'),
                             ('auto', 'Autorizacion'),
                             ('auto_com', 'Autorizacion Compras')], 'Tipo')
    user_id = fields.Many2one('res.users', 'Usuario')
    date_acc = fields.Datetime('Fecha')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseLineRequisicion(models.Model):
    _name = 'purchase.line.requisicion'

    name = fields.Text('Descripcion')
    cantidad = fields.Float('cantidad', default=1.00)
    price_unitary = fields.Float('Precio Unitario', default=0)
    monto = fields.Float('Monto')
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True)
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

    @api.onchange('cantidad', 'price_unitary')
    def onchage_calculos(self):
        if self.cantidad and self.price_unitary:
            self.monto = self.cantidad * self.price_unitary

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            self.name = self.product_id.name

class purchaseorderOfertas(models.Model):
    _name = 'purchase.order.ofertas'

    name = fields.Char('Documento')
    archivo = fields.Binary('Archivo')
    description = fields.Text('Descripcion')
    date_reception = fields.Date('Fecha de Recepcion')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class pucharseOrderAdjudicacion(models.Model):
    _name = 'purchase.order.adjudicacion'

    name = fields.Many2one('res.partner')
    date_envio = fields.Date('Fecha de Envio')
    observation = fields.Text('Observaciones')
    adjudication = fields.Boolean('Adjudicacion')
    date_adjudication = fields.Date('Fecha de Adjudicacion')
    requisition_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')
    lineas_adjudicacion = fields.Many2many('purchase.line.requisicion', 'rel_lineas_requisiciones', 'adjudicacion_id',
                                           'detalle_id', 'Productos Adjudicados')

class purchaseOrderService(models.Model):
    _name = 'purchase.order.service'

    clase = fields.Many2one('order.service.clase', 'Clase')
    name = fields.Char('Nombre')
    proveedor = fields.Many2one('res.partner', 'Proveedor')
    objetivo_general = fields.Text('Objetivo General')
    desde = fields.Date('Desde')
    hasta = fields.Date('Hasta')
    cordinacion = fields.Text('COORDINACIÓN')
    terminacion = fields.Text('TERMINACIÓN')
    product_id = fields.Many2one('product.product', 'Actividad')
    lineas_ids = fields.One2many('purchase.order.service.line', 'order_id', 'Lineas de Actividad')
    precios_formas_ids = fields.One2many('purchase.order.forma.pago', 'orden_id', 'Formas de Pago')
    requisicion_id = fields.Many2one('purchase.order.requisitions', 'Requisicion')

class purchaseorderServiceLine(models.Model):
    _name = 'purchase.order.service.line'

    name = fields.Many2one('product.service', 'Producto')
    order_id = fields.Many2one('purchase.order.service', 'Orden de Servicio')

class purchaseFormaPago(models.Model):
    _name = 'purchase.order.forma.pago'

    name = fields.Text('Descripción')
    precio = fields.Float('Precio')
    numero = fields.Integer('Numero de Pago')
    orden_id = fields.Many2one('purchase.order.service', 'Orden de Servicio')

class orderServiceClase(models.Model):
    _name = 'order.service.clase'
    
    name = fields.Char('Nombre Clase')

class serviceproduct(models.Model):
    _name = 'product.service'

    name = fields.Char('Nombre')
    codigo = fields.Char('Codigo')

class Evaluaciones(models.Model):
    _name = 'purchase.order.evaluacion'

    name = fields.Integer('Correlativo')
    criterio_id = fields.Many2one('purchase.order.evaluacion.criterio', string='Criterio')
    indicador = fields.Text('Detalle de Indicador')
    valor1 = fields.Float(string='Valor 1')
    valor2 = fields.Float(string='Valor 2')
    order_id = fields.Many2one('purchase.order.requisitions', string='Requisicion')

class EvaluacionesTipo(models.Model):
    _name = 'purchase.order.evaluacion.criterio'

    name = fields.Char('Nombre')








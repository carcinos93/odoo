# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions




class Car(models.Model):
    _name = 'odoo_model_advanced.car'
    _description = 'Coche'
    #_inherit = 'base.active' # No funciona?

    name = fields.Char(string='Modelo')
    number_plate = fields.Char(string='Matrícula')
    cv = fields.Float(string='CV')
    colour = fields.Char(string='Color')
    fuel_litres = fields.Float(string='Litros')  #fuel_litres = fields.Float(string='Litros', compute='_check_under_fuel')
    under_fuel = fields.Boolean(string='Necesita repostar', compute='_compute_under_fuel') # paara guardar se store=True
    customer = fields.Many2one(comodel_name='res.users', string='Cliente')
    group_id = fields.Integer(string='Group_id', required=False)

    customer_phone = fields.Char(string='Teléfono',related='customer.phone', readonly=True)
    #_sql_constraints = [
    #    ('number_plate_unique', 'UNIQUE(number_plate)', 'El número de matrícula deberá ser único'),
    #]

    def map(self):
        cars = self.env['odoo_model_advanced.car'].search([])
        cars_mapped = cars.mapped(lambda c: 'mt³ ' + str(c.fuel_litres / 1000.0) )
        print(cars_mapped)

    def sort(self):
        cars = self.env['odoo_model_advanced.car'].search([])
        cars_sorted = cars.sorted(key=lambda c: c.cv, reverse=False)
        for car in cars_sorted:
            print(car.name, car.cv)

    def filter(self):
        cars = self.env['odoo_model_advanced.car'].search([])
        cards_filtered = cars.filtered( lambda c:  c.cv >= 90)
        self.print_cars(cards_filtered)


    def print_cars(self, cars):
        for car in cars:
            print(car.name, car.cv, car.fuel_litres)


    def get_average_cv(self):
        grouped = self.read_group(
            [ ('cv', '>', '85') ],
            [ 'cv:avg' ],
            [ 'group_id' ]
        )
        print(grouped)
        return grouped

    def recorset_operations(self):
        r1 = self.env['odoo_model_advanced.car'].search([ ('group_id', '=', '1') ])
        r2 = self.env['odoo_model_advanced.car'].search([ ('group_id', '=', '2') ])
        r3 = r1 - r2
        self.print_recorset( r3 )
        print('-----------')
        print(r1 == r2)


    def print_recorset(self, recordset):
        for record in recordset:
            print(record.name, record.cv, record.fuel_litres)

    def get_average_cv_sql(self):
        sql = 'SELECT AVG(car.cv) FROM odoo_model_advanced_car AS car WHERE name = %s'
        auto =  'Audi A4'
        self.env.cr.execute(sql, ( auto, ) )
        result = self.env.cr.fetchall()
        print(result)



    @api.constrains('cv')
    def _validate_cv(self):
        if self.cv <= 0:
            raise exceptions.ValidationError('El valor de CV no puede ser menor o igual a 0') # Se aplica cuando las condiciones que afectan a un determinado registro fallan.
            # raise exceptions.UseError('El valor de CV no puede ser menor o igual a 0') # Se emplea cuando un usuario trata de agregar un valor a un registro y el estado del registro no es el correcto porque no se cumplen ciertas condiciones.

    @api.model
    def create(self, vals):
        vals['colour'] = 'rojo'
        rec = super(Car, self).create(vals)
        return rec

    def _compute_under_fuel(self):
        self.under_fuel = self.fuel_litres < 50


    def create_cars(self):
        car1 = {
            'name': 'Audo A4',
            'number_plate': '4458-HJG',
            'cv': 130,
            'colour': 'rojo',
            'fuel_litres': 75
        }
        car2 = {
            'name': 'Audo A4',
            'number_plate': '4459-HJG',
            'cv': 95,
            'colour': 'azul',
            'fuel_litres': 13
        }
        # self.env['odoo_model_advanced.car'].create(car1)
        # self.env['odoo_model_advanced.car'].create(car2)


    # @api.depends('fuel_litres', 'customer.phone')    #@api.onchange('fuel_litres') #atributo1, atributo2
    # def _check_under_fuel(self):
    #    print('Se ejecuta depends...')
    #    self.under_fuel = self.fuel_litres < 50

    #@api.model_create_multi
    #def create(self, vals_list):
    #    records = super(Car, self).create(vals_list)
    #    return records


class UserExtended(models.Model):
    _inherit = 'res.users'

    def name_get(self):
        result = []
        for user in self:
            name = '%s (%s)' % ( user.name, user.phone, )
            result.append((user.id, name,))
        return result


class BaseActive(models.AbstractModel):
    _name = 'base.active'
    _abstract = True
    # _auto = False
    active = fields.Boolean(default=True)
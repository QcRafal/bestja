# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Organization(models.Model):
    _name = 'organization'
    _parent = 'parent'

    STATES_FOR_AUTHORIZATION = [
        ('waiting', 'Czeka na zatwierdzenie'),
        ('authorized', 'Potwierdzona')
    ]
    state = fields.Selection(STATES_FOR_AUTHORIZATION, default='waiting', string="Stan")
    name = fields.Char(string="Nazwa", required=True)
    krs = fields.Char(string="KRS")
    regon = fields.Char(string="REGON")
    nip = fields.Char(string="NIP")
    street_address = fields.Char(string="Ulica", required=True)
    city_address = fields.Char(string="Miejscowość", required=True)
    street_number = fields.Char(string="Numer", required=True)
    postal_code = fields.Char(size=6,string="Kod pocztowy")
    email = fields.Char(string="E-mail", required=True) 
    phone = fields.Char(size=10, string="Numer Telefonu")
    www = fields.Char(string="WWW")
    fbfanpage = fields.Char(string="Fanpage na FB") 
    parent = fields.Many2one('organization')
    
    coordinator = fields.Many2one('res.users', ondelete='restrict', 
       string="Koordynator", default=lambda self: self.env.user, readonly=True) 

    active = fields.Boolean(default=True)
   
    storage_street = fields.Char(string="Ulica")
    storage_street_number = fields.Char(string="Numer")
    storage_city_address = fields.Char(string="Miejscowość")
    storage_postal_code = fields.Integer(size=6,string="Kod pocztowy")

    organization_description = fields.Text(string="Opis Organizacji")

    image = fields.Binary("Photo")
    
    @api.constrains('coordinator')
    def _check_organizations(self):
        if (self.coordinator.id != self.env.user.id): 
            raise ValueError("Możesz zmieniać tylko swoje organizacje!") 

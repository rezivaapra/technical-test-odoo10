# -*- coding: utf-8 -*-

from odoo import models, fields

class ServiceTeam(models.Model):
    _name = 'booking_order_reziva_05042001.service_team'
    _description = 'booking_order_reziva_05042001.service_team'

    name = fields.Char('Team Name', required=True)
    team_leader_id = fields.Many2one('res.users', 'Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')
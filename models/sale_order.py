# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean('Is Booking Order', default=True)
    service_team_id = fields.Many2one('booking_order_reziva_05042001.service_team', 'Team', required=True)
    team_leader_id = fields.Many2one('res.users', 'Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members', required=True)
    booking_start = fields.Datetime('Booking Start', required=True)
    booking_end = fields.Datetime('Booking End', required=True)

    @api.onchange('service_team_id')
    def _onchange_team_id(self):
        if self.service_team_id:
            self.team_leader_id = self.service_team_id.team_leader_id
            self.team_member_ids = [(6, 0, self.service_team_id.team_member_ids.ids)]
    
    def check_team_availability(self):
        overlapping_wo = self.env['booking_order_reziva_05042001.work_order'].search([
            ('team_id', '=', self.service_team_id.id),
            ('state', '!=', 'cancelled'),
            ('planned_start', '<=', self.booking_end),
            ('planned_end', '>=', self.booking_start)
        ])

        if overlapping_wo:
            so_ref = overlapping_wo.mapped('sale_order_id.name')
            raise UserError(_('Team already has work order during that period on %s') % ', '.join(so_ref))
        else:
            raise UserError(_('Team is available for booking'))
    
    def action_confirm_sale_order(self):
        overlapping_wo = self.env['booking_order_reziva_05042001.work_order'].search([
            ('team_id', '=', self.service_team_id.id),
            ('state', '!=', 'cancelled'),
            ('planned_start', '<=', self.booking_end),
            ('planned_end', '>=', self.booking_start)
        ])

        if overlapping_wo:
            so_ref = overlapping_wo.mapped('sale_order_id.name')
            raise UserError(_('Team is not available during this period, already booked on %s. Please book on another date.') % ', '.join(so_ref))
        else:
            super(SaleOrder, self).action_confirm()
            self.create_work_order()

    def create_work_order(self):
        self.env['booking_order_reziva_05042001.work_order'].create({
            'sale_order_id': self.id,
            'team_id': self.service_team_id.id,
            'team_leader_id': self.team_leader_id.id,
            'team_member_ids': [(6, 0, self.team_member_ids.ids)],
            'planned_start': self.booking_start,
            'planned_end': self.booking_end,
            'state': 'pending'
        })


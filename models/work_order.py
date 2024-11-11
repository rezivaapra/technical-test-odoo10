# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class WorkOrder(models.Model):
    _name = 'booking_order_reziva_05042001.work_order'
    _description = 'booking_order_reziva_05042001.work_order'

    name = fields.Char('WO Number', required=True, copy=False, readonly=True, index=True, default=lambda self: self.env['ir.sequence'].next_by_code('booking_order_reziva_05042001.work_order'))
    sale_order_id = fields.Many2one('sale.order', 'Booking Order Reference', readonly=True)
    team_id = fields.Many2one('booking_order_reziva_05042001.service_team', 'Team', required=True)
    team_leader_id = fields.Many2one('res.users', 'Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime('Planned Start', required=True)
    planned_end = fields.Datetime('Planned End', required=True)
    date_start = fields.Datetime('Date Start', readonly=True)
    date_end = fields.Datetime('Date End', readonly=True)
    state = fields.Selection([('pending', 'Pending'),
                              ('in_progress', 'In Progress'),
                              ('done', 'Done'),
                              ('cancelled', 'Cancelled')], default='pending', string='State', required=True)
    notes = fields.Text('Notes')
    cancel_reason = fields.Text(string="Cancel Reason")

    def action_start_work(self):
        for record in self:
            record.state = 'in_progress'
            record.date_start = datetime.now()

    def action_end_work(self):
        for record in self:
            if record.state == 'in_progress':
                record.state = 'done'
                record.date_end = datetime.now()

    def action_reset(self):
        for record in self:
            if record.state == 'in_progress':
                record.state = 'pending'
                record.date_start = False

    @api.multi
    def action_cancel(self):
        """Open a wizard to input the cancel reason"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Work Order',
            'res_model': 'work.order.cancel.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_work_order_id': self.id}
        }

    def confirm_cancel(self, cancel_reason):
        """Append the cancellation reason and set the state to cancelled"""
        if not cancel_reason:
            raise UserError('You must provide a reason for cancellation.')

        self.write({
            'state': 'cancelled',
            'notes': self.notes + "\n" + "Cancellation Reason: " + cancel_reason if self.notes else "Cancellation Reason: " + cancel_reason
        })

from odoo import models, fields

class WorkOrderCancelWizard(models.TransientModel):
    _name = 'work.order.cancel.wizard'
    _description = 'Cancel Work Order Wizard'

    work_order_id = fields.Many2one('booking_order_reziva_05042001.work_order', string="Work Order", required=True)
    cancel_reason = fields.Text(string="Reason for Cancellation", required=True)

    def action_confirm(self):
        """Confirm the cancellation and pass the reason to the work order"""
        self.work_order_id.confirm_cancel(self.cancel_reason)
        return {'type': 'ir.actions.act_window_close'}

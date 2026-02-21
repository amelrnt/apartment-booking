from odoo import api, fields, models


class BookingCancelWizard(models.TransientModel):
    _name = 'booking.cancel.wizard'
    _description = 'Cancel Booking Wizard'

    booking_id = fields.Many2one('travelio.apartment.booking', string='Booking')
    reason = fields.Text(string='Reason', required=True)

    def action_confirm_cancel(self):
        self.booking_id.write({
            'state': 'cancelled',
            'cancel_reason': self.reason
        })
        self.booking_id.unit_id._promote_waitlist(self.booking_id.checkin_date, self.booking_id.checkout_date)
from datetime import timedelta

from odoo import _, api, fields, models


class BookingRequestWizard(models.TransientModel):
    _name = 'booking.request.wizard'
    _description = 'Request Booking Wizard'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    unit_id = fields.Many2one('travelio.apartment.unit', string='Unit', required=True)
    checkin_date = fields.Date(string='Check-in Date', required=True)
    checkout_date = fields.Date(string='Check-out Date', required=True)

    def action_process(self):
        self.ensure_one()
        # Check for overlaps 
        overlap = self.env['travelio.apartment.booking'].search_count([
            ('unit_id', '=', self.unit_id.id),
            ('state', 'in', ['hold', 'confirmed']),
            ('checkin_date', '<', self.checkout_date),
            ('checkout_date', '>', self.checkin_date),
        ])

        if not overlap:
            return self.env['travelio.apartment.booking'].create({
                'customer_id': self.customer_id.id,
                'unit_id': self.unit_id.id,
                'checkin_date': self.checkin_date,
                'checkout_date': self.checkout_date,
                'state': 'hold',
                'hold_expired_at': fields.Datetime.now() + timedelta(minutes=30)
            })
        else:
            return self.env['travelio.apartment.waitlist'].create({
                'customer_id': self.customer_id.id,
                'unit_id': self.unit_id.id,
                'checkin_date': self.checkin_date,
                'checkout_date': self.checkout_date,
                'state': 'waiting'
            })
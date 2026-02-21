from datetime import datetime, timedelta

from odoo import fields, models


class ApartmentUnit(models.Model):
    _name = 'travelio.apartment.unit'
    _description = 'Apartment Unit'

    name = fields.Char(string='Unit Code', required=True, copy=False)
    building_name = fields.Char(string='Building Name')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Unit code must be unique!')
    ]

    def _promote_waitlist(self, checkin, checkout):
        """Logic to promote FIFO waitlist when a slot opens """
        waitlists = self.env['travelio.apartment.waitlist'].search([
            ('unit_id', '=', self.id),
            ('state', '=', 'waiting'),
            ('checkin_date', '<', checkout),
            ('checkout_date', '>', checkin)
        ], order='requested_at asc')

        for wl in waitlists:
            overlap = self.env['travelio.apartment.booking'].search_count([
                ('unit_id', '=', self.id),
                ('state', 'in', ['hold', 'confirmed']),
                ('checkin_date', '<', wl.checkout_date),
                ('checkout_date', '>', wl.checkin_date),
            ])
            
            if not overlap:
                new_booking = self.env['travelio.apartment.booking'].create({
                    'customer_id': wl.customer_id.id,
                    'unit_id': wl.unit_id.id,
                    'checkin_date': wl.checkin_date,
                    'checkout_date': wl.checkout_date,
                    'state': 'hold',
                    'hold_expired_at': fields.Datetime.now() + timedelta(minutes=30)
                })
                wl.write({
                    'state': 'promoted',
                    'promoted_booking_id': new_booking.id
                })
                break

    def action_open_booking_wizard(self):
        """Opens the Request Booking wizard for this specific unit."""
        self.ensure_one()
        return {
            'name': 'Request Booking',
            'type': 'ir.actions.act_window',
            'res_model': 'booking.request.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_unit_id': self.id,
            }
        }
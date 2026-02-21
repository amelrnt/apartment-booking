from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ApartmentBooking(models.Model):
    _name = 'travelio.apartment.booking'
    _description = 'Apartment Booking'
    _order = 'id desc'

    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    unit_id = fields.Many2one('travelio.apartment.unit', string='Unit', required=True)
    checkin_date = fields.Date(string='Check-in Date', required=True)
    checkout_date = fields.Date(string='Check-out Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('hold', 'Hold'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')
    ], string='Status', default='draft')
    cancel_reason = fields.Text(string='Cancel Reason')
    hold_expired_at = fields.Datetime(
        string='Deadline Hold', 
        index=True  # Optimization
    )

    @api.model
    def create(self, vals):
        for val in vals:
            if val.get('name', _('New')) == _('New'):
                val['name'] = self.env['ir.sequence'].next_by_code('travelio.apartment.booking') or _('New')
        return super(ApartmentBooking, self).create(vals)

    @api.constrains('checkin_date', 'checkout_date', 'unit_id', 'state')
    def _check_booking_constraints(self):
        for rec in self:
            if rec.checkout_date <= rec.checkin_date:
                raise ValidationError(_("Checkout date must be after check-in date."))
            
            if rec.state in ['hold', 'confirmed']:
                domain = [
                    ('id', '!=', rec.id),
                    ('unit_id', '=', rec.unit_id.id),
                    ('state', 'in', ['hold', 'confirmed']),
                    ('checkin_date', '<', rec.checkout_date),
                    ('checkout_date', '>', rec.checkin_date),
                ]
                if self.search_count(domain):
                    raise ValidationError(_("Safety Check: Unit is already locked for these dates by another active booking."))

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'
            rec.unit_id._promote_waitlist(rec.checkin_date, rec.checkout_date)

    def action_open_cancel_wizard(self):
        """Opens the Cancel Booking wizard for this specific booking."""
        self.ensure_one()
        return {
            'name': 'Cancel Booking',
            'type': 'ir.actions.act_window',
            'res_model': 'booking.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_booking_id': self.id,
            }
        }

    @api.model
    def _cron_expire_hold(self):
        expired_bookings = self.search([
            ('state', '=', 'hold'),
            ('hold_expired_at', '<', fields.Datetime.now())
        ])
        for booking in expired_bookings:
            booking.state = 'expired'
            booking.unit_id._promote_waitlist(booking.checkin_date, booking.checkout_date)


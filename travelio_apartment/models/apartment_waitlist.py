from odoo import _, api, fields, models


class ApartmentWaitlist(models.Model):
    _name = 'travelio.apartment.waitlist'
    _description = 'Booking Waitlist'

    name = fields.Char(string='Waitlist Ref', readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    unit_id = fields.Many2one('travelio.apartment.unit', string='Unit', required=True)
    checkin_date = fields.Date(string='Check-in Date', required=True)
    checkout_date = fields.Date(string='Check-out Date', required=True)
    requested_at = fields.Datetime(string='Requested At', default=fields.Datetime.now)
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('promoted', 'Promoted'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='waiting')
    promoted_booking_id = fields.Many2one('travelio.apartment.booking', string='Promoted Booking')

    @api.model
    def create(self, vals):
        for val in vals:
            if val.get('name', _('New')) == _('New'):
                val['name'] = self.env['ir.sequence'].next_by_code('travelio.apartment.waitlist') or _('New')
        return super(ApartmentWaitlist, self).create(vals)

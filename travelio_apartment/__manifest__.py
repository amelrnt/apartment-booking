{
    'name': "Travelio Apartment",
    'description': "Custumize module built for travellio Technical Interview",
    'summary': """
            Travelio Apartment Unit Booking Module
    """,
    'author': "Amelia Rosanti",
    'license': 'LGPL-3',
    'version': '19.0.1.0.0',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'wizard/booking_request_wizard_views.xml',
        'wizard/booking_cancel_wizard_views.xml',
        'views/apartment_unit_views.xml',
        'views/apartment_booking_views.xml',
        'views/apartment_waitlist_views.xml',
    ],
    'installable': True,
    'application': True,
}


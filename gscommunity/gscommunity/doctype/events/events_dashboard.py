from frappe import _

def get_data():
	return {
		'heatmap': False,
		'heatmap_message': _('Events'),
		'fieldname': 'events',
		'transactions': [		
			{
				'label': _('Event Management'),
				'items': ['Competition','Team']
			},
			{
				'label': _('Event Survey'),
				'items': ['Event Survey']
			},
			{
				'label': _('Event Bookings'),
				'items': ['Bookings']
			},
			{
				'label': _('Volunteer'),
				'items': ['Tasks']
			}	
		]
	}
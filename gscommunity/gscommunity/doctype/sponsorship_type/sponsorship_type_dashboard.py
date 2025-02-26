from frappe import _

def get_data():
	return {
		'heatmap': False,
		'heatmap_message': _('Member Activity'),
		'fieldname': 'sponsorship_type',
		'transactions': [
			{
				'label': _('Sponsorship Items'),
				'items': ['Sponsorship Items']
			}
			
		]
	}
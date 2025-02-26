from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Events"),
			"items": [
				{
					"type": "doctype",
					"name": "Events",
					"description": _("Events details."),
				},
				{
					"type": "doctype",
		     		"name": "Event Type",
					"description": _("Events details."),
				},
				{
					"type": "doctype",
		     		"name": "Event Group",
				},
				{
					"type": "doctype",
		     		"name": "Event Halls",
				},
				{
					"type": "doctype",
		     		"name": "Bookings",
				},
				{
					"type": "doctype",
					"name": "Gallery",
				}
			]
		},
		{
			"label": _("Event Management"),
			"items": [
				{
					"type": "doctype",
					"name": "Competition",
				},
				{
					"type": "doctype",
					"name": "Team",
				},
				{
					"type": "doctype",
					"name": "Competition Type",
				},
				{
					"type": "doctype",
					"name": "Age Group",
				}
			]
		},
		{
			"label": _("Event Survey"),
			"items": [
				{
					"type": "doctype",
					"name": "Event Survey",
				},
				{
					"type": "doctype",
					"name": "Event Survey Questions",
				},
				{
					"type": "doctype",
					"name": "Event Survey Response",
				}
			]
		},
		{
			"label": _("Membership"),
			"items": [
				{
					"type": "doctype",
					"name": "Member",
				},
				{
					"type": "doctype",
					"name": "Membership",
				},
				  {
					"type": "doctype",
					"name": "Membership Type",
				},
				{
					"type": "doctype",
					"name": "Old Members",
				},
				{
					"type": "doctype",
					"name": "Existing Members",
				}
			]
		},
		{
			"label": _("Sponsorship"),
			"items": [			    
				{
					"type": "doctype",
					"name": "Sponsors",
				},
				{
					"type": "doctype",
					"name": "Sponsorship Items",
				},
				{
					"type": "doctype",
					"name": "Sponsorship Type",
				},
				{
					"type": "doctype",
					"name": "Sponsorship Features",
				},				
				{
					"type": "doctype",
					"name": "Advertisement",
				}
			]
		},
		{
			"label": _("Donation"),
			"items": [
			    {
					"type": "doctype",
					"name": "Donation",
				},
				{
					"type": "doctype",
					"name": "Donation Category",
				}
			]
		},
		{
			"label": _("Business Listings"),
			"items": [
				{
					"type": "doctype",
					"name": "Yellow Pages",
				},
				{
				    "type": "doctype",
					"name": "Vendors",	
				},
				{
					"type": "doctype",
					"name": "Business Listing Category",
				},
				{
					"type": "doctype",
					"name": "Business Listing Subcategories",
				}

			]
		},
		{
			"label": _("Committee"),
			"items": [
			    {
					"type": "doctype",
					"name": "Committee",
				},
				{
					"type": "doctype",
					"name": "Designation",
				}
			]
		},
		{
			"label": _("Pages"),
			"items": [
				{
					"type": "doctype",
					"name": "Page Type",
				},
				{
					"type": "doctype",
					"name": "Pages",
				},
				 
				{
					"type": "doctype",
					"name": "Menu",
				}
			]
		},
        {
			"label": _("Accounts"),
			"items": [
				{
					"type": "doctype",
					"name": "Payment Entries",
				},
				{
					"type": "doctype",
					"name": "Expense",
				},
				{
					"type": "doctype",
					"name": "Expense Claims",
				},
				{
					"type": "doctype",
					"name": "Expense Category",
				},
				{
					"type": "doctype",
					"name": "Accounting Category",
				},
				{
					"type": "doctype",
					"name": "Budget Income And Expense",
				}
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "About Us Settings",
					"description": _("About Us."),
				},
				{
					"type": "doctype",
					"name": "HomeSliders",
					"description": _("Home page sliders"),
				},
				{
					"type": "doctype",
					"name": "Samaj Darshan",
				},	
				{
					"type": "doctype",
					"name": "FAQ",
				},	
				{
					"type": "doctype",
					"name": "General Settings",
				},				
				
				{
					"type": "doctype",
					"name": "Relationship Group",
				},
				{
					"type": "doctype",
					"name": "Relationship",
				},
				{
					"type": "doctype",
					"name": "Colors",
				},
			]
		}
	]

// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Choreographer Event Report"] = {
	"filters": [
		{
			"fieldname":"events",
			"label": __("Events"),
			"fieldtype": "Link",
			"options": "Events",
			"reqd": 0			
		},
		{
			"fieldname":"competition",
			"label": __("Competition"),
			"fieldtype": "Link",
			"options": "Competition",
			"reqd": 0,
			"get_query": function() {
				return{
					filters: {
						"events": frappe.query_report_filters_by_name.events.value
					}
				};
			}		
		}
	]
}

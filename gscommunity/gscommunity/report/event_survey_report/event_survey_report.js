// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Event Survey Report"] = {
	"filters": [
		{
			"fieldname":"events",
			"label": __("Event"),
			"fieldtype": "Link",
			"options": "Events",
			"reqd": 1
		},
		{
			"fieldname":"event_survey",
			"label": __("Event Survey"),
			"fieldtype": "Link",
			"options": "Event Survey",
			"reqd": 1,
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

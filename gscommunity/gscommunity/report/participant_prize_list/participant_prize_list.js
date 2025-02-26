// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Participant Prize list"] = {
	"filters": [
		{
			"fieldname":"events",
			"label": __("Events"),
			"fieldtype": "Link",
			"options": "Events",
			"reqd": 1
			// "default": frappe.defaults.get_user_default("Company")
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
			// "default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"prize_type",
			"label": __("Prize Type"),
			"fieldtype": "Select",
			"options": "\nTrophy\nCertificate\nNone",
			"reqd": 0
			// "default": frappe.defaults.get_user_default("Company")
		},
	]
}

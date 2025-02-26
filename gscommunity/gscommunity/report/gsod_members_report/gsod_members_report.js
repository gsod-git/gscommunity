// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GSOD Members Report"] = {
	"filters": [
       {
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Int",
			
		},
		{
			"fieldname":"membership_type",
			"label": __("Membership Type"),
			"fieldtype": "Link",
			"options": "Membership Type",
			"reqd": 1
			// "default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"active",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive",
			// "default": frappe.defaults.get_user_default("Company")
		}
	]
}

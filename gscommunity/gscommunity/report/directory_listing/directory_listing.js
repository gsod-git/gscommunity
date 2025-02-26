// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Directory Listing"] = {
	"filters": [
		{
			"fieldname":"membership_type",
			"label": __("Membership Type"),
			"fieldtype": "Link",
			"options": "Membership Type",
			"reqd": 0
			// "default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nActive\nIn Active",
			"reqd": 0
			// "default": frappe.defaults.get_user_default("Company")
		},
	]
}

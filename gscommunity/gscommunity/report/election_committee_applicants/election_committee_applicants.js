// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Election Committee Applicants"] = {
	"filters": [
		{
			"fieldname":"payment_date",
			"label": __("Payment Date"),
			"fieldtype": "Date",
			"options": "",
			"reqd": 1
		},
		{
			"fieldname":"emails",
			"label": __("Emails"),
			"fieldtype": "Data",
			"options": "",
			"reqd": 0
		},
	]
}

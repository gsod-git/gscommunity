// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Samaj Darshan - Mailing List"] = {
	"filters": [
		{
			"fieldname":"samaj_darshan",
			"label": __("Mail Type"),
			"fieldtype": "Select",
			"options": "\nElectronic Mail\nMail\nBoth",
			"reqd": 0
			// "default": frappe.defaults.get_user_default("Company")
		},
	]
}

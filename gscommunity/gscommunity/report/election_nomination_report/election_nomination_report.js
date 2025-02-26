// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Election Nomination Report"] = {
	"filters": [
		{
			"fieldname":"elections",
			"label": __("Elections"),
			"fieldtype": "Link",
			"options": "Elections",
			"reqd": 1
		}
	]
}

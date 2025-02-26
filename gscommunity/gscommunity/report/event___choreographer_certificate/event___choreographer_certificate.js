// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Event - Choreographer Certificate"] = {
	"filters": [
		{
			"fieldname":"events",
			"label": __("Events"),
			"fieldtype": "Link",
			"options": "Events",
			"reqd": 1			
		}
	]
}

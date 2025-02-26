// Copyright (c) 2016, valiantsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Committee Members Report"] = {
	"filters": [
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
			
		},
		{
			"fieldname":"committee",
			"label": __("Committee"),
			"fieldtype": "Link",
			"options": "Committee",
			"reqd": 1			
		}
	],
	"onload": function() {
		return frappe.call({
			method: "gscommunity.gscommunity.report.committee_members_report.committee_members_report.get_years",
			callback: function(r) {
				console.log(r.message)
				var year_filter = frappe.query_report_filters_by_name.year;
				year_filter.df.options = r.message;
				year_filter.df.default = r.message.split("\n")[0];
				year_filter.refresh();
				year_filter.set_input(year_filter.df.default);
			}
		});
	}
}

// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('General Settings', {
	refresh: function(frm) {
		frm.set_query("yellow_page_plan", "table_19", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.general_settings.general_settings.get_sponsor_items"                
            };
        });
        frm.set_query("role", "roles", function(doc, cdt, cdn) {
            return {
                filters:{
                	"role_name": ["not in","System Manager,Administrator,Guest,All"]
                }                
            };
        });
	}
});
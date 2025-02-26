// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Events', {
    refresh: function(frm) {
    	cur_frm.set_query("accounting_head", function() {
            return {
                "filters": {
                    "accounting_group": (frm.doc.accounting_group)
                }
            };
        });
    },
    onload: function(frm) {


    }
});
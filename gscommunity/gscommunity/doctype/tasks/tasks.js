// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tasks', {
    refresh: function(frm) {        
        frm.set_query("member", "table_11", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.tasks.tasks.get_members",
                filters:{
                	task_type:frm.doc.task_type,
                    events:frm.doc.events
                }
            };
        });
    }
});
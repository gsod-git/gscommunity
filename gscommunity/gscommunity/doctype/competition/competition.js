// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Competition', {
    refresh: function(frm) {
        frm.set_query("events", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.team.team.get_upcoming_events"

            };
        });
        frm.set_query("team", "table_11", function(doc, cdt, cdn) {
            return {
                filters: {
                    'competition': frm.doc.name,
                }
            };
        });
    }
});
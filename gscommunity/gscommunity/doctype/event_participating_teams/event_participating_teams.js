// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event Participating Teams', {
    refresh: function(frm) {
        frm.set_query("event", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.event_participating_teams.event_participating_teams.get_upcoming_events"

            };
        });
        frm.set_query("member", "table_7", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.event_participating_teams.event_participating_teams.get_members"
            };
        });
        frm.set_query("color", "table_15", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.event_participating_teams.event_participating_teams.get_hall_color",
                txt:frm.doc.event
            };
        });        
    }
});
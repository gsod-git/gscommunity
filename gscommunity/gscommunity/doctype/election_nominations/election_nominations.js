// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Election Nominations', {
    refresh: function(frm) {
        frm.set_query("designation", "election_nomination_choice", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.election_nominations.election_nominations.get_designation",
                txt: frm.doc.election
            };
        });        
    }    
});	
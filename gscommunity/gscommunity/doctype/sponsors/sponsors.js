// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sponsors', {
	refresh: function(frm) {
}
});

frappe.ui.form.on("Sponsors", "sponsorship_type", function(frm, cdt, cdn) {

if(frm.doc.validity){
		 frappe.call({
        method: "gscommunity.gscommunity.doctype.sponsors.sponsors.add_months",
        args: {
      "date":frm.doc.starts_on,
      "months":frm.doc.validity,
        },
        callback: function(r) {
        	if(r){
        		frm.set_value("expires_on", r.message);
        	}
		
	}
})
}

});
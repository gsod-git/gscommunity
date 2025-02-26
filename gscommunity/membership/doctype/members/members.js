// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Members', {
	refresh: function(frm) {
	frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Members'};
	frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);
	}
});

// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bookings', {
    refresh: function(frm) {
        var name = ''
        if (frm.doc.docstatus == 1) {
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_payment_entry',
                args: {
                    'doctype': frm.doctype,
                    'ref_id': frm.doc.name
                },
                callback: function(data) {
                    if (data.message != undefined) {
                        name = data.message[0].name;
                        frm.add_custom_button(__('View Payment Entry'), function() {
                            frappe.set_route("Form", "Payment Entries", name);
                        });
                    } else {
                        frm.add_custom_button(__('Make Payment Entry'), function() {
                            frappe.set_route("Form", "Payment Entries", "New Payment Entries", 
                            	{ 
                            		paid_amount:frm.doc.total_amount,
                            		has_reference: 1, 
                            		payment_for: frm.doctype, 
                            		ref_id: frm.doc.name,
                            		member:frm.doc.member,
                                    accounting_head:frm.doc.accounting_category,
                                    payment_type:'Credit'                   		
                            	});
                        });
                    }
                }
            })
        }
    }
});
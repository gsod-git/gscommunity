// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense', {
    refresh: function(frm) {
        cur_frm.set_query("events", function() {
            return {
                "filters": {
                    "event_type": (frm.doc.event_type)
                }
            };
        });
        cur_frm.set_query("accounting_category", function() {
            return {
                "filters": {
                    "accounting_group": (frm.doc.accounting_group)
                }
            };
        });
        if(frm.doc.docstatus==1){
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
                            frappe.set_route("Form", "Payment Entries", "New Payment Entries", {
                                has_reference: 1,
                                payment_for: frm.doctype,
                                ref_id: frm.doc.name,
                                paid_amount: frm.doc.amount,
                                member: frm.doc.member,
                                accounting_head:frm.doc.accounting_category,
                                payment_type:'Debit'
                            });
                        });
                    }
                }
            })
        }
    }
});
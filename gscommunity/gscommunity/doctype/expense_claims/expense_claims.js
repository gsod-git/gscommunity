// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Claims', {
    refresh: function(frm) {
        cur_frm.set_query("accounting_category", function() {
            return {
                "filters": {
                    "accounting_group": (frm.doc.accounting_group)
                }
            };
        });
        if(frm.doc.status=='Approved' && frm.doc.expense_id){
        	frappe.call({
                method: 'gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_payment_entry',
                args: {
                    'doctype': "Expense",
                    'ref_id': frm.doc.expense_id
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
                                payment_for: "Expense",
                                ref_id: frm.doc.expense_id,
                                paid_amount: frm.doc.sanctioned_amount,
                                member: frm.doc.member,
                                accounting_head:frm.doc.accounting_category,
                                payment_type:'Debit'
                            });
                        });
                    }
                }
            })
        }
    },
    events:function(frm){
        if(frm.doc.events){
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    'doctype': "Events",
                    'filters': { 'name': frm.doc.events },
                    'fieldname': [
                        'accounting_group','accounting_head'
                    ]
                },
                callback: function(data) {
                    console.log(data.message.name)
                    if (data.message) {
                        frm.set_value("accounting_group", data.message.accounting_group);
                        frm.set_value("accounting_category", data.message.accounting_head);
                    }
                }
            })
        }
    }
});
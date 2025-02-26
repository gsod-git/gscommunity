// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Donation', {
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
                            frappe.new_doc("Payment Entries", {
                                "has_reference": 1,
                                "payment_for": frm.doctype,
                                "ref_id": frm.doc.name,
                                "paid_amount": frm.doc.donation_amount,
                                "member":frm.doc.member,
                                "accounting_head":frm.doc.accounting_head,
                                "payment_type":'Credit'
                            });
                        });
                    }
                }
            })
        }
    },phone:function(frm){
        if(frm.doc.phone){
            var regex=/[0-9]+$/;
            if(!regex.test(frm.doc.phone)){
                frm.set_value("phone", '');
                frappe.throw('Please enter a valid phone number')                
            }
        }
    },email:function(frm){
        if(frm.doc.email){
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            if(!regex.test(frm.doc.email)){
                frm.set_value("email", '');
                frappe.throw('Please enter a valid email id')                
            }
        }
    },zip_code:function(frm){
        if(frm.doc.zip_code){
            var regex=/[0-9]+$/;
            if(!regex.test(frm.doc.zip_code)){
                frm.set_value("zip_code", '');
                frappe.throw('Please enter a zip code')                
            }
        }
    },
    member:function(frm){
        if(frm.doc.member){
            frappe.call({
                method:'frappe.client.get_value',
                args:{
                    'doctype': "Member",
                    'filters': { 'name': frm.doc.member },
                    'fieldname': [
                    'email'
                    ]
                },callback:function(data){
                    frm.set_value('email',data.message.email)
                }
            })
        }
    }
});
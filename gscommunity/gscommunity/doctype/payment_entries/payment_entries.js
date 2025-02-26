// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entries', {
    refresh: function(frm) {
        if (frm.doc.__islocal) {
            if (frm.doc.payment_for) {
                frappe.call({
                    method: 'gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_docnames',
                    args: {
                        doctype: frm.doc.payment_for
                    },
                    callback: function(data) {
                        var html = '';
                        if (data.message != undefined) {
                            html = '<option></option>'
                            for (var i = 0; i < data.message.length; i++) {
                                html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>';
                            }
                            $('select[data-fieldname=ref_id]').html(html)
                            if (frm.doc.ref_id) {
                                $('select[data-fieldname=ref_id]').val(frm.doc.ref_id)
                            }
                        } else {
                            $('select[data-fieldname=ref_id]').html(html)
                        }
                    }
                })
            }
        }
        // if (frm.doc.payment_for && frm.doc.ref_id) {
        //     console.log(frm.doc.payment_for)
        //     frm.set_query("member", function(frm) {
        //         return {
        //             query: "gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_member",
        //             filters: {
        //                 doctype: frm.doc.payment_for,
        //                 docname: frm.doc.ref_id
        //             }
        //         };
        //     });
        // }
    }
});
frappe.ui.form.on('Payment Entries', 'payment_for', function(frm, cdt, cdn) {
    if(frm.doc.payment_for){
        frappe.call({
            method: 'gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_docnames',
            args: {
                doctype: frm.doc.payment_for
            },
            callback: function(data) {
                var html = '';
                if (data.message != undefined) {
                    html = '<option></option>'
                    for (var i = 0; i < data.message.length; i++) {
                        html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>';
                    }
                    $('select[data-fieldname=ref_id]').html(html)
                } else {
                    $('select[data-fieldname=ref_id]').html(html)
                }
            }
        })
    }
})
frappe.ui.form.on('Payment Entries', 'ref_id', function(frm, cdt, cdn) {
    // if (frm.doc.payment_for && frm.doc.ref_id) {
    //     console.log(frm.doc.payment_for)
    //     frm.set_query("member", function(frm) {
    //         return {
    //             query: "gscommunity.gscommunity.doctype.payment_entries.payment_entries.get_member",
    //             filters: {
    //                 doctype: frm.doc.payment_for,
    //                 docname: frm.doc.ref_id
    //             }
    //         };
    //     });
    // }
})
// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sponsorship Items', {
    refresh: function(frm) {
        cur_frm.set_query("accounting_head", function() {
            return {
                "filters": {
                    "accounting_group": (frm.doc.accounting_group)
                }
            };
        });
        if(frm.doc.__islocal){
            var html='Please save the document to add yellowpage features'
            $('div[data-fieldname="yellowpage_feature"]').html(html)    
        }
        if (frm.doc.sponsorship_type && !frm.doc.__islocal) {
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_sponsor_feature',
                args: {
                    type: frm.doc.sponsorship_type
                },
                callback: function(data) {
                    if (data.message[0].enable_yellowpage == 1) {
                        $('div[data-fieldname="yellowpage_feature"]').parent().parent().parent().parent().show()
                        frappe.call({
                            method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_yellowpage_feature',
                            args: {

                            },
                            callback: function(data) {
                                var html = '<div id="yp_feature">'
                                for (var i = 0; i < data.message.length; i++) { 
                                    html += '<div class="col-md-3"><div class="checkbox"><label><span class="input-area">';
                                    html += '<input type="checkbox" autocomplete="off" class="input-with-feedback" name="yp" label="'+data.message[i].label+'" value="' + data.message[i].fieldname + '"  /></span>';
                                    html += '<span class="disp-area" style="display:none"><i class="octicon octicon-check" style="margin-right: 3px;"></i></span>';
                                    html += '<span class="label-area small">' + data.message[i].label + '</span></label>'
                                    html += '<p class="help-box small text-muted"></p></div></div>'
                                }
                                html += '</div>'
                                $('div[data-fieldname="yellowpage_feature"]').html(html)
                                if (!frm.doc.__islocal) {
                                    frappe.call({
                                        method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_selected_yp_feature',
                                        args: {
                                            name: frm.doc.name
                                        },
                                        callback: function(r) {
                                            if (r.message != undefined) {
                                                for (var k = 0; k < r.message.length; k++) {
                                                    $('input[value="' + r.message[k].section + '"]').attr('checked', true)
                                                }
                                            }
                                        }
                                    })
                                }

                            }
                        })
                    } else {
                        $('div[data-fieldname="yellowpage_feature"]').parent().parent().parent().parent().hide()
                    }
                }
            })
        }
    },
    validate: function(frm) {
        if (!frm.doc.__islocal) {
            $('input[value="business_details"]').attr('checked','checked')
            $('input[value="contact_details"]').attr('checked','checked')            
            $('input[name="yp"]').each(function() {                
                frappe.call({
                    method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.add_yp_feature',
                    args: {
                        section: this.value,
                        docname: frm.doc.name,
                        label: $(this).attr('label'),
                        checked: this.checked
                    },
                    callback: function(data) {
                        console.log(data.message)
                    }
                })
            });
        }
    }
});
frappe.ui.form.on('Sponsorship Items', 'sponsorship_type', function(frm, cdt, cdn) {
    if (frm.doc.sponsorship_type) {
        frappe.call({
            method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_items',
            args: {
                sponsorship_type: frm.doc.sponsorship_type
            },
            callback: function(data) {
                var html = '';
                if (data.message == undefined) {
                    $('select[data-fieldname=sponsor_for]').html(html)
                    $('select[data-fieldname=sponsor_for]').parent().parent().parent().parent().hide()
                } else if (data.message.length > 0) {
                    html = '<option></option>'
                    if (frm.doc.sponsorship_type == 'Samaj Darshan') {
                        for (var i = 0; i < data.message.length; i++) {
                            var list = data.message[i].list;
                            for (var j = 0; j < list.length; j++) {
                                var value = list[j].month + '-' + data.message[i].year;
                                html += '<option value="' + value + '">' + value + '</option>';
                            }
                        }
                    } else {
                        for (var i = 0; i < data.message.length; i++) {
                            html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>';
                        }
                    }

                    $('select[data-fieldname=sponsor_for]').html(html)
                    $('select[data-fieldname=sponsor_for]').parent().parent().parent().parent().show()
                } else {
                    $('select[data-fieldname=sponsor_for]').parent().parent().parent().parent().hide()
                }
            }
        })
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_sponsor_feature',
                args: {
                    type: frm.doc.sponsorship_type
                },
                callback: function(data) {
                    if (data.message[0].enable_yellowpage == 1) {
                        $('div[data-fieldname="yellowpage_feature"]').parent().parent().parent().parent().show()
                        frappe.call({
                            method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_yellowpage_feature',
                            args: {

                            },
                            callback: function(data) {
                                var html = '<div id="yp_feature">'
                                for (var i = 0; i < data.message.length; i++) {
                                    html += '<div class="col-md-3"><div class="checkbox"><label><span class="input-area">';
                                    html += '<input type="checkbox" autocomplete="off" class="input-with-feedback" name="yp" label="'+data.message[i].label+'" value="' + data.message[i].fieldname + '" /></span>';
                                    html += '<span class="disp-area" style="display:none"><i class="octicon octicon-check" style="margin-right: 3px;"></i></span>';
                                    html += '<span class="label-area small">' + data.message[i].label + '</span></label>'
                                    html += '<p class="help-box small text-muted"></p></div></div>'
                                }
                                html += '</div>'
                                $('div[data-fieldname="yellowpage_feature"]').html(html)
                            }
                        })
                    } else {
                        $('div[data-fieldname="yellowpage_feature"]').parent().parent().parent().parent().hide()
                    }
                }
            })
        }else{
            var html='Please save the document to add yellowpage features'
            $('div[data-fieldname="yellowpage_feature"]').html(html)
        }
    }
})
frappe.ui.form.on('Sponsorship Items', 'sponsor_for', function(frm, cdt, cdn) {
    if (frm.doc.sponsor_for) {
        frappe.call({
            method: 'gscommunity.gscommunity.doctype.sponsorship_items.sponsorship_items.get_account_head',
            args: {
                docname: frm.doc.sponsor_for,
                doctype: frm.doc.sponsorship_type
            },
            callback: function(data) {
                var html = '';
                if (data.message != undefined) {
                    frm.set_value("accounting_head", data.message.accounting_head);
                    frm.set_value("accounting_group", data.message.accounting_group);
                }
            }
        })
    }
})
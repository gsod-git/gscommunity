// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advertisement', {
    refresh: function(frm) {
        frm.set_query("page", function(frm) {
            return {
                filters: {
                    'has_web_view': 1,
                    'module':'Gscommunity'
                }
            }
        });
        if(!cur_frm.doc.__islocal && cur_frm.doc.status=='Waiting for approval'){
            cur_frm.add_custom_button(__('Approve'), function() {
                frappe.call({
                    method:"gscommunity.gscommunity.doctype.advertisement.advertisement.change_status",
                    args:{
                        name:cur_frm.doc.name,
                        status:'Approved'
                    },
                    callback:function(data){
                        location.reload(true);
                    }
                })
            });
        }
        if(cur_frm.doc.status!='Waiting for approval'){
            $('select[data-fieldname="status"]').parent().hide();
            $('select[data-fieldname="status"]').parent().parent().find('.like-disabled-input').css('display','block')
        }else{
            $('select[data-fieldname="status"]').attr('disabled',false)
        }
    }
});
frappe.ui.form.on("Advertisement", "sponsor", function(frm, cdt, cdn) {
    if (frm.doc.sponsor) {
        frappe.call({
            method: "gscommunity.gscommunity.doctype.advertisement.advertisement.get_duration",
            args: {
                "sponsor": frm.doc.sponsor
            },
            callback: function(r) {
                console.log(r.message)
                if(r){
                    frm.set_value("slot_timing", r.message.advertisement_timing);
                    frm.set_value("start_date", r.message.starts_on);
                    frm.set_value("end_date", r.message.expires_on);
                }
            }
        })
    }
});
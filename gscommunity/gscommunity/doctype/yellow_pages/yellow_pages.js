// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Yellow Pages', {
    onload: function(frm) {
    	cur_frm.set_query("subcategory", function() {
            return {
                "filters": {
                    "category": cur_frm.doc.category
                }
            };
        });
    },
    refresh:function(frm){
        if(!cur_frm.doc.__islocal && cur_frm.doc.status=='Waiting for approval'){
            cur_frm.add_custom_button(__('Approve'), function() {
                frm.set_value('status','Approved');
                frm.set_value('published',1);
                cur_frm.save()
            });
        }
        if(cur_frm.doc.status!='Waiting for approval'){
            $('select[data-fieldname="status"]').parent().hide();
            $('select[data-fieldname="status"]').parent().parent().find('.like-disabled-input').css('display','block')
        }else{
            $('select[data-fieldname="status"]').attr('disabled',false)
        }
        cur_frm.set_query("sponsor", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.yellow_pages.yellow_pages.get_sponsors"

            };
        });
        cur_frm.set_query("user", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.yellow_pages.yellow_pages.get_user"

            };
        });     
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
    }
});
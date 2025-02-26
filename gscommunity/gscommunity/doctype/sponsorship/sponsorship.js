// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sponsorship', {
    refresh: function(frm) {
        var yp_count=1, ad_count=1;
        if(frm.doc.__islocal){

        }
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
                            frappe.set_route("Form", "Payment Entries", "New Payment Entries", {
                                has_reference: 1,
                                payment_for: frm.doctype,
                                ref_id: frm.doc.name,
                                paid_amount: frm.doc.amount,
                                member: frm.doc.member,
                                accounting_head:frm.doc.accounting_head,
                                payment_type:'Credit'
                            });
                        });
                    }
                }
            })
            frappe.call({
                method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_sponsor_feature',
                args: {
                    plan: frm.doc.sponsorship_plan
                },
                callback: function(data) {
                    console.log(data.message)
                    var x = data.message
                    if(x[0].enable_yellowpage){
                        yp_count=1
                    }else{
                        yp_count=0
                    }
                    var html = '<div><p>You can add an yellow page for the selected sponsorship type.';                    
                    html += ' </p><input type="hidden" id="yp_count" value="' + yp_count + '"/></div>'
                    $('div[data-fieldname="yellow_page_count"]').html(html)
                    var html2 = '<div><p>You can add an advertisement for the selected sponsorship type.';                    
                    html2 += ' </p><input type="hidden" id="ad_count" value="' + ad_count + '"/></div>'
                    $('div[data-fieldname="advertisement_count"]').html(html2)
                    if (yp_count == 0) {
                        $('button[data-fieldname="add_new_yellow_page"]').hide();
                    }
                    if (ad_count == 0) {
                        $('button[data-fieldname="add_new_advertisement"]').hide();
                    }
                }
            })
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship.sponsorship.get_yellowpage_detail',
                args: {
                    name: frm.doc.name
                },
                callback: function(data) {
                    console.log(data.message)
                    if (data.message != '0') {
                        var x = data.message;
                        var html = '<table class="table table-bordered"><thead style="background:#f7fafc"><tr style="border-color: #d1d8dd;"><th style="font-size:12px;padding:11px;border-width:1px;">Business Name</th><th style="font-size:12px;padding:11px;border-width:1px;">Category</th>'
                        html += '<th style="font-size:12px;padding:11px;border-width:1px;">Sub Category</th><th style="font-size:12px;padding:11px;border-width:1px;">Website Url</th><th style="font-size:12px;padding:11px;border-width:1px;">View Count</th></tr></thead><tbody>';
                        for (var i = 0; i < x.length; i++) {
                            html += '<tr style="border-color: #d1d8dd;"><td style="padding:11px;"><a href="#Form/Yellow%20Pages/' + x[i].name + '">' + x[i].business_name + '</a></td><td style="padding:11px;">' + x[i].category + '</td><td style="padding:11px;">' + x[i].subcategory + '</td><td style="padding:11px;">' + x[i].website_url + '</td><td style="padding:11px;">' + x[i].view_count + '</td></tr>';
                        }
                        html += '</tbody></table>';
                        $('div[data-fieldname="yellow_page_detail"]').html(html)
                        var yellowpage = x.length;
                        if (x.length == yp_count) {
                            $('button[data-fieldname="add_new_yellow_page"]').hide();
                            $('div[data-fieldname="yellow_page_count"]').hide()
                        }
                    } else {
                        $('div[data-fieldname="yellow_page_detail"]').html('')
                    }
                }
            })
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship.sponsorship.get_advertisement_detail',
                args: {
                    name: frm.doc.name
                },
                callback: function(data) {
                    console.log(data.message)
                    if (data.message != '0') {
                        var x = data.message;
                        var html = '<table class="table table-bordered"><thead style="background:#f7fafc"><tr style="border-color: #d1d8dd;"><th style="font-size:12px;padding:11px;border-width:1px;">Adverisement Name</th><th style="font-size:12px;padding:11px;border-width:1px;">Redirect Url</th>'
                        html += '<th style="font-size:12px;padding:11px;border-width:1px;">Slot Timing</th><th style="font-size:12px;padding:11px;border-width:1px;">Published</th></tr></thead><tbody>';
                        for (var i = 0; i < x.length; i++) {
                            html += '<tr style="border-color: #d1d8dd;"><td style="padding:11px;"><a href="#Form/GSOD Promotions/' + x[i].name + '">' + x[i].advertisement_name + '</a></td><td style="padding:11px;">' 
                            if(x[i].redirect_url)
                                html+= x[i].redirect_url 
                            html+= '</td><td style="padding:11px;">' + x[i].slot_timing + '</td><td style="padding:11px;">';
                            html += '<input type="checkbox"';
                            if (x[0].view_count == 1) {
                                html += ' checked="checked"'
                            }
                            html += '/></td></tr>';
                        }
                        html += '</tbody></table>';
                        $('div[data-fieldname="advertisement_detail"]').html(html)
                        var ad = x.length;
                        if (x.length == ad_count) {
                            $('button[data-fieldname="add_new_advertisement"]').hide();
                            $('div[data-fieldname="advertisement_count"]').hide()
                        }
                    } else {
                        $('div[data-fieldname="advertisement_detail"]').html('')
                        $('button[data-fieldname="add_new_advertisement"]').show();
                    }
                }
            })
        }
    },
    add_new_yellow_page: function(frm) {
        var dialog = new frappe.ui.Dialog({
            title: __("New Yellow Page"),
            fields: [
                { fieldtype: "Data", fieldname: "business_name", label: __("Business Name"), reqd: 1 },
                { fieldtype: "Link", fieldname: "category", label: __("Category"), reqd: 1, options: "Business Listing Category" },
                { fieldtype: "Link", fieldname: "subcategory", label: __("Sub Category"), reqd: 0, options: "Business Listing Subcategories" },
                { fieldtype: "Data", fieldname: "email", label: __("Email"), reqd: 1 },
                { fieldtype: "Data", fieldname: "phone", label: __("Phone"), reqd: 1 },
                { fieldtype: "Data", fieldname: "address", label: __("Address"), reqd: 1 },
                { fieldtype: "Data", fieldname: "city", label: __("City"), reqd: 1 },
                { fieldtype: "Data", fieldname: "state", label: __("State"), reqd: 1 },
                { fieldtype: "Data", fieldname: "zip_code", label: __("Zip Code"), reqd: 1 },
            ]
        });

        dialog.set_primary_action(__("Save"), function() {
            var btn = this;
            var values = dialog.get_values();
            var published = 0
            if (frm.doc.paid) {
                published = 1
            }
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship.sponsorship.add_yellow_page',
                args: {
                    b_name: values.business_name,
                    b_type: 'Sponsor',
                    sponsor: frm.doc.name,
                    category: values.category,
                    subcategory: values.subcategory,
                    email: values.email,
                    phone: values.phone,
                    address: values.address,
                    city: values.city,
                    state: values.state,
                    zip_code: values.zip_code,
                    published: published
                },
                callback: function(data) {
                    dialog.hide();
                    location.reload(true);
                }
            })


        });

        dialog.show();
    },
    add_new_advertisement: function(frm) {
        var dialog = new frappe.ui.Dialog({
            title: __("New Advertisement"),
            fields: [
                { fieldtype: "Data", fieldname: "advertisement_name", label: __("Advertisement Name"), reqd: 1 },
                { fieldtype: "Data", fieldname: "redirect_url", label: __("Redirect Url"), reqd: 1 },

            ]
        });

        dialog.set_primary_action(__("Save"), function() {
            var btn = this;
            var values = dialog.get_values();
            var published = 0
            if (frm.doc.paid) {
                published = 1
            }
            frappe.call({
                method: 'gscommunity.gscommunity.doctype.sponsorship.sponsorship.add_advertisement',
                args: {
                    ad_name: values.advertisement_name,
                    redirect_url: values.redirect_url,
                    sponsor: frm.doc.name,
                    start_date: frm.doc.starts_on,
                    end_date: frm.doc.expires_on,
                    published: published,
                    sponsorship_plan: frm.doc.sponsorship_plan,
                    sponsorship_type:frm.doc.sponsorship_type
                },
                callback: function(data) {
                    dialog.hide();
                    location.reload(true);
                }
            })


        });

        dialog.show();
    },phone:function(frm){
        if(frm.doc.phone){
            var regex=/[0-9]+$/;
            if(!regex.test(frm.doc.phone)){
                frm.set_value("phone", "");
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
frappe.ui.form.on("Sponsorship", "refresh", function(frm) {
    cur_frm.set_query("sponsorship_plan", function() {
        return {
            "filters": {
                "sponsorship_type": (frm.doc.sponsorship_type)
            }
        };
    });
});
frappe.ui.form.on("Sponsorship", "sponsorship_plan", function(frm, cdt, cdn) {
    if (frm.doc.sponsorship_plan) {
        // frappe.call({
        //     method: "gscommunity.gscommunity.doctype.sponsorship.sponsorship.get_expiry_date",
        //     args: {
                
        //     },
        //     callback: function(r) {
        //         if (r) {
        //             frm.set_value("expires_on", r.message);
        //         }

        //     }
        // })
    }
});

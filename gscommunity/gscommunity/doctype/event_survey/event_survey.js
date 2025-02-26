// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event Survey', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('View Response'), function() {
                frappe.call({
                    method: "gscommunity.gscommunity.doctype.event_survey.event_survey.get_response",
                    args: {
                        name: frm.doc.name
                    },
                    callback: function(data) {
                        console.log(data.message)
                        if (data.message != undefined) {
                            var html = '<div><ul>'
                            var total_response = 0;
                            for (var i = 0; i < data.message.length; i++) {
                                html += '<li>' + data.message[i].question_name + '</li>';
                                html += '<div class="row"><ul style="list-style:none;">';
                                total_response = data.message[i].total_response;
                                $.each(data.message[i].options, function(key, value) {
                                    html += '<li>' + value.options;
                                    var response_percent = Math.round((parseInt(value.response_count) / parseInt(total_response)) * 100);
                                    // html+='<div class="col-xs-4"><p>'+response_percent+'%</p></div>';
                                    if(value.response_count==0){
                                    	response_percent=0
                                    }
                                    html += '<span style="float:right;margin-right: 10%;">' + response_percent + ' %</span></li>'
                                })
                                html += '</ul></div>'
                            }
                            html += '</ul></div>'
                            frappe.msgprint(html, 'Survey Response')
                        }else{
                        	frappe.msgprint('No questions have been added for this survey','Alert');
                        }
                    }
                })
            });
        }
    }
});
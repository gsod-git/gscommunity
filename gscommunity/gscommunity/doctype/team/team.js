// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt
var reference = 0;
frappe.ui.form.on('Team', {
    onload:function(frm){
        // cur_frm.page.btn_primary.addClass('hide')
        cur_frm.page.btn_primary.hide()

        $(cur_frm.page.page_actions).find('.custom-save').remove();
        cur_frm.page.page_actions.append('<button class="btn btn-primary btn-sm custom-save">Save</button>')
        $(cur_frm.page.page_actions).find('.custom-save').click(function(){
            var participant_count = cur_frm.doc.table_7.length;
            reference=1;
            if(parseInt(cur_frm.doc.min_participants)>parseInt(participant_count)){
                frappe.confirm(
                    'Minimum participants of ' + cur_frm.doc.min_participants + ' required for a team. Would you like to add participants later?',
                    function(){
                        cur_frm.set_value('flag', 'yes');
                        cur_frm.save();
                        reload_doc(cur_frm);
                    },
                    function(){
                        cur_frm.set_value('flag', '');
                    }
                    )
            }else{
                cur_frm.set_value('flag', 'yes');
                cur_frm.save();
                reload_doc(cur_frm)
            }
        })
    },
    refresh: function(frm) {
        frm.set_query("events", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.team.team.get_upcoming_events"

            };
        });
        frm.set_query("color", "table_15", function(doc, cdt, cdn) {
            return {
                query: "gscommunity.gscommunity.doctype.team.team.get_hall_color",
                txt: frm.doc.events
            };
        });
        // frm.set_value('flag', '');
        if (frm.doc.events) {
            hall_color(frm.doc.events)
        }
        if (!frm.doc.__islocal) {
            if (frm.doc.status == 'Waiting for approval') {
                frm.add_custom_button(__('Approve'), function() {
                    frm.set_value('status', 'Approved');
                    validate_active_members(frm)
                    // cur_frm.save();
                });
                frm.add_custom_button(__('Reject'), function() {
                    frappe.confirm(
                        'Are you sure to reject this team?',
                        function() {
                            frm.set_value('status', 'Rejected');
                            cur_frm.save();
                        },
                        function() {
                            // show_alert('Thanks for continue here!')
                        }
                    )
                    // frm.set_value('status', 'Rejected');
                    // cur_frm.save();
                });
            } else if (frm.doc.status == 'Approved') {
                frm.add_custom_button(__('Finalize'), function() {
                    frm.set_value('status', 'Finalized');
                    validate_active_members(frm)
                    // cur_frm.save();
                });
                frm.add_custom_button(__('Reject'), function() {
                    frm.set_value('status', 'Rejected');
                    cur_frm.save();
                });
            } else if (frm.doc.status == 'Rejected') {
                if (frappe.user.has_role('Webmaster')) {
                    frm.add_custom_button(__('Re-Approve'), function() {
                        frappe.confirm(
                            'Are you sure to approve this rejected team again?',
                            function() {
                                frm.set_value('status', 'Approved');
                                validate_active_members(frm)
                            },
                            function() {
                                // show_alert('Thanks for continue here!')
                            }
                        )
                        // cur_frm.save();
                    });
                }
            }
            if (frm.doc.status == 'Finalized') {

            }
        }
        if(frm.doc.competition && !frm.doc.min_paricipants){
            get_min_participants(frm);
        }             
    },
    competition:function(frm){
        if(frm.doc.competition){
            get_min_participants(frm);
        }
    }    
});
var m_team_idx = 0;
var m_team_ref = 0;
frappe.ui.form.on("Event Managing Team", "active", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    if (m_team_idx != item.idx && m_team_ref != 2) {
        m_team_idx = item.idx;
        m_team_ref = 0
    }
    if (item.active == 1) {
        frappe.model.set_value(cdt, cdn, "active", 'Active');
    } else if (item.active == 0) {
        if (m_team_ref != 1 && m_team_idx == item.idx) {
            m_team_ref = 1
            frappe.confirm(
                'Member ' + item.member + ' - ' + item.member_name + ' is not active. Do you want to proceed?',
                function() {
                    frappe.model.set_value(cdt, cdn, "active", 'In Active');
                },
                function() {
                    frappe.model.set_value(cdt, cdn, "member", '');
                    frappe.model.set_value(cdt, cdn, "member_name", '');
                    frappe.model.set_value(cdt, cdn, "active", '');
                    frappe.model.set_value(cdt, cdn, "email", '');
                    frappe.model.set_value(cdt, cdn, "whatsapp_number", '');
                    m_team_ref = 2
                    m_team_idx = 0
                }
            )
        }
    }
});
var part_idx = 0;
var part_ref = 0;
var part_id = '';
frappe.ui.form.on("Event Participating Members", "active", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    if (part_idx != item.idx && part_ref != 2) {
        part_idx = item.idx;
        part_ref = 0
        part_id = item.member
    }
    if (item.active == 1) {
        frappe.model.set_value(cdt, cdn, "active", 'Active');
    } else if (item.active == 0) {
        if (part_ref != 1 && part_idx == item.idx) {
            part_ref = 1
            frappe.confirm(
                'Member ' + item.member + ' - ' + item.member_name + ' is not active. If you want to add the member, he cannot get either trophy or certificate. Do you want to proceed?',
                function() {
                    frappe.model.set_value(cdt, cdn, "active", 'In Active');
                },
                function() {
                    frappe.model.set_value(cdt, cdn, "member", '');
                    frappe.model.set_value(cdt, cdn, "member_name", '');
                    frappe.model.set_value(cdt, cdn, "active", '');
                    part_ref = 2
                    part_idx = 0
                }
            )
        }

    }
});
frappe.ui.form.on("Event Managing Team", "whatsapp_number", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    if (item.whatsapp_number.length != 10 && item.whatsapp_number.length != 0) {
        frappe.model.set_value(cdt, cdn, "whatsapp_number", '');
        frappe.throw('Please enter 10 digit Whatsapp Number for member ' + item.member_name + ' in Event Managing Team')
    }
});
var hall_color = function(event) {
    if (event) {
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.participant_form.participant_form.get_hall_color',
            args: {
                events: event
            },
            callback: function(data) {
                if (data.message == 'All') {
                    // $('div[data-fieldname="table_15"] .grid-row .data-row div[data-fieldname="color"]').hide()
                } else {

                }
            }
        })
    }
}
var validate_active_members = function(frm) {
    var message = ''
    for (var i = 0; i < frm.doc.table_11.length; i++) {
        var member = frm.doc.table_11[i];
        if (member.active != 'Active') {
            if (message == '') {
                message += member.member + ' - ' + member.member_name
            } else {
                message += ', ' + member.member + ' - ' + member.member_name
            }
        }
    }
    if (message == '') {
        validate_active_participants(frm)
    } else {
        frappe.confirm(
            message + ' is/are not active. Do you still want to proceed further?',
            function() {
                validate_active_participants(frm)
            },
            function() {

            }
        )
    }
}
var validate_active_participants = function(frm) {
    var message = ''
    for (var i = 0; i < frm.doc.table_7.length; i++) {
        var member = frm.doc.table_7[i];
        if (member.active != 'Active') {
            if (message == '') {
                message += member.member + ' - ' + member.member_name
            } else {
                message += ', ' + member.member + ' - ' + member.member_name
            }
        }
    }
    if (message == '') {
        frm.set_value('flag', 'yes');
        cur_frm.save()
    } else {
        frappe.confirm(
            message + ' is/are not active. Do you still want to proceed further?',
            function() {
                frm.set_value('flag', 'yes');
                cur_frm.save()
            },
            function() {

            }
        )
    }
}

var reload_doc = function(frm) {
    frappe.call({
        method: 'frappe.desk.form.load.getdoc',
        args: {
            doctype: 'Team',
            name: frm.doc.name
        },
        callback: function(data) {
            reference=0;
        }
    })
}

var get_min_participants=function(frm){
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.participant_form.participant_form.get_competition',
        args: {
            name: frm.doc.competition
        },
        callback:function(data){
            if(data.message){
                frm.set_value('min_participants',data.message.minimum_participants)
            }
        }
    })
}

cur_frm.cscript.validate_curfrm=function(doc){
    console.log(doc)
}

// frappe.ready(function(){

// })

frappe.ready(function() {
    $('.help-block').css({ "padding-left": "15px", "margin-top": "20px" });
    if ($('select[name="membership_type"]').val() == "") {
        $('#table_25').parent().parent().parent().parent().hide();
        var ufname = localStorage.getItem("userfirst_name")
        var ulname = localStorage.getItem("userlast_name")
        var uemail = localStorage.getItem("useremail_id")
        var umobile = localStorage.getItem("usermobile_no")
        $('input[name="member_name"]').val(ufname);
        $('input[name="last_name"]').val(ulname);
        $('input[name="email"]').val(uemail);
        $('input[name="phone_no"]').val(umobile);
    } else {
        var newtype = $('select[name="membership_type"]').val();
        $('input[name="membership"]').val(newtype)
    }
    var active = $('input[name="active"]').val();
    localStorage.setItem('donationamount', $('input[name=membership_amount]').val());
    if (frappe.is_new != 1) {
        $('select[name="membership_type"]').attr('disabled', true)
        var html = '<button class="btn btn-small btn-warning" id="change-membership" onclick="changemembership()">Change Membership</button>';
        $('input[name="active"]').parent().append(html)
        if (active == "1") {
            $('.btn-form-submit').hide()
            get_membership_details()
        } else {
            $('.btn-form-saveonly').hide()
        }
        localStorage.setItem("existing_type", $('select[name=membership_type]').val())
    } else {
        $('.btn-form-saveonly').hide()
        get_user_detail()
    }
    var first_edit=$('input[name=first_edit]').val()
    get_membership_types()
    get_family_validation()
    var self_relation = $('input[name=self_relation]').val();
    if (self_relation == '')
        get_self()
    var newsletter = $('select[name=newsletter] option:selected').val()
    var samaj = $('select[name=samaj_darshan] option:selected').val()
    get_newsletter(newsletter);
    get_samaj(samaj);
    $('.datepicker').show();
    $('#table_25 thead tr td').hide()
    $('#table_25 thead tr th:eq(8)').hide()
    $('#table_25 tbody tr').each(function() {
        $(this).find('input[name="relationship_group"]').parent().parent().hide()
    })
    var initial = $('input[name="membership_amount"]').val();
    localStorage.setItem("initial_amount", initial);
    if (frappe.is_new == 1) {
        var m_type = localStorage.getItem("membership_typename");
        var m_amount = localStorage.getItem("membership_payment");
        if (m_type) {
            $('select[name="membership_type"]').val(m_type);
            $('input[name="membership"]').val(m_type);
            $('input[name="membership_amount"]').val(m_amount);
        }
        localStorage.setItem("membership_typename", "");
        localStorage.setItem("membership_payment", "");
    }
    if (frappe.is_new != 1) {
        $('.btn-remove').parent().hide();
        $('#table_25 thead tr td').hide()
        var newval = $('select[name="membership_type"]').val();
        var mdate = $('div[data-label="Primary Member Info"] input[name="date_of_birth"]').val();
        var memail = $('div[data-label="Primary Member Info"] input[name="email"]').val();
        var exp_date = $('div[data-label="Primary Member Info"] input[name="membership_expiry_date"]').val();
        var state = $('input[name="active"]').val();
        var mrelation = $('select[name="relation"]').val();
        var mgender = $('div[data-label="Primary Member Info"] select[name="gender"]').val();
        var today = new Date();
        var fdate = formatDate(today)

        if (exp_date == "") {
            // $('select[name="membership_type"]').attr('disabled', '');  
        }
        $('input[name="membership"]').val(newval);
        if (mdate == '01-01-1900') {
            $('div[data-label="Primary Member Info"] input[name="date_of_birth"]').val('')
            mdate = ''
        }
        if (mdate != '') {
            $('div[data-label="Primary Member Info"] input[name="date_of_birth"]').attr('disabled', true)
        }
        if (memail) {
            $('div[data-label="Primary Member Info"] input[name="email"]').attr('disabled', true)
        }
        if (mrelation != "") {
            $('select[name="relation"]').attr('disabled', '');
        }
        if ($('input[name="phone_no"]').val() == '0') {
            $('input[name="phone_no"]').val('')
        }
    }
    $('input[name="member_name"]').change(function(e) {
        var news = $('input[name="member_name"]').val();
        if (!/^[a-zA-Z\s]*$/g.test(news)) {
            frappe.msgprint("please enter characters only")
            return false;
        }
    })
    $('input[name="mobile_no"]').change(function(e) {
        var number = $('input[name="mobile_no"]').val();
        if (!validate_number(number)) {
            frappe.msgprint('Please enter a valid whatsapp number', 'Alert')
            $('input[name=mobile_no]').val('');
        } else {
            if (number.length != 10) {
                frappe.msgprint('Please enter 10 digit whatsapp number', 'Alert')
                $('input[name=mobile_no]').val('');
            }
        }
    })
    $('input[name="last_name"]').change(function(e) {
        var news = $('input[name="last_name"]').val();
        if (!/^[a-zA-Z\s]*$/g.test(news)) {
            frappe.msgprint("please enter characters only", 'Alert')
            return false;
        }
    })
    $('input[name=email][data-doctype=Member]').change(function() {
        var email = $('input[name=email][data-doctype=Member]').val()
        if (!validate_email(email)) {
            frappe.msgprint('Please enter a valid email id', 'Alert')
            $('input[name=email][data-doctype=Member]').val('');
        }
    })
    $('input[name=state]').change(function() {
        var state = $('input[name=state]').val()
        if (!validate_state(state)) {
            frappe.msgprint('Please enter 2 digit alpha characters for state name', 'Alert')
            $('input[name=email]').val('');
        }
        if (state.length != 2) {
            frappe.msgprint('State must be 2 digit alpha characters only', 'Alert')
            $('input[name=state]').val('');
        }
    })
    $('input[name=office_no]').change(function() {
        var number = $('input[name=office_no]').val()
        if (!validate_number(number)) {
            frappe.msgprint('Please enter a valid office number', 'Alert')
            $('input[name=office_no]').val('');
        } else {
            if (number.length != 10) {
                frappe.msgprint('Please enter 10 digit office number', 'Alert')
                $('input[name=office_no]').val('');
            }
        }

    })
    $('input[name=home_phone_no]').change(function() {
        var number = $('input[name=home_phone_no]').val()
        if (!validate_number(number)) {
            frappe.msgprint('Please enter a valid home phone number', 'Alert')
            $('input[name=home_phone_no]').val('');
        } else {
            if (number.length != 10) {
                frappe.msgprint('Please enter 10 digit home phone number', 'Alert')
                $('input[name=home_phone_no]').val('');
            }
        }

    })
    $('input[name="middle_name"]').change(function(e) {
        var news = $('input[name="middle_name"]').val();
        var x = news.length;
        if (!/^[a-zA-Z ]*$/g.test(news)) {
            frappe.msgprint("please enter characters only", 'Alert')
            return false;
        } else {
            if (x > 1) {
                frappe.msgprint("Please enter only single character.", 'Alert')
                return false;
            }
        }
    })
    $("#table_25").on("click", "select[name=relation]", function() {
        $("select[name=relation] option[value='Self']").remove();
    })    
    $('input[name="phone_no"][data-doctype=Member]').change(function(e) {
        var number = $('input[name="phone_no"][data-doctype=Member]').val();
        if (!validate_number(number)) {
            frappe.msgprint('Please enter a valid mobile number', 'Alert')
            $('input[name=phone_no][data-doctype=Member]').val('');
        }
        if (number.length != 10) {
            frappe.msgprint('Please enter 10 digit mobile number', 'Alert')
            $('input[name=phone_no][data-doctype=Member]').val('');
        }
    })    
    $('select[name="membership_type"]').change(function(e) {
        get_family_validation()
        var self_relation = $('input[name=self_relation]').val()
        if (self_relation == '')
            get_self()
        $('#Nsub').show();
        var newtype = $('select[name="membership_type"]').val();
        $('select[name="membership_type"]').removeAttr('disabled');
        $('input[name="membership"]').val(newtype);
        var membership_type = $('select[name="membership_type"]').val();
        var active = $('input[name="active"]').val();
        e.preventDefault();
        frappe.call({
            method: "gscommunity.gscommunity.api.get_membership_details",
            args: {
                "membertype": membership_type,
                "old_member_type":localStorage.getItem('existing_type'),
                "is_new":frappe.is_new
            },
            callback: function(r) {
                var membership_info=r.message.membership_details;
                var initial_amt = $('input[name=membership_amount]').val()
                if(!frappe.is_new){
                    if(r.message.has_family==1){
                        if(r.message.failed_response){
                            var html='<p>Sorry! You cannot change your membership since you have '+r.message.failed_response+' as per your previous membership.</p>'
                            html+='<p>If you still want to change your membership, you have to delete those members.</p>'
                            html+='<div style="text-align:right;"><button style="margin-right:10px;" class="btn btn-default" onclick="restoreMembership()">Cancel</button><button onclick="removeMembers(this)" class="btn btn-primary" data-price="'+membership_info.amount+'" data-id="'+r.message.failed_response+'">Delete & Proceed</button></div>';
                            frappe.msgprint(html,'Confirm')
                        }else{
                            if(active=='1'){
                                if (parseFloat(initial_amt) < parseFloat(membership_info.amount)) {
                                    $("input[name=membership_amount]").val(membership_info.amount);
                                    localStorage.setItem('donationamount', membership_info.amount);
                                } else {
                                    frappe.msgprint('You cannot change your membership type which has less amount than the current type.', 'Alert')
                                    $('select[name=membership_type]').val('')
                                }
                            }else{
                                $("input[name=membership_amount]").val(membership_info.amount);
                                localStorage.setItem('donationamount', membership_info.amount);
                                localStorage.setItem('initial_amount',0)
                            }
                        }
                    }else if(r.message.has_family==0){
                        var html='<p>Sorry! You cannot change your membership since you have family members as per your previous membership.</p>'
                            html+='<p>If you still want to change your membership, you have to delete those members.</p>'
                            html+='<div style="text-align:right;"><button style="margin-right:10px;" class="btn btn-default" onclick="restoreMembership()">Cancel</button><button onclick="removeAllMembers(this)" class="btn btn-primary" data-price="'+membership_info.amount+'" data-id="'+r.message.failed_response+'">Delete & Proceed</button></div>';
                            frappe.msgprint(html,'Confirm')
                    }else{
                        if(active=='1'){
                            if (parseFloat(initial_amt) < parseFloat(membership_info.amount)) {
                                $("input[name=membership_amount]").val(membership_info.amount);
                                localStorage.setItem('donationamount', membership_info.amount);
                            } else {
                                frappe.msgprint('You cannot change your membership type which has less amount than the current type.', 'Alert')
                                $('select[name=membership_type]').val('')
                            }
                        }else{
                            $("input[name=membership_amount]").val(membership_info.amount);
                            localStorage.setItem('donationamount', membership_info.amount);
                            localStorage.setItem('initial_amount',0)
                        }
                    }
                }else{
                    $("input[name=membership_amount]").val(membership_info.amount);
                    localStorage.setItem('donationamount', membership_info.amount);
                    localStorage.setItem('initial_amount',0)
                }
            }
        });
        frappe.call({
            method: "gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_rolecount",
            args: {
                "relation": membership_type
            },
            callback: function(r) {

                if (r.message) {
                    var lenm = r.message.length;
                    var count = $('tr').length;

                    $.each(r.message, function(i, d) {
                        for (var i = 1; i <= d.allowed_members; i++) {

                        }
                    });
                }
            }
        });
    })
    $('input[name="date_of_birth"]').change(function() {
        var data = $('input[name="date_of_birth"]').val();
        var self_rel = $('input[name=self_relation]').val();
        var today = new Date();
        var birthDate = new Date(data);
        var age_str = get_limitage(data);
        frappe.call({
            method: "nonprofit.nonprofit.doctype.member.member.get_relationgroup",
            args: {
                relation: self_rel
            },
            callback: function(r) {
                $('input[name="member_group"]').val(r.message[0][0]);
                var group = $('input[name="member_group"]').val();
                var date_birth = $('input[name="date_of_birth"]').val();
                var ship_type = $('select[name="membership_type"]').val();
                if (group) {
                    var today = new Date();
                    var birthDate = new Date(date_birth);
                    var age_strs = get_limitage(date_birth);
                    $('input[name="ageyears"]').val(age_str);
                    frappe.call({
                        method: "nonprofit.nonprofit.doctype.member.member.get_self_agelimit",
                        args: {
                            "age_limit": age_strs,
                            "relation": group,
                            "parent": ship_type
                        },
                        callback: function(r) {
                            // if (r.message != undefined) {
                            //     if (r.message[0].age_condition == "Minimum") {
                            //         var ages = r.message[0].age_limit;
                            //         var html = '<div>'
                            //         html += '<span style="float:left;margin-right: 10px;;">Member age should be above ' + ages + '</span><br/>'
                            //         html += '</div>'
                            //         frappe.msgprint(html, 'Member')
                            //     } else if (r.message[0].age_condition == "Maximum") {
                            //         var ages = r.message[0].age_limit;
                            //         var html = '<div>'
                            //         html += '<span style="float:left;margin-right: 10px;;">Member age should be below ' + ages + '</span><br/>'
                            //         html += '</div>'
                            //         frappe.msgprint(html, 'Member')
                            //     }
                            // }
                        }
                    })
                }
            }
        });
    });
    var normal_test_items = $('div[data-fieldname = "table_25"]');
    var normal_test_items_add_btn = $('button[data-fieldname = "table_25"]');
    var data = $('input[name="member_name"]').val();
    var membership_type = $('select[name="membership_type"]').val();
    var dateof_birth = $('input[name="date_of_birth"]').val();
    var tables = $('div[name="table_25"]').val();
    var docname = frappe.doc_name;
    if (dateof_birth) {
        var today = new Date();
        var birthDate = new Date(dateof_birth);
    }
    var values = {};
    $('td input').each(function(e) {
        // values[$(this).attr('name')] = $(this).val();
        var ofbirth = $('input[name=date_of_birth]').val();
        // var dat=$('select[name=gender]>option:selected').val();
        var relation = $('select[name=relation] option:selected').text();
        var relationship_group = $('input[name=relationship_group]').val();
        if (ofbirth) {
            var today = new Date();
            var birthDate = new Date(ofbirth);
            var age_str = get_limitage(ofbirth);
            if (membership_type) {
                frappe.call({
                    method: "gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_age_limit",
                    args: {
                        "age_limit": age_str,
                        "relation": relationship_group,
                        "parent": membership_type
                    },
                    callback: function(r) {
                        if (r.message) {
                            // console.log(r.message)
                        } else {

                            // frappe.throw(__("Age limit is exceed!"))
                        }

                    }
                })
            }

        }
    });
    // console.log(docname)
    frappe.call({
        method: "frappe.client.get_value",
        args: {
            'doctype': "Membership",
            'filters': { 'member': docname },
            'fieldname': [
                'to_date'
            ],
            'ignore_permissions':true
        },
        callback: function(data) {
            if (data.message) {
                $('input[name="membership_expiry_date"]').val(data.message.to_date)
            }
        }
    });

    var members_count = 7;
    if (members_count) {

    }
    $('button[data-fieldname=table_25]').click(function() {
        var table_length = $("#table_25 tbody tr").length;
        var id = 'relation-' + table_length;
        $('#table_25 tbody tr:last').attr('id', table_length)
    })
    $('button[data-fieldname=table_25]').click(function() {
        var table_length = $("#table_25 tbody tr").length;
        var id = 'date_of_birth-' + table_length;
        $('#table_25 tbody tr:last').find('td:eq(4)').find("input[name=date_of_birth]").attr('id', id);
        $('#table_25 tbody tr:last').find("input[name=date_of_birth]").attr('onchange', 'getdatevalidation(' + table_length + ')')
        $('#table_25 tbody tr:last').find("input[name=phone_no]").attr('onchange', 'getphonevalidation(' + table_length + ')')
        $('#table_25 tbody tr:last').find("input[name=email]").attr('onchange', 'getemailvalidation(' + table_length + ')')
        $('#table_25 tbody tr:last').find("input[name=relation]").attr('onchange', 'getMemberData(' + table_length + ')')             
    })
    $('#Nsave').click(function() {
        var memtype = $('select[name="membership_type"]').val();
        var typeamount = $('input[name="membership_amount"]').val();
        var amount = localStorage.getItem('donationamount');
        localStorage.setItem("existing_type", memtype);
        localStorage.setItem("new_amount", typeamount);
    })
    $('#Nsub').click(function() {
        var memtype = $('select[name="membership_type"]').val();
        var typeamount = $('input[name="membership_amount"]').val();
        localStorage.setItem("existing_type", memtype);
        localStorage.setItem("new_amount", typeamount);
    })
    var i = 1;
    $('#table_25 tbody tr').each(function() {
        // $(this).find('div[name="relationship_group"]').parent().parent().hide()
        if ($(this).find('input[name="date_of_birth"]').val() != '') {
            $(this).find('input[name="date_of_birth"]').attr('disabled', true)
        } else {
            $(this).find('input[name="date_of_birth"]').removeAttr('disabled')

        }
        if ($(this).find('input[name="gender"]').val() != '') {
            $(this).find('input[name="gender"]').attr('disabled', true)
        } else {
            $(this).find('input[name="gender"]').removeAttr('disabled')

        }
        if ($(this).find('select[name="relation"]').val() != '') {
            $(this).find('select[name="relation"]').attr('disabled', true)
        } else {
            $(this).find('select[name="relation"]').removeAttr('disabled')
        }
        if ($(this).find('select[name=gender]').val() != '') {
            $(this).find('select[name="gender"]').attr('disabled', true)
        } else {
            $(this).find('select[name="gender"]').removeAttr('disabled')
        }
        if ($(this).find('input[name=email]').val() != '') {
            $(this).find('input[name="email"]').attr('disabled', true)
        } else {
            $(this).find('input[name="email"]').removeAttr('disabled')
        }
        if ($(this).attr('data-name') != '') {
            $(this).attr('id', i)
            $(this).find('input[data-fieldname=phone_no]').attr('onchange', 'getphonevalidation("' + i + '")')
            $(this).find('input[data-fieldname=email]').attr('onchange', 'getemailvalidation("' + i + '")')
        }
        i++;
    })
    if($('input[name="recurring_payment"]').val()=='1' && $('input[name="active"]').val()=='1'){
        // $('input[data-label="Make Recurring Payment?"]').parent().hide()
        // $('div[data-label="Recurring Payment"]').hide()
        // localStorage.setItem('recurring_payment','1')
        $('#Nsave').show();
        $('#Nsub').hide();
    }else if($('input[name="recurring_payment"]').val()=='1' && $('input[name="active"]').val()=='0'){
        $('#Nsave').show();
        $('#Nsub').hide();
        localStorage.setItem('recurring_payment','1')
    }else{
        $('input[data-label="Make Recurring Payment?"]').removeAttr('checked')
    }
    // $('input[name="recurring_payment"]').val('1')
    $('input[data-label="Make Recurring Payment?"]').change(function(){
        if($(this).attr('checked')=='checked'){
            $('input[name="recurring_payment"]').val('1')
            localStorage.setItem('recurring_payment','1')
        }else{
            var html='<div>Are you sure to cancel your membership subscription?</div><div \
            style="margin-top:25px;text-align:right;"><button class="btn btn-default" \
            onclick="continue_subscription()" style="margin-right:10px;">Continue Subscription</button><button class="btn btn-primary" \
            onclick="cancel_subscription1()">Cancel Subscription</button></div>';
            frappe.msgprint(html,'Confirm')            
        }
    })
    get_recurring_payment_details()
})

function cancel_subscription1(){
    $('input[name="recurring_payment"]').val('0')
    localStorage.removeItem('recurring_payment')
    $('.modal').modal('hide')
}

function continue_subscription(){
    $('input[data-label="Make Recurring Payment?"]').attr('checked',true)
    $('input[name="recurring_payment"]').val('1')
    $('.modal').modal('hide')
}

function getMemberData(length) {

    var relation = $("#table_25 #" + length + " select[name=relation] option:selected").val();
    frappe.call({
        method: "nonprofit.nonprofit.doctype.member.member.get_relationgroup",
        args: {
            relation: relation
        },
        callback: function(data) {
            $("#table_25 #" + length + " input[name=relationship_group]").val(data.message[0][0])
        }
    });
}

function getdatevalidation(id) {
    var gr = $("#table_25 #" + id + " select[name=relation]").val();
    var data = $("#table_25 #" + id + " input[name=date_of_birth]").val();
    var self_rel = $("#table_25 #" + id + " select[name=relation]").val();
    var today = new Date();
    var birthDate = new Date(data);
    var age_str = get_limitage(data);
    frappe.call({
        method: "nonprofit.nonprofit.doctype.member.member.get_relationgroup",
        args: {
            relation: self_rel
        },
        callback: function(r) {
            $("#table_25 #" + id + " input[name=relationship_group]").val(r.message[0].parent)
            var group = r.message[0].parent;
            var date_birth = $("#table_25 #" + id + "  input[name=date_of_birth]").val();
            var ship_type = $('select[name="membership_type"]').val();
            if (group) {
                var today = new Date();
                var birthDate = new Date(date_birth);
                var age_strs = get_limitage(date_birth);
                frappe.call({
                    method: "nonprofit.nonprofit.doctype.member.member.get_self_agelimit",
                    args: {
                        "age_limit": age_strs,
                        "relation": group,
                        "parent": ship_type
                    },
                    callback: function(r) {
                        // if (r.message[0].age_condition == "Minimum") {
                        //     var ages = r.message[0].age_limit;
                        //     var html = '<div>'
                        //     html += '<span style="float:left;margin-right: 10px;;">Member age should be above ' + ages + '</span><br/>'
                        //     html += '</div>'
                        //     frappe.msgprint(html, 'Member')
                        // } else if (r.message[0].age_condition == "Maximum") {
                        //     var ages = r.message[0].age_limit;
                        //     var html = '<div>'
                        //     html += '<span style="float:left;margin-right: 10px;;">Member age should be below ' + ages + '</span><br/>'
                        //     html += '</div>'
                        //     frappe.msgprint(html, 'Member')
                        // }

                    }
                })
            }
        }
    });
}

function get_membershiptype(types) {

}

function get_limitage(birth) {
    var yourdate = birth.split("-").reverse();
    var tmp = yourdate[2];
    yourdate[2] = yourdate[1];
    yourdate[1] = tmp;
    yourdate = yourdate.join("-");
    var ageMS = Date.parse(Date()) - Date.parse(yourdate);
    var age = new Date(ageMS);
    age.setTime(ageMS);
    var years = age.getFullYear() - 1970;
    return years
};

function get_age_limitage(birth) {
    var yourdate = birth.split("-").reverse();
    var tmp = yourdate[2];
    yourdate[2] = yourdate[1];
    yourdate[1] = tmp;
    yourdate = yourdate.join("-");
    var ageMS = Date.parse(Date()) - Date.parse(yourdate);
    var age = new Date(ageMS);
    age.setTime(ageMS);
    var years = age.getFullYear() - 1970;
    return years
};

function formatDate(date) {
    var year = date.getFullYear().toString();
    var month = (date.getMonth() + 101).toString().substring(1);
    var day = (date.getDate() + 100).toString().substring(1);
    return month + "-" + day + "-" + year;
}

function get_family_validation() {
    var newtype = $('select[name="membership_type"]').val();
    var self_relation = $('input[name=self_relation]').val();
    if (self_relation == 'Self') {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                'doctype': "Membership Type",
                'filters': { 'name': newtype },
                'fieldname': [
                    'has_family', 'count'
                ],
                'ignore_permissions':true
            },
            callback: function(data) {
                if (data.message != undefined) {
                    var row_count = $('#table_25 tbody tr').length;
                    for (var i = 0; i < parseInt(row_count); i++) {
                        // $('tr[id="' + i + '"]').remove();
                    }
                    var t_length = $('#table_25 tbody tr').length - 1;
                    var html = '<div class="info-msg"><p>You can add ' + data.message.count + ' family members for ' + newtype + '</p><p><b>Note:</b> Email & Mobile number are <b>not mandatory</b> for family members. Please <b>do not</b> add primary member`s email or phone number for the family members.</p></div>'
                    $('div[data-label="Family Member Count"]').html(html)
                    $('input[name="has_family"]').val(data.message.has_family);
                    var has_familys = $('input[name="has_family"]').val();
                    if (has_familys == "Yes") {
                        $('#table_25').parent().parent().parent().parent().show();
                        $('.btn-remove').parent().hide();
                        $('#table_25 thead tr td').hide()
                    } else {
                        $('#table_25').parent().parent().parent().parent().hide();
                        $('.btn-remove').parent().hide();
                        $('#table_25 thead tr td').hide()
                    }
                }
            }
        })
    } else {
        $('div[data-label="Family Information"]').hide()
    }
}

function get_self() {
    frappe.call({
        method: "frappe.client.get_value",
        args: {
            'doctype': "Relationship",
            'filters': { 'is_member': "Yes" },
            'fieldname': [
                'name'
            ],
            'ignore_permissions':true
        },
        callback: function(data) {
            if (data.message) {
                $('input[name=self_relation]').val(data.message.name);
            }
        }
    });
}

function changemembership() {
    $('select[name=membership_type]').val('')
    $('select[name=membership_type]').attr('disabled', false)
    $('button.btn-form-submit').show()
    $('button.btn-form-saveonly').hide()
}

function get_user_detail() {
    var user = getCookie('user_id');
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_user',
        args: {
            user: user
        },
        callback: function(data) {
            if (data.message != undefined) {
                $('input[name="member_name"]').val(data.message.first_name)
                $('input[name="email"]').val(data.message.email)
                $('input[name="phone_no"]').val(data.message.mobile_no)
                $('input[name="middle_name"]').val(data.message.middle_name)
                $('input[name="last_name"]').val(data.message.last_name)
            }
        }
    })
}

function get_membership_details() {
    var membership = $('select[name=membership_type] option:selected').val()
    localStorage.setItem('donationamount', $('input[name="membership_amount"]').val());
    frappe.call({
        method: "gscommunity.gscommunity.doctype.general_settings.general_settings.get_validity",
        args: {
            membershiptype: membership
        },
        callback: function(data) {
            if (data.message.membership_type == membership) {
                $('#change-membership').hide()
            }
        }
    });
}

function validate_date() {
    // console.log()
}

function get_newsletter(newsletter) {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_email_group",
        args: {
            category: 'Newsletter'
        },
        callback: function(data) {
            if (data.message) {
                var html = '<option value></option>'
                for (var i = 0; i < data.message.length; i++) {
                    html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>'
                }
                $('select[name="newsletter"][data-doctype="Member"]').html(html)
                $('select[name=newsletter][data-doctype="Member"]').val(newsletter)
                $('div[data-fieldname="table_25"] tbody tr').each(function(){
                    var news=$(this).find('select[name=newsletter]').val()
                    $(this).find('select[name=newsletter]').html(html)
                    $(this).find('select[name=newsletter]').val(news)
                })
            }
        }
    });
}

function get_samaj(samaj) {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_email_group",
        args: {
            category: 'Samaj Darshan'
        },
        callback: function(data) {
            if (data.message) {
                var html = '<option value></option>'
                for (var i = 0; i < data.message.length; i++) {
                    html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>'
                }
                $('select[name="samaj_darshan"]').html(html)
                $('select[name=samaj_darshan]').val(samaj)
            }
        }
    });
}

function getphonevalidation(id) {
    var number = $("#table_25 #" + id + " input[name=phone_no]").val();
    if (!validate_number(number)) {
        frappe.msgprint('Please enter a valid phone number')
        $("#table_25 #" + id + " input[name=phone_no]").val('');
    } else {
        if (number.length != 10) {
            frappe.msgprint('Please enter 10 digit phone number')
            $("#table_25 #" + id + " input[name=phone_no]").val('');
        }
    }
}

function getemailvalidation(id) {
    var email = $("#table_25 #" + id + " input[name=email]").val();
    if (!validate_email(email)) {
        frappe.msgprint('Please enter a valid email id')
        $("#table_25 #" + id + " input[name=email]").val('');
    }
}

function get_membership_types() {
    var type = $('select[name=membership_type] option:selected').val()
    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            'doctype': "Membership Type",
            'filters': { 'published': 1 },
            'fields': [
                'name','amount'
            ]
        },
        callback: function(data) {
            var option = '<option value=""></option>';
            if (data.message) {
                for (var i = 0; i < data.message.length; i++) {
                    option += '<option value="' + data.message[i].name + '" data-price="'+data.message[i].amount+'">' + data.message[i].name + '</option>';
                }
            }            
            $('select[name=membership_type]').html(option);
            $('select[name=membership_type]').val(type)
            var active=$('input[name="active"]').val();
            if(active!="1"){
                var amount=$('option[value="'+type+'"]').attr('data-price')
                $('input[name="membership_amount"]').val(amount)
                localStorage.setItem('donationamount',amount)
                localStorage.setItem('initial_amount',amount)
            }
        }
    })
}
function get_recurring_payment_details(){
    frappe.call({
        method:'gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_recurring_payment_details',
        args:{
            doctype:'Membership Type',
            parent:$('select[name="membership_type"] option:selected').val()
        },
        callback:function(data){
            if(data.message){
                localStorage.setItem('plan_id',data.message[0].plan_id)
            }            
        }
    })
}
function removeMembers(e){
    var types=$(e).attr('data-id');
    var price=$(e).attr('data-price')
    if(types){
        var type=types.split(',');
        $(type).each(function(k,v){
            $('#table_25 tbody tr').each(function(){
                var relation=$(this).find('input[name="relationship_group"]').val();
                if(relation==v){
                    $(this).remove();
                }
            })
        })
    }
    $("input[name=membership_amount]").val(price);
    localStorage.setItem('initial_amount', 0);
    localStorage.setItem('donationamount', price);
    $('.modal').modal('hide')
}
function removeAllMembers(e){
    var types=$(e).attr('data-id');
    var price=$(e).attr('data-price')
    if(types){
        var type=types.split(',');
        $(type).each(function(k,v){
            $('#table_25 tbody tr').each(function(){
                var relation=$(this).find('input[name="relationship_group"]').val();
                if(relation){
                    $(this).remove()
                }
            })
        })
    }
    $("input[name=membership_amount]").val(price);
    localStorage.setItem('donationamount', price);
    localStorage.setItem('initial_amount', 0);
    $('.modal').modal('hide')
}
function restoreMembership(){
    $('select[name=membership_type]').val(localStorage.getItem('existing_type'))
    $('.modal').modal('hide')
}
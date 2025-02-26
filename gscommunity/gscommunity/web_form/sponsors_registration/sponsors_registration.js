frappe.ready(function() {
    var docname = frappe.doc_name;
    var url = ''
    var type = ''
    var amount = ''
    var plan = ''
    var newfile = ''
    var Route = window.location.href;
    var image = ''
    var change_in_yp=0
    if (Route.includes('?')) {
        url = Route.split('?')[1];
        type = url.split('&')[1];
        amount = url.split('&')[3];
        plan = url.split('&')[2];
        newfile = url.split('&')[0];
    }
    $('.btn-form-saveonly').hide()
    var date = new Date();
    var month = (date.getMonth() + 1)
    var day = date.getDate()
    var year = date.getFullYear()
    var dateformat = year + '-' + month + '-' + day
    $('input[name=starts_on]').val(dateformat)
    $('div[data-label="Edit YP"]').attr('class', 'info-text')
    $('select[data-label="Category"]').parent().parent().attr('id', 'top-margin')
    $('#top-margin').css('margin-top','82px')
    check_current_user();
    $('div[data-label="Member Info"]').parent().parent().parent().hide();
    if (type != '' && type != undefined) {
        type = type.split('=')[1].replace(/%20/g, ' ');
        $('input[name=sponsorship_type]').val(type)
        get_sponsorship_plan(type, plan)
    }
    if (amount != '' && amount != undefined) {
        var totalamount = amount.split('=')[1].replace(/%20/g, ' ');
        $("input[name=amount]").val(totalamount);
        localStorage.setItem('donationamount', totalamount);
    }
    $('select[name=sponsorship_plan]').change(function(e) {
        var Sponsorshiptype = $('select[name=sponsorship_plan]').val();
        e.preventDefault();
        frappe.call({
            method: "gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_plan_amount",
            args: {
                "sptype": Sponsorshiptype
            },
            callback: function(r) {
                $("input[name=amount]").val(r.message[0].item_amount);
                localStorage.setItem('donationamount', r.message[0].amount);
                $('input[name="validity"]').val(r.message[0].validity)
                $('input[name=accounting_head]').val(r.message[0].accounting_head)
                get_end_date()
                get_feature();
            }
        });
    })
    $('select[name=sponsor_type]').on('change', function() {
        var sponsor_type = $('select[name=sponsor_type]').val()
        if (sponsor_type == 'Member') {
            var html = '<p> Enter your email id or mobile number to verify your member details.</p>';
            $('div[data-label="Member Credentials"]').html(html)
        } else {
            $('div[data-label="Membership Info"]').hide()
            $('input[name="sponsor_name"]').val('')
            $('input[name="last_name"]').val('')
            $('input[name="phone"]').val('')
            $('input[name="email"]').val('')
            $('select[name="member"]').val('')
            $('div[data-label="Member Credentials"]').html('')
            $('input[name="sponsor_name"]').removeAttr('disabled')
            $('input[name="last_name"]').removeAttr('disabled')
            $('input[name="phone"]').removeAttr('disabled')
            $('input[name="email"]').removeAttr('disabled')
        }
    })
    $('input[name="phone"]').on('change', function() {
        var phone = $('input[name="phone"]').val();
        var email = $('input[name="email"]').val();
        var sponsor_type = $('select[name=sponsor_type] option:selected').val();
        if (phone != '') {
            if (!validate_number(phone)) {
                frappe.msgprint('Please enter 10 digit phone number', 'Alert')
                $('input[name=phone]').val('');
            }
            if (phone.length != 10) {
                frappe.msgprint('Please enter 10 digit phone number', 'Alert')
                $('input[name=phone]').val('');
            }
        }
        if (phone != '' && sponsor_type == 'Member') {
            get_member_info(phone, email);
        }        
    })
    $('input[name="email"]').on('change', function() {
        var phone = $('input[name="phone"]').val();
        var email = $('input[name="email"]').val();
        if (email != '') {
            if (!validate_email(email)) {
                frappe.msgprint('Please enter a valid email id', 'Alert')
                $('input[name=email]').val('');
            }
        }
        var sponsor_type = $('select[name=sponsor_type] option:selected').val();
        if (email != '' && sponsor_type == 'Member') {
            get_member_info(phone, email);
        }
        if (email != '' && sponsor_type != 'Member') {
            check_guest_details(email)
            check_guest_login(email)
        }
    })
    $('input[data-label="Business Name"]').change(function() {
        change_in_yp=1;
        var name = $('input[data-label="Business Name"]').val();              
    })
    $('#Nsave').click(function(e) {
        add_yellowpage(newfile, image);
    })
    $('#Nsub').click(function() {
        add_yellowpage(newfile, image);
    })
    $('.info-text').css('z-index','999')
    $('.info-text').css('position','relative')
    $('input[data-label="Business Name"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('select[data-label="Category"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="Address Line 1"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="City"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="State"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="Zip Code"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="Email Id"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="Phone No"]').parent().find('label').append(' <span class="reqd_field">*</span>')
    $('input[data-label="Zip Code"]').attr('maxlength', 5);
    $('input[name="phone"]').attr('maxlength', 10);
    $('input[data-label="Phone No"]').attr('maxlength', 10);
    $('input[data-label="Would you like to add yellow page now or add later?"]').on('change', function() {
        var checked = $('input[data-label="Would you like to add yellow page now or add later?"]:checked').val();
        if (checked == 'on') {
            $('input[data-label="Business Name"]').attr('data-reqd', '1');            
            $('select[data-label="Category"]').attr('data-reqd', '1');            
            $('input[data-label="Address Line 1"]').attr('data-reqd', '1');            
            $('input[data-label="City"]').attr('data-reqd', '1');            
            $('input[data-label="State"]').attr('data-reqd', '1');            
            $('input[data-label="Zip Code"]').attr('data-reqd', '1');            
            $('input[data-label="Email Id"]').attr('data-reqd', '1');            
            $('input[data-label="Phone No"]').attr('data-reqd', '1');            
            $('select[data-label="Business Type"]').parent().hide();
            $('input[data-label="Email Id"]').parent().show()
            $('input[data-label="Phone No"]').parent().show()
            $('input[data-label="Address Line 1"]').parent().show()
            $('input[data-label="City"]').parent().show()
            $('input[data-label="Zip Code"]').parent().show()
            $('input[data-label="Business Name"]').parent().show()
            $('select[data-label="Category"]').parent().parent().show();
            $('div[data-label="Yellow page Info"]').hide()
            $('div[data-label="Edit YP"]').show()
            var user = getCookie('user_id');
            var html = '<div class="col-sm-12">'
            html += '<div class="form-group" id="image">'
            if (user == 'Guest') {
                html += '<p class="info-msg">You will be provided with a basic login details through your mail. You can edit your yellowpage in My Account page.'
            } else {
                html += '<p class="info-msg">You can edit your yellowpage in My Account page.'
            }
            html += ' <br><a href="/yellow-page-terms-and-conditions" target="_blank">* Terms & Conditions apply</a></p></div></div>'
            $('div[data-label="Edit YP"]').html(html)
        } else {
            $('input[data-label="Business Name"]').removeAttr('data-reqd');
            $('select[data-label="Category"]').removeAttr('data-reqd');
            $('input[data-label="Address Line 1"]').removeAttr('data-reqd');
            $('input[data-label="City"]').removeAttr('data-reqd');
            $('input[data-label="State"]').removeAttr('data-reqd');
            $('input[data-label="Zip Code"]').removeAttr('data-reqd');
            $('input[data-label="Email Id"]').removeAttr('data-reqd');
            $('input[data-label="Phone No"]').removeAttr('data-reqd');
            $('select[data-label="Business Type"]').parent().hide();
            $('select[data-label="Business Type"]').parent().hide();
            $('input[data-label="Email Id"]').parent().hide()
            $('input[data-label="Phone No"]').parent().hide()
            $('input[data-label="Address Line 1"]').parent().hide()
            $('input[data-label="City"]').parent().hide()
            $('input[data-label="Zip Code"]').parent().hide()
            $('input[data-label="Business Name"]').parent().hide()
            $('select[data-label="Category"]').parent().parent().hide();
            $('#image').hide();
            $('div[data-label="Yellow page Info"]').show()
        }
    })
    $('input[name="phone"]').keydown(function(e) {
        KeyDown(e);
    });
    $('input[data-label="Phone No"]').keydown(function(e) {
        KeyDown(e);
    });
    $('input[data-label="Phone No"]').change(function(e) {
        var phone = $('input[data-label="Phone No"]').val();
        if (phone.length != 10) {
            frappe.msgprint('Please enter 10 digit phone number', 'Alert')
            $('input[data-label="Phone No"]').val('');
        }
    });
    $('input[data-label="Fax"]').keydown(function(e) {
        KeyDown(e);
    });
    $('input[data-label="Zip Code"]').keydown(function(e) {
        KeyDown(e);
    });
    $('input[data-label="Zip Code"]').change(function(e) {
        var zip = $('input[data-label="Zip Code"]').val();
        if (zip.length != 5) {
            frappe.msgprint('Please enter 5 digit zip code', 'Alert')
            $('input[data-label="Zip Code"]').val('');
        }
    });
    $('input[data-label="Email Id"]').change(function() {
        var email = $('input[data-label="Email Id"]').val();
        if (email != '') {
            if (!validate_email(email)) {
                frappe.msgprint('Please enter a valid email id', 'Alert')
                $('input[data-label="Email Id"]').val('');
            }
        }
    })
    $('input[data-label="State"]').change(function() {
        var state = $('input[data-label="State"]').val();
        if (state != '') {
            if (!validate_state(state)) {
                frappe.msgprint('Please enter 2 digit alpha characters for state name', 'Alert')
                $('input[data-label="State"]').val('');
            }
            if (state.length != 2) {
                frappe.msgprint('Please enter 2 digit alpha characters for state name', 'Alert')
                $('input[data-label="State"]').val('');
            }
        }
    })
    $('select[data-label="Category"]').change(function() {
        var category = $('select[data-label="Category"] option:selected').val()
        if (category != '') {
            frappe.call({
                method: 'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_subcategory',
                args: {
                    category: category
                },
                callback: function(data) {
                    var html = '<option value selected="selected"></option>'
                    if (data.message != undefined) {
                        for (var i = 0; i < data.message.length; i++) {
                            html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>'
                        }
                        $('select[data-label="Sub Category"]').html(html)
                    } else {
                        $('select[data-label="Sub Category"]').html(html)
                    }
                }
            })
        }
    })
    $('input[data-label="Make Recurring Payment?"]').change(function(){
        if($(this).attr('checked')=='checked'){
            localStorage.setItem('recurring_payment','1')
        }else{
            localStorage.removeItem('recurring_payment')
        }
    })
    get_recurring_payment_details(plan)
})

function get_sponsorship_plan(type, plan) {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_sponsor_plan",
        args: {
            stype: type
        },
        callback: function(data) {
            console.log(data.message)
            var html = '';
            plan = plan.split('=')[1].replace(/%20/g, ' ')
            for (var i = 0; i < data.message.length; i++) {
                html += '<option value="' + data.message[i].name + '">' + data.message[i].item_name + '</option>';
                if (plan.trim() == data.message[i].name) {
                    $('input[name="validity"]').val(data.message[i].validity)
                    $('input[name=accounting_head]').val(data.message[i].accounting_head)
                }
            }
            $('select[name=sponsorship_plan]').html(html)
            $('select[name=sponsorship_plan]').val(plan.trim())
            get_end_date()
            get_feature();
        }
    });
}

function get_member_info(phone, email) {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_member_info",
        args: {
            phone: phone,
            email: email
        },
        callback: function(data) {
            if (data.message != '0') {
                var html = '<table style="width:75%" class="table table-bordered"><thead style="background:#f1f1f1"><tr><th style="padding:10px;">Member</th><th style="padding:10px;">Name</th><th style="padding:10px;">Status</th></thead>';
                html += '<tbody><tr><td style="padding:15px;">' + data.message.name + '</td><td>' + data.message.member_name + '</td><td>';
                if (data.message.active == 1) {
                    html += 'Active'
                } else {
                    html += 'In Active'
                }
                html += '</td></tr></tbody></table>';
                $('div[data-label="Member Info"]').html(html)
                $('div[data-label="Member Info"]').parent().parent().parent().show();
                $('select[name="member"]').val(data.message.name)
                $('input[name=sponsor_name]').val(data.message.member_name)
                $('input[name=last_name]').val(data.message.last_name)
                if (phone == '') {
                    phone = data.message.phone_no
                    $('input[name="phone"]').val(phone)
                }
                if (email == '') {
                    email = data.message.email
                    $('input[name="email"]').val(email)
                }
                $('input[name=sponsor_name]').attr('disabled',true)
                $('input[name=last_name]').attr('disabled',true)
                if(data.message.email)
                    $('input[name=email]').attr('disabled',true)
                if(data.message.phone_no)
                    $('input[name=phone]').attr('disabled',true)
                get_yellopage_details(email)
                get_end_date()
            } else {
                frappe.msgprint('Invalid Member details', 'Alert')
                $('input[name="phone"]').val('');
                $('input[name="email"]').val('');
            }
        }
    });
}

function check_current_user() {
    var member = getCookie('member_id');
    var user = getCookie('user_id');
    if (member != '') {
        $('select[name="member"]').val(member)
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.participant_form.participant_form.check_user',
            args: {
                member: member
            },
            callback: function(data) {
                $('input[name=sponsor_name]').val(data.message.member_name)
                $('input[name=last_name]').val(data.message.last_name)
                $('select[name=sponsor_type]').val('Member')
                $('input[name=email]').val(data.message.email)
                $('input[name=phone]').val(data.message.phone_no)
                $('select[name=sponsor_type]').parent().hide()
                $('select[name="member"]').prop('disabled', true)
                if (data.message.email != '')
                    $('input[name=email]').prop('disabled', true)
                if (data.message.phone_no != '')
                    $('input[name=phone]').prop('disabled', true)
                if (data.message.last_name != '')
                    $('input[name=last_name]').prop('disabled', true)
                $('input[name=sponsor_name]').prop('disabled', true)
                get_yellopage_details(data.message.email)
            }
        })
    } else if (user != 'Guest') {
        check_guest_login(user)
    } else {
        $('select[name="member"]').parent().hide();
    }
}

function add_yellowpage(newfile, image) {
    var business_name = $('input[data-label="Business Name"]').val();
    var business_type = $('select[data-label="Business Type"] option:selected').val();
    var category = $('select[data-label="Category"] option:selected').val();
    var sub_category = $('select[data-label="Sub Category"] option:selected').val();
    var addr_1 = $('input[data-label="Address Line 1"]').val();
    var addr_2 = $('input[data-label="Address Line 2"]').val();
    var city = $('input[data-label="City"]').val();
    var state = $('input[data-label="State"]').val();
    var zip = $('input[data-label="Zip Code"]').val();
    var owner = $('input[name="sponsor_name"]').val();
    var email = $('input[data-label="Email Id"]').val();
    var phone = $('input[data-label="Phone No"]').val();
    var fax = $('input[data-label="Fax"]').val();
    var name = $('input[data-label="Yellow Page Name"]').val();
    if (business_name != '' && category != '' && addr_1 != '' && city != '' && state != '' && zip != '' && owner != '' && email != '' && phone != '') {
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.add_new_yellowpage',
            args: {
                b_name: business_name,
                b_type: business_type,
                category: category,
                sub_category: sub_category,
                addr_1: addr_1,
                addr_2: addr_2,
                city: city,
                state: state,
                zip: zip,
                owner_name: owner,
                email: email,
                phone: phone,
                fax: fax,
                name: name
            },
            callback: function(data) {
                $('input[data-label="Image"]').click();
            }
        })
    } else {
        return false;
    }
}

function get_feature() {
    var plan = $('select[name="sponsorship_plan"] option:selected').val();
    if (plan != '' && plan != undefined) {
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_sponsor_feature',
            args: {
                plan: plan
            },
            callback: function(data) {
                console.log(data.message[0].enable_yellowpage)
                if (data.message[0].enable_yellowpage == 1) {
                    $('select[data-label="Business Type"]').parent().hide();
                    $('input[data-label="Email Id"]').parent().hide()
                    $('input[data-label="Phone No"]').parent().hide()
                    $('input[data-label="Address Line 1"]').parent().hide()
                    $('input[data-label="City"]').parent().hide()
                    $('input[data-label="Zip Code"]').parent().hide()
                    $('input[data-label="Website Url"]').parent().hide()
                    $('input[data-label="Business Name"]').parent().hide()
                    $('select[data-label="Category"]').parent().parent().hide();
                    $('div[data-label="Edit YP"]').hide()
                    var html = '<div id="free_yp_message"><p>You can add an yellow page for the selected sponsorship type.</p></div>';
                    $('div[data-label="Yellow page Info"]').html(html)
                } else {
                    $('select[data-label="Business Type"]').parent().hide();
                    $('input[data-label="Business Name"]').parent().parent().parent().parent().hide()
                }
            }
        })
    }
}

function get_yellopage_details(email) {
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_yellowpage',
        args: {
            email: email
        },
        callback: function(data) {
            console.log(data.message)
            if (data.message != undefined) {
                $('input[data-label="Business Name"]').val(data.message[0].business_name)
                $('select[data-label="Business Type"]').val(data.message[0].business_type)
                $('select[data-label="Category"]').val(data.message[0].category)
                $('select[data-label="Sub Category"]').val(data.message[0].subcategory)
                $('input[data-label="Email Id"]').val(data.message[0].email)
                $('input[data-label="Phone No"]').val(data.message[0].phone)
                $('input[data-label="Fax"]').val(data.message[0].fax)
                $('input[data-label="Address Line 1"]').val(data.message[0].address)
                $('input[data-label="Address Line 2"]').val(data.message[0].address_line_2)
                $('input[data-label="City"]').val(data.message[0].city)
                $('input[data-label="State"]').val(data.message[0].state)
                $('input[data-label="Zip Code"]').val(data.message[0].zip_code)
                $('input[data-label="Website Url"]').val(data.message[0].website_url)
                $('input[data-label="Yellow Page Name"]').val(data.message[0].name)
                $('textarea[data-label="Description"]').val(data.message[0].description)
            }
        }
    })
}

function KeyDown(e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || e.keyCode == 13 || e.keyCode == 10 || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
}

function get_end_date(validity, starts_on) {
    console.log($('select[name=sponsorship_plan] option:selected').val())
    frappe.call({
        method: 'gscommunity.gscommunity.doctype.sponsorship.sponsorship.get_expiry_date',
        args: {
            "sponsorship_type": $('input[name="sponsorship_type"]').val(),
            "sponsorship_plan": $('select[name=sponsorship_plan] option:selected').val(),
            "member": $('select[name="member"] option:selected').val()
        },
        callback: function(data) {
            if (data) {
                console.log(data.message)
                $('input[name=expires_on]').val(data.message)
            }
        }
    })
}

function check_guest_details(email) {
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.check_guest_details',
        args: {
            email: email
        },
        callback: function(data) {
            console.log(data.message)
            if (data.message != undefined) {
                if (confirm('Your email is already linked with member. Would you like to proceed with sponsor type as member?')) {
                    $('select[name="sponsor_type"]').val('Member')                    
                    get_member_info($('input[name=phone]').val(), email);
                } else {
                    $('input[name=email]').val('')
                }
            }
        }
    })
}

function check_guest_login(user) {
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_user',
        args: {
            user: user
        },
        callback: function(data) {
            var name = data.message.first_name
            $('input[name=sponsor_name]').val(name)
            $('input[name=last_name]').val(data.message.last_name)
            $('select[name=sponsor_type]').val('Guest')
            $('input[name=email]').val(data.message.email)
            $('input[name=phone]').val(data.message.mobile_no)
            $('select[name=sponsor_type]').parent().hide()
            $('select[name="member"]').parent().hide()
            if (data.message.email != '')
                $('input[name=email]').prop('disabled', true)
            if (data.message.mobile_no != '')
                $('input[name=phone]').prop('disabled', true)
            if (data.message.last_name != '')
                $('input[name=last_name]').prop('disabled', true)
            $('input[name=sponsor_name]').prop('disabled', true)
            get_yellopage_details(data.message.email)
        }
    })
}
function get_recurring_payment_details(plan){
    frappe.call({
        method:'gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_recurring_payment_details',
        args:{
            doctype:'Sponsorship Items',
            parent:plan.split('=')[1]
        },
        callback:function(data){
            if(data.message){
                localStorage.setItem('plan_id',data.message[0].plan_id)
            }            
        }
    })
}
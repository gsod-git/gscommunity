frappe.ready(function() {
    check_current_user();
    $('input[name=email]').attr('type', 'email')
    $('input[name=donation_amount]').change(function() {
        console.log($('input[name=donation_amount]').val())
        localStorage.setItem('donationamount', $('input[name=donation_amount]').val());
    })
    $('#Nsave').hide();
    var email;
    var phone;
    $('input[name=donate_as_guest]').change(function() {
        var value = $('input[name=donate_as_guest]:checked').val();        
        if (value == 'on') {
            $('input[name="member"]').parent().hide()
            $('input[name="member_name"]').parent().hide()
            $('input[name=full_name]').parent().show();
            $('input[name=last_name]').parent().show();
            $('input[name=address]').parent().show();
            $('input[name=zip_code]').parent().show();
            $('input[name=email]').parent().parent().show();
            $('input[name=full_name]').attr('data-reqd', '1')
            $('input[name=full_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=last_name]').attr('data-reqd', '1')
            $('input[name=last_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=address]').attr('data-reqd', '1')
            $('input[name=address]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=zip_code]').attr('data-reqd', '1')
            $('input[name=zip_code]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=member]').removeAttr('data-reqd')
            $('input[name=member_name]').removeAttr('data-reqd')
            $('input[name=member_name]').parent().find('label').find('span').remove()
            $('input[name=member]').parent().find('label').find('span').remove()
            $('input[name=email]').prop('readonly', false)
            $('input[name=phone]').prop('readonly', false)
            email=$('input[name=email]').val()
            phone=$('input[name=phone]').val()
            $('input[name=email]').val('')
            $('input[name=phone]').val('')            
        } else {
            $('input[name="member"]').parent().show()
            $('input[name="member_name"]').parent().show()
            $('input[name=full_name]').parent().hide();
            $('input[name=last_name]').parent().hide();
            $('input[name=address]').parent().hide();
            $('input[name=zip_code]').parent().hide();
            $('input[name=email]').parent().parent().show();
            $('input[name=full_name]').removeAttr('data-reqd')
            $('input[name=full_name]').parent().find('label').find('span').remove()
            $('input[name=last_name]').removeAttr('data-reqd')
            $('input[name=last_name]').parent().find('label').find('span').remove()
            $('input[name=address]').removeAttr('data-reqd')
            $('input[name=address]').parent().find('label').find('span').remove()
            $('input[name=zip_code]').removeAttr('data-reqd')
            $('input[name=zip_code]').parent().find('label').find('span').remove()
            $('input[name=member]').attr('data-reqd', '1')
            $('input[name=member]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=member_name]').attr('data-reqd', '1')
            $('input[name=member_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
            $('input[name=email]').val(email)
            $('input[name=phone]').val(phone)
            $('input[name=email]').removeAttr('readonly')
            $('input[name=phone]').removeAttr('readonly')
        }        
    })
    $('input[name=donation_amount]').keydown(function(e) {
        Keydown(e)
    })
    $('input[name=phone]').keydown(function(e) {
        Keydown(e)
    })
    $('input[name=zip_code]').keydown(function(e) {
        Keydown(e)
    })
    $('input[name=phone]').change(function(e) {
        var phone=$('input[name=phone]').val()
        if(phone.length!=10){
            alert('Please enter 10 digit phone number')
            $('input[name=phone]').val('')
        }
    })
    $('input[name=zip_code]').change(function(e) {
        var zip=$('input[name=zip_code]').val()
        if(zip.length!=5){
            alert('Please enter 5 digit zip code')
            $('input[name=zip_code]').val('')
        }
    })
    $('input[name=member]').change(function(){
        var member=$('input[name=member]').val();
        frappe.call({
            method:'gscommunity.gscommunity.web_form.participant_form.participant_form.check_user',
            args:{
                member:member
            },
            callback:function(data){
                $('input[name=member_name]').val(data.message.member_name)
                $('input[name=member_name]').prop('readonly', true)
                $('input[name=email]').val(data.message.email)
                $('input[name=phone]').val(data.message.phone_no)
                $('input[name=email]').prop('readonly', true)
                $('input[name=phone]').prop('readonly', true)
            }
        })
    })
    $('select[name=donation_for]').change(function(){
        var category=$('select[name=donation_for] option:selected').val()
        if(category!=''){
            get_recurring_payment_details()
            frappe.call({
                method:'gscommunity.gscommunity.web_form.donation.donation.get_account_head',
                args:{
                    category:category
                },
                callback:function(data){
                    console.log(data.message)
                    $('input[name=accounting_head]').val(data.message.accounting_head)
                }
            })
        }else{
            $('select[data-label="Payment Options"]').html('<option></option>')
        }
    })
    $('input[name=email]').change(function(){        
        var e_mail=$('input[name=email]').val();
        if(e_mail!=''){                       
            if(!validate_email(e_mail)){
                alert('Please enter a valid email id')
                $('input[name=email]').val('');
            }
        }            
    })
    $('select[data-label="Payment Options"]').parent().hide();
    $('input[data-label="Make Recurring Payment?"]').change(function(){
        if($(this).attr('checked')=='checked'){
            localStorage.setItem('recurring_payment','1')
            $('select[data-label="Payment Options"]').parent().show();
            $('input[name="donation_amount"]').attr('disabled',true)
        }else{
            localStorage.removeItem('recurring_payment')
            $('select[data-label="Payment Options"]').parent().hide();
            $('input[name="donation_amount"]').removeAttr('disabled')
        }
    })
    $('select[data-label="Payment Options"]').change(function(){
        localStorage.setItem('plan_id',$(this).val())
        var text=$('select[data-label="Payment Options"] option:selected').text()
        var price=text.split('-')[1].split('$')[1];
        $('input[name="donation_amount"]').val(price)
        localStorage.setItem('donationamount',price)
    }) 
})

function check_current_user() {
    var member = getCookie('member_id');
    var user = getCookie('user_id');
    if (member != '') {
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.participant_form.participant_form.check_user',
            args: {
                member: member
            },
            callback: function(data) {
                $('input[name=member_name]').val(data.message.member_name)
                $('input[name=member]').val(data.message.name)
                $('input[name=email]').val(data.message.email)
                $('input[name=phone]').val(data.message.phone_no)
                $('select[name=sponsor_type]').parent().hide()
                $('input[name="member"]').prop('readonly', true)
                $('input[name=member]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                $('input[name=member_name]').prop('readonly', true)
                $('input[name=member_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                $('input[name="email"]').prop('readonly', true)
                $('input[name=phone]').prop('readonly', true)
                $('input[name=full_name]').parent().hide();
                $('input[name=last_name]').parent().hide();
                $('input[name=address]').parent().hide();
                $('input[name=zip_code]').parent().hide();
                $('input[name="donate_as_guest"]').parent().hide()
            }
        })
    } else if (user != 'Guest') {
        frappe.call({
            method: 'gscommunity.gscommunity.web_form.sponsors_registration.sponsors_registration.get_user',
            args: {
                user: user
            },
            callback: function(data) {
                var name = data.message.first_name
                $('input[name=full_name]').val(name)
                $('input[name=email]').val(data.message.email)
                $('input[name=phone]').val(data.message.phone)
                $('input[name=last_name]').val(data.message.last_name)
                $('input[name="member"]').parent().hide()
                $('input[name="member_name"]').parent().hide()
                $('input[name=email]').prop('readonly', true)
                if(data.message.phone)
                    $('input[name=phone]').prop('readonly', true)
                $('input[name=full_name]').prop('readonly', true)
                $('input[name=full_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                $('input[name="donate_as_guest"]').prop('checked', true)
                $('input[name="donate_as_guest"]').parent().hide()
                $('input[name=last_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                $('input[name=address]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                $('input[name=zip_code]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                if(data.message.last_name){
                    $('input[name=last_name]').prop('readonly',true)
                }
            }
        })
    } else {
        $('input[name=full_name]').parent().hide();
        $('input[name=last_name]').parent().hide();
        $('input[name=address]').parent().hide();
        $('input[name=zip_code]').parent().hide();
        $('input[name=member]').attr('data-reqd', '1')
        $('input[name=member]').parent().find('label').append(' <span class="reqd_field">*</span>') 
        $('input[name=member_name]').attr('data-reqd', '1')
        $('input[name=member_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
    }
}

function Keydown(e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
}
function get_recurring_payment_details(){
    frappe.call({
        method:'gscommunity.gscommunity.web_form.membership_registration.membership_registration.get_recurring_payment_details',
        args:{
            doctype:'Donation Category',
            parent:$('select[name="donation_for"] option:selected').val()
        },
        callback:function(data){
            if(data.message){
                // var html='<div><div style="font-weight:600;font-size:15px;padding:10px;">Please select any one of the available recurring payment options.</div><div style="padding:10px 25px;">'
                var html='<option></option>'
                $(data.message).each(function(k,v){
                    // html+='<label><input type="radio" name="recurring_payment_option" value="'+v.plan_id+'" /> '+v.plan_name+' - $'+v.price+' - For every '+v.billing_frequency
                    // if(v.billing_frequency=='1')
                    //     html+=' month</label><br>'
                    // else
                    //     html+=' months</label><br>'
                    html+='<option value="'+v.plan_id+'">'+v.plan_name+' - $'+v.price+' - For every '+v.billing_frequency+' month(s)</option>'
                })
                // html+='</div></div>'
                $('select[data-label="Payment Options"]').html(html)
            } else{
                $('select[data-label="Payment Options"]').html('<option></option>')
            }           
        }
    })
}
frappe.ready(function() {
	var pathname = window.location.href;
	var url=''
	if (pathname.includes('?')) {
        url = pathname.split('?')[1];
    }
    // if(url.trim()=='new=1'){
    // 	$('input[name="image"]').parent().parent().hide()
    // 	var html='<p>Please save the form to upload image.</p>'
    // 	$('div[data-label="Image Html"]').html(html)
    // }
    var html='<div class="col-md-12"><div class="form-group" id="image"><p class="info-msg"><a href="/yellow-page-terms-and-conditions" target="_blank">* Terms & Conditions apply</a></p></div></div>'
    // $('div[data-label="Image Html"]').html(html)
    // $('#image').css('width','200%')
    $('#docname').parent().append(html)
    var sp_type=localStorage.getItem("sponsor_type");
    var s_type=$('input[name=business_type]').val()
    if(url.trim()=='new=1'){
        if(sp_type=='Sponsor'){
            $('input[name="business_type"]').val(sp_type)
            get_sponsor(url);
        }else{
            $('input[name="business_type"]').val('Member')
        }
    }else{
        if(!s_type){
            $('input[name="business_type"]').val('Member')
        }
    }
        
    $('.btn-form-submit').hide()
    var sponsor=$('input[name="sponsor"]').val()
	get_current_user(url);
    get_yp_feature(url,sponsor)
	$('select[name="business_type"]').val('Member')
	$('select[name="business_type"]').parent().hide()
	$('input[name="email"]').change(function(){
		var e_mail=$('input[name=email]').val();
        if(e_mail!=''){                       
            if(!validate_email(e_mail)){
                frappe.msgprint('Please enter a valid email id','Alert')
                $('input[name=email]').val('');
            }
        }
	})
    $('input[name="state"]').change(function(){
        var state=$('input[name=state]').val();
        if(state!=''){                       
            if(!validate_state(state)){
                frappe.msgprint('Please enter 2 alpha characters for state name','Alert')
                $('input[name=state]').val('');
            }
            if(state.length!=2){
                frappe.msgprint('State must be 2 alpha characters length','Alert')
                $('input[name=state]').val('');
            }
        }
    })
	$('input[name=phone]').keydown(function(e) {
        Keydown(e)
    })
    $('input[name=phone]').change(function(e) {
        var phone=$('input[name=phone]').val()
        if(phone.length!=10){
            frappe.msgprint('Please enter 10 digit phone number','Alert')
            $('input[name=phone]').val('')
        }
    })
    $('input[name=zip_code]').keydown(function(e) {
        Keydown(e)
    })
    $('input[name=zip_code]').change(function(e) {
        var zip=$('input[name=zip_code]').val()
        if(zip.length!=5){
            frappe.msgprint('Please enter 5 digit zip code','Alert')
            $('input[name=zip_code]').val('')
        }
    })
	// $('input[name="image"]').change(function(e){
	// 	var file = e.currentTarget.files[0];
 //        var $input = $(this);
 //        var input = $input.get(0);
 //        if (input.files.length) {
 //            input.filedata = { "files_data": [] };
 //            window.file_reading = true;
 //            var dataurl = '';
 //            $.each(input.files, function(key, value) {
 //                var name = value.name;
 //                var reader = new FileReader();
 //                var docname = $('#docname').val()
 //                console.log(docname)
 //                reader.onload = function(e) {
 //                    dataurl = reader.result;
 //                    console.log(input.files[0].name)
 //                    console.log(dataurl)
 //                    frappe.call({
 //                        method: "uploadfile",
 //                        args: {
 //                            from_form: 1,
 //                            doctype: 'Yellow Pages',
 //                            docname: docname,
 //                            is_private: 0,
 //                            filename: input.files[0].name,
 //                            file_url: '',
 //                            filedata: dataurl,
 //                            file_size: input.files[0].size,
 //                            docfield: 'image'
 //                        },
 //                        callback: function(data) {
 //                            console.log(data)                            
 //                            frappe.call({
 //                                method: "gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.save_image",
 //                                args: {
 //                                    doctype: 'Yellow Pages',
 //                                    docname: docname,
 //                                    docfield: 'image',
 //                                    file_url:data.message.file_url                                    
 //                                },
 //                                callback: function(data) {
 //                                    $input.wrap('<form>').closest('form').get(0).reset();
 //                                    $input.unwrap();
 //                                    frappe.msgprint('Your file uploaded successfully')
 //                                }
 //                            });
 //                        }
 //                    })
 //                }
 //                reader.readAsDataURL(file);
 //            });
 //            window.file_reading = false;
 //        }
	// })
    $('select[name="category"]').change(function(){
        var category=$('select[name="category"] option:selected').val()
        if(category!=''){
            frappe.call({
                method:'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_subcategory',
                args:{
                    category:category
                },
                callback:function(data){
                    var html='<option value selected="selected"></option>'
                    if(data.message!=undefined){                        
                        for(var i=0;i<data.message.length;i++){
                            html+='<option value="'+data.message[i].name+'">'+data.message[i].name+'</option>'
                        }                        
                    }
                    $('select[name="subcategory"]').html(html)
                }
            })
        }
    })
})
function get_current_user(url){
	var user=getCookie('user_id')
	if(url.trim()=='new=1'){
		$('input[name="user"]').val(user)
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
function get_yp_feature(url,sponsor){
    var user=getCookie('user_id');
    if(url!='new=1'){
        frappe.call({
            method:'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_yp_feature',
            args:{
                sponsor:sponsor
            },
            callback:function(data){
                var section=[]
                $('.table_design').each(function(){
                    section.push($(this).attr('data-label'))
                })
                if(data.message!=undefined){
                    for(var i=0;i<data.message.length;i++){
                        if(data.message[i].enable==0){
                            $('div[data-label="'+data.message[i].label+'"]').hide()
                        }
                    }
                }
            }
        })
    }else{
        frappe.call({
            method:'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_free_yp',
            args:{
                user:user,
                member:getCookie('member_id')
            },
            callback:function(data){
                if(data.message!=undefined){
                    for(var i=0;i<data.message.length;i++){
                        if(data.message[i].enable==0){
                            $('div[data-label="'+data.message[i].label+'"]').hide();
                        }
                    }
                }
            }
        })
    }
}
function get_sponsor(url){
    frappe.call({
        method:'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_sponsor',
        args:{

        },
        callback:function(data){
            $('input[name=business_type]').val('Sponsor')
            $('input[name=sponsor]').val(data.message.name)
            frappe.call({
            method:'gscommunity.gscommunity.web_form.new_yellowpage.new_yellowpage.get_yp_feature',
            args:{
                sponsor:data.message.name
            },
            callback:function(data){
                var section=[]
                $('.table_design').each(function(){
                    section.push($(this).attr('data-label'))
                })
                if(data.message!=undefined){
                    for(var i=0;i<data.message.length;i++){
                        if(data.message[i].enable==0){
                            $('div[data-label="'+data.message[i].label+'"]').hide()
                        }
                    }
                }
            }
        })
        }
    })
}
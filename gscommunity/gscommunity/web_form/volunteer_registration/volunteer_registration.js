frappe.ready(function() {
      var docname = frappe.doc_name;
      var vol_form =frappe.web_form_doctype;
    var objectUrl;
    var name = $('h1').text();
    var pathname = window.location.href;
    var url = ''
    var newFile = ''
    var event = ''
    var competition = '';
    if (pathname.includes('?')) {
        url = pathname.split('?')[1];
        newFile = url.split('&')[0];
        event = url.split('&')[1];
        competition = url.split('&')[2];
    }
     var user=getCookie('user_id');
    if(user!='Guest'){        
        get_current_user(newFile);
    }   
  if(vol_form =="Volunteer"){
   
    $('.btn-form-submit').text("Save");
       $('.btn-form-saveonly').hide();
  }
	  
})
function get_current_user(newFile){
    var user=getCookie('user_id');
    var member = getCookie('member_id');

    console.log(member)
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.check_user",
        args: {
            member: member
        },
        callback: function(data) {
            console.log(data)
                      console.log(data.message.name)
            $('input[name="member"]').val(data.message.name)
            $('input[name="email"]').val(data.message.email)
    
        }
    });
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
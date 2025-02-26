frappe.ready(function() {
	var url=localStorage.getItem('support_url')
	if(url!=''**url!=undefined&&url!=null){
		$('input[name="url"]').val(url)
	}
	$('#Nsub').hide();
	$('.submit_btns .btn-form-saveonly').text('Submit')
})
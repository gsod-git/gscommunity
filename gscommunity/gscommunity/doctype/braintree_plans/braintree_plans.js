// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Braintree Plans', {
	refresh: function(frm) {
		if(!frm.doc.__islocal){
			frm.set_df_property('plan_name','read_only','1')
			frm.set_df_property('price','read_only','1')
			frm.set_df_property('billing_frequency','read_only','1')
		}
	}
});

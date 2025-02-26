frappe.listview_settings['Braintree Plans'] = {
	refresh: function(doclist){
		doclist.page.clear_inner_toolbar()
		doclist.page.add_inner_button(__("Sync all plans"), function() {
			frappe.call({
				method:'gscommunity.gscommunity.doctype.braintree_plans.braintree_plans.get_all_plans',
				args:{

				},
				callback:function(data){
					if(data.message=='Success'){
						cur_list.refresh();
					}
				}
			})
		})
	}
}

frappe.listview_settings['Old Members'] = {
    onload: function(list_view) {
		let method = "gscommunity.gscommunity.doctype.old_members.old_members.add_members"

		list_view.page.add_menu_item(__("Register as Member"), function() {
			list_view.call_for_selected_items(method, {  });
		});		
	}
}
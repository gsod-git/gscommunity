// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Old Members', {
	refresh: function(frm) {
		frm.set_query("newsletter", function() {
            return {
                "filters": {
                    "category": "Newsletter"
                }
            };
        });
	},
	membership_type:function(frm){
		if(frm.doc.membership_type){
			frappe.call({
				method: "frappe.client.get_value",
		        args: {
		            'doctype': "Membership Type",
		            'filters': { 'name': frm.doc.membership_type },
		            'fieldname': [
		                'has_family', 'count'
		            ]
		        },
		        callback:function(data){
		        	frm.set_value('family_members_limit',data.message.count)
		        }
			})
		}
	}
});
frappe.ui.form.on("Other Members", "relation", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    frappe.call({
    	method:'gscommunity.gscommunity.doctype.old_members.old_members.get_relation_ship_group',
    	args:{
    		relation:item.relation
    	},
    	callback:function(data){
    		if(data.message){
    			frappe.model.set_value(cdt, cdn, "relationship_group", data.message);
    		}
    	}
    })
});
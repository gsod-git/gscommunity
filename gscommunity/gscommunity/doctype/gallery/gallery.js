// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gallery', {
    refresh: function(frm) {
        // frappe.call({
        //     method: "gscommunity.gscommunity.doctype.events.events.get_events",
        //     args: {},
        //     callback: function(r) {
        //         console.log(r.message)
        //         var array = [];
        //         for (var i = 0; i < r.message.length; i++) {
        //             // console.log(r.message[i].fieldname)
        //             array.push(r.message[i].name);
        //             console.log(array)
        //             // frm.set_df_property("fields", "options", array);
        //         }



        //         frm.set_df_property("name1", "options", array);
        //         frm.events.properties(frm)

        //     }
        // })
        frm.set_query("events", function(frm) {
            return {
                query: "gscommunity.gscommunity.doctype.gallery.gallery.get_events"

            };
        });
    }
});
// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Committee', {
    refresh: function(frm) {
        var d = new Date();
        var Firstdate = new Date(d.getFullYear(), 0, 1);
        var Lastdate = new Date(d.getFullYear(), 11, 31);
        var old_year = frm.doc.year;
        var date = new Date();
        frm.set_value("year",
            date.getFullYear())
        o_year=old_year-1
        if (!frm.doc.__islocal) {
            frappe.contacts.render_address_and_contact(frm);

            // custom buttons
            frm.add_custom_button(__('Previous Members'), function() {
                frappe.set_route('query-report', 'Committee Members Report', { committee: frm.doc.name,year:o_year });

            });
        }
    },
    onload: function(frm) {
        var last_date = new Date(new Date().getFullYear(), 11, 31)        
        var year = last_date.getFullYear();
        $('div[data-fieldname="table_4"] .form-grid .grid-body .rows .grid-row').each(function(){
            var date=$(this).find('div[data-fieldname="from_date"] .static-area').html();            
            if(date.split('-')[2]!=year){
                $(this).hide();
            }
        });   

    }
});
frappe.ui.form.on("Team Members", "from_date", function(frm, cdt, cdn) { 
    var item = frappe.get_doc(cdt,cdn);
    var last_date = new Date(new Date().getFullYear(), 11, 31)
    var month = (last_date.getMonth() + 1)
    var day =last_date.getDate()
    var year=item.from_date.split('-')[0]
    var dateformat=year+'-'+month+'-'+day
    frappe.model.set_value(cdt, cdn, "to_date",dateformat );
    frappe.model.set_value(cdt, cdn, "year",year );    
});

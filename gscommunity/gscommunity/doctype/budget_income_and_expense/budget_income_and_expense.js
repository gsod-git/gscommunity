// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Budget Income And Expense', {
    refresh: function(frm) {
        
        frm.set_query("accounting_category", "table_4", function(doc, cdt, cdn) {
            child = locals[cdt][cdn];
            return {
                query: "gscommunity.gscommunity.doctype.budget_income_and_expense.budget_income_and_expense.get_accounting_category",
                txt: child.accounting_group
            };
        });
    }
});

frappe.ui.form.on("Budget Income And Expense", "refresh", function(frm) {
    cur_frm.set_query("events", function() {
        return {
            "filters": {
                "event_type": (frm.doc.event_type)
            }
        };
    });
});
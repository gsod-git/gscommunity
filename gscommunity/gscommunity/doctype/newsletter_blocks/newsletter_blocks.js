// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Newsletter Blocks', {
    refresh: function(frm) {

    },
    generate_html: function(frm) {
        if (frm.doc.components) {
            var html = '<div class="block ' + frm.doc.name + '">'
            var layout = ''
            if (frm.doc.layout_type == 'Single Column') {
                layout = 'width:100%;'
            } else if (frm.doc.layout_type == 'Two Column') {
                layout = 'width:50%;'
            } else {
                layout = 'width:33.33%;'
            }
            var first_column = '<div class="first_column" style="float: left;position: relative;min-height: 1px;' + layout + '">'
            var second_column = '<div class="second_column" style="float: left;position: relative;min-height: 1px;' + layout + '">'
            var third_column = '<div class="third_column" style="float: left;position: relative;min-height: 1px;' + layout + '">'
            for (var i = 0; i < frm.doc.components.length; i++) {
                var wrapper_cls=frm.doc.components[i].component+'-'+parseInt(i+1)
                if (frm.doc.components[i].column == 'First Column') {
                    first_column += '<div class="'+wrapper_cls+'" style="padding-left: 15px;padding-right: 15px;">'+frm.doc.components[i].value+'</div>'
                } else if (frm.doc.components[i].column == 'Second Column') {
                    second_column += '<div class="'+wrapper_cls+'" style="padding-left: 15px;padding-right: 15px;">'+frm.doc.components[i].value+'</div>'
                } else {
                    third_column += '<div class="'+wrapper_cls+'" style="padding-left: 15px;padding-right: 15px;">'+frm.doc.components[i].value+'</div>'
                }
            }
            first_column += '</div>'
            second_column += '</div>'
            third_column += '</div>'
            if ($(first_column).html() != '')
                html += first_column
            if ($(second_column).html() != '')
                html += second_column
            if ($(third_column).html() != '')
                html += third_column
            html += '</div>'
            frm.set_value('content', html)
        }
    }
});
frappe.ui.form.on("Block Components", "value", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    content = item.html;
    // if (item.type == 'Text' || item.type == 'Button') {
    //     content = '<div><p class="' + item.component + '">' + item.value + '</p></div>'
    // } else if (item.type == 'Button') {
    //     content = '<div><button class="btn ' + item.component + '">' + item.value + '</button></div>'
    // } else if (item.type == 'Link') {
    //     content = '<div><a href="" class="' + item.component + '">' + item.value + '</a></div>'
    // } else {
    //     content = '<div><img src="" alt="' + item.component + '" style="display: block;max-width: 100%;" /></div>'
    // }
    // frappe.model.set_value(cdt, cdn, "html", content);
});
frappe.ui.form.on("Block Components", "component", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    content = ''
    // if (item.type == 'Text') {
    //     content = '<div><p class="' + item.component + '">' + item.value + '</p></div>'
    // } else if (item.type == 'Button') {
    //     content = '<div><button class="btn ' + item.component + '">' + item.value + '</button></div>'
    // } else if (item.type == 'Link') {
    //     content = '<div><a href="" class="' + item.component + '">' + item.value + '</a></div>'
    // } else {
    //     content = '<div><img src="" alt="' + item.component + '" style="display: block;max-width: 100%;" /></div>'
    // }
    // frappe.model.set_value(cdt, cdn, "html", content);
});
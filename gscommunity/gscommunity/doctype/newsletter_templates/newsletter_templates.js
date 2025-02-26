// Copyright (c) 2018, valiantsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Newsletter Templates', {
	refresh: function(frm) {
		
	},generate_template:function(frm){
		if(frm.doc.template_blocks){
			var html='<div class="template">'
			for(var i=0;i<frm.doc.template_blocks.length;i++){				
				html+='<div id='+frm.doc.template_blocks[i].block_id+'>'
				html+=frm.doc.template_blocks[i].content
				html+='</div>'
			}
			html+='</div>'
			frm.set_value('template',html)
		}
	},view_template:function(frm){
		var styles=frm.doc.styles.split('/n')
		for(var i=0;i<styles.length;i++){
			if(styles[i]!=''){
				var class1=styles[i].split('{')[0]
				var style1=styles[i].split('{')[1].split('}')[0]
				if(class1=='.template'){
					var prev_style=$('div[data-fieldname="template"] .template').attr('style')
					var new_style=''
					if(prev_style!=undefined&&prev_style!=''){
						new_style=prev_style+style1
					}else{
						new_style=style1
					}
					$('div[data-fieldname="template"] .template').attr('style',new_style)
				}
				$('div[data-fieldname="template"] .template '+class1).each(function(){
					var prev_style=$(this).attr('style')
					var new_style=''
					if(prev_style!=undefined&&prev_style!=''){
						new_style=prev_style+style1
					}else{
						new_style=style1
					}	
					$(this).attr('style',new_style)
				})						
			}
		}
		frm.set_value('template',$('div[data-fieldname=template] .control-value').html())
	},template:function(frm){
		var html=frm.doc.template;
		console.log(frm.doc.template_blocks)
		for(var i=0;i<frm.doc.template_blocks.length;i++){
			var ref=$(html).find('#'+frm.doc.template_blocks[i].block_id).html();
			frappe.model.set_value(frm.doc.template_blocks[i].doctype,frm.doc.template_blocks[i].name,'content',ref)
		}
	}
});
frappe.ui.form.on("Template Blocks", "block", function(frm, cdt, cdn) {
    var item = frappe.get_doc(cdt, cdn);
    var id=item.block+'-'+item.idx;
    frappe.model.set_value(cdt, cdn, "block_id", id);
});
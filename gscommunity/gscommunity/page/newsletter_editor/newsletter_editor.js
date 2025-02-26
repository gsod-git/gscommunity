frappe.pages['newsletter-editor'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Newsletter Editor',
        single_column: true
    });
    $('.page-content').find('.layout-main').append(frappe.render_template("editor_dashboard", {
        // content: frappe.session.user_fullname
    }));
    // frappe.newsletter_editor.refresh(wrapper)
    // $("<div class='editor' style='min-height: 200px;'></div>").appendTo(page.main);

}
var new_blocks=[]
var deleted_blocks=[]
frappe.pages['newsletter-editor'].refresh = function(wrapper) {  
    var to_editor=localStorage.getItem('to_editor')
    if(to_editor){
        localStorage.removeItem('to_editor')
        location.reload();
    }  
    var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1]
    newsletter_click(newsletter)
	var html='<button id="preview_btn" class="btn btn-default btn-sm primary-action left_mg" onclick="gotonewsletter()"><i class="visible-xs octicon octicon-check"></i><span class="hidden-xs">Back to Newsletter</span></button>'
	html+='<button id="save_btn" class="btn btn-primary btn-sm primary-action" onclick="save_preview()"><i class="visible-xs octicon octicon-check"></i><span class="hidden-xs">Save</span></button>'
	$('.page-actions').append(html)
    // $('.main-sidebar .sidebar-menu').hide()
    // $('.main-sidebar .sidebar').append('<ul id="treeDemo" class="ztree"></ul>')
    var a;
    $.ajax({
        async: false,
        url: window.location.origin + "/api/method/gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_tree_data",
        success: function(r) {
            a = r.message;
        }
    });
    var zTreeObj;

    function myOnClick(event, treeId, treeNode) {
        var ops = $(".maindiv ul.nav-tabs li.active").text().trim().split(' ')[0];
        var opslen = ops.length;

        if (treeNode.type == "year") {
            year_click(treeNode, ops, opslen)
        }
        if (treeNode.type == "newsletter") {
            newsletter_click(treeNode, ops, opslen)
        }
        if (treeNode.type == "template") {
            template_click(treeNode, ops, opslen)
        }
        if (treeNode.type == "block") {
            block_click(treeNode, ops, opslen)
        }
    };
    var setting = {
        callback: {
            onClick: myOnClick
        }
    };

    function go(a) {
        var arr = [];
        for (var i = 0; i < a.year.length; i++) {
            arr.push({
                'name': a.year[i].year,
                'open': a.year[i].open,
                'children': construct_newsletter(a.year[i].year, a),
                'type': 'year',
                'idname': a.year[i].year
            })
        }

        return arr
    }

    function construct_newsletter(u, a) {
        var arr1 = [];
        for (var i = 0; i < a.newsletter.length; i++) {
            var date = new Date(a.newsletter[i].creation)
            if (date.getFullYear() == u) {
                arr1.push({
                    'name': a.newsletter[i].subject,
                    'open': a.newsletter[i].open,
                    'children': construct_template(a.newsletter[i].template, a, a.newsletter[i].name),
                    'type': 'newsletter',
                    'idname': a.newsletter[i].name
                })
            }
        }
        return arr1
    }

    function construct_template(u, a, newsletter) {
        var arr2 = [];
        for (var i = 0; i < a.template.length; i++) {
            if (a.template[i].name == u) {
                arr2.push({
                    'name': a.template[i].title,
                    'open': a.template[i].open,
                    'children': construct_blocks(a.template[i].name, a, newsletter),
                    'type': 'template',
                    'idname': a.template[i].name
                })
            }
        }
        return arr2
    }

    function construct_blocks(u, a, newsletter) {
        var arr3 = [];
        for (var i = 0; i < a.block.length; i++) {
            if (a.block[i].parent == newsletter) {
                arr3.push({
                    'name': a.block[i].block,
                    'type': 'block',
                    'idname': a.block[i].name
                })
            }
        }
        return arr3
    }


    // var zNodes = go(a)

    // zTreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);    
    var modal_html='<div id="block_modal" class="modal fade" style="overflow: auto; padding-right: 17px;" tabindex="-1">'
    modal_html+='<div class="modal-dialog"><div class="modal-content"><div class="modal-header">'
    modal_html+='<a type="button" class="close" data-dismiss="modal" aria-hidden="true"></a>'
    modal_html+='<h4 class="modal-title">Blocks</h4></div><div class="modal-body ui-front"></div></div></div></div>'
    // $('.main-section').append(modal_html)
    get_all_block_details()
}
frappe.newsletter_editor = {
    refresh: function(wrapper) {
        if (wrapper) {
            this.wrapper = $(wrapper);
        }
        this.render();
    },
    render: function() {
        var me = this;
        // frappe.utils.set_title(__("Newsletter Editor"));
        // var template='newsletter_editor'
        // var newsletter_list=frappe.newsletter_editor.get_all_newsletters()
        // frappe.newsletter_editor.wrapper.html(frappe.render_template('newsletter_editor', {}));

        // $(document).trigger("newsletter-editor-render");
    }
}

function year_click(treeNode, ops, opslen) {

}

function newsletter_click(treeNode, ops, opslen) {
    frappe.call({
        method: 'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_newsletter_details',
        args: {
            newsletter: treeNode
        },
        callback: function(data) {
            console.log(data.message)
            if (data.message) {
                $('.maindiv').html(frappe.render_template("newsletter_editor", { 
                	template: data.message.message, 
                	components: "",
                	newsletter:treeNode
                }));
                $(".preview_details .fixed_class").slimScroll({
                    height: ($(document).height() - 150)
                })

                for(var i=0;i<data.message.components.length;i++){
                    var icon_html='<div id="block_icons"><div class="abs_cls"><a class="add_top"><span class="fa fa-plus"></span></a></div><div class="abs_cls"><a class="delete"><span class="fa fa-trash"></span></a></div><div class="abs_cls"><a class="add_bottom"><span class="fa fa-plus"></span></a></div></div>'
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onclick','get_block_data("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onmouseover','show_items("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onmouseout','hide_items("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids+' .block').append(icon_html)
                }
            }
        }
    })
}

function template_click(treeNode) {
    var newsletter = treeNode.getParentNode().idname
    frappe.call({
        method: 'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_newsletter_details',
        args: {
            newsletter: newsletter
        },
        callback: function(data) {
            if (data.message) {
                $('.maindiv').html(frappe.render_template("newsletter_editor", { 
                	template: data.message.message, 
                	components: "",
                	newsletter:newsletter
                }));
                $(".preview_details .fixed_class").slimScroll({
                    height: ($(document).height() - 100)
                })
            }
        }
    })
}

function block_click(block,newsletter) {
    // var template = treeNode.getParentNode().idname
    // var newsletter = treeNode.getParentNode().getParentNode().idname
    // var block = treeNode.idname
    frappe.call({
        method: 'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_bloc_details',
        args: {
            newsletter: newsletter,
            block: block
        },
        callback: function(data) {            
            if (data.message) {
                var fields = [];
                var field_list = data.message.block[0].fields_data_type.split(';')
                var block_html=''             
                for (var i = 0; i < field_list.length - 1; i++) {
                    var list = {};
                    field_data = field_list[i].split(',')
                    list.type = field_data[1];
                    list.otr_class = field_data[0] + '-' + field_data[2]
                    list.inr_class = field_data[0]
                    list.count = i + 1;
                    acc_class='fa fa-chevron-down'
                    display=''
                    if(i==0){
                        acc_class='fa fa-chevron-up'
                        display='display:block'
                    }
                    block_html+='<div data-type="'+list.type+'" data-otr_cls="'+list.otr_class+'" data-inr_cls="'+list.inr_class+'" class="accordion"><b>'+list.inr_class+'</b><span class="fa fa-chevron-up">'
                    
                    block_html+='</span></div><div class="panelcode" style="'+display+'"><h6 style="text-transform: capitalize;">'+list.inr_class+'</h6>'
                    if(list.type=='Text'){
                        block_html+='<input type="text" onchange="get_value(this)" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'" data-inclass="'+list.inr_class+'" data-block="'+block+'">'
                    }else if(list.type=='Image'){
                        block_html+='<img src="" class="img-responsive '+list.otr_class+'" style="max-height: 170px;margin:auto;" name="'+list.otr_class+'">'
                        block_html+='<input type="file" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'" data-inclass="'+list.inr_class+'" onchange="upload(this)" data-block="'+block+'">'
                        block_html+='<input type="hidden" name="image-'+list.otr_class+'" id="image-'+list.otr_class+'">'
                    }else if(list.type=='Link'){
                        block_html+='<p>Link Text</p><input type="text" onchange="get_value(this)" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'" data-inclass="'+list.inr_class+'" data-block="'+block+'">'                            
                        block_html+='<p>Link Url</p><input type="text" onchange="get_value(this)" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'-url" data-inclass="'+list.inr_class+'" data-block="'+block+'">'
                    }else if(list.type=='Button'){
                        block_html+='<p>Button Text</p><input type="text" onchange="get_value(this)" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'" data-inclass="'+list.inr_class+'" data-block="'+block+'">'
                        block_html+='<p>Button Url</p><input type="text" onchange="get_value(this)" name="'+list.otr_class+'" class="form-control" id="'+list.otr_class+'-url" data-inclass="'+list.inr_class+'" data-block="'+block+'">'
                    }else if(list.type=='Html'){
                        block_html+='<textarea name="'+list.otr_class+'" onchange="get_value(this)" class="form-control" id="'+list.otr_class+'" data-inclass="'+list.inr_class+'" data-block="'+block+'"></textarea>'                        
                    }
                    block_html+='</div>'
                    fields.push(list)
                }
                // $('.maindiv').html(frappe.render_template("newsletter_editor", {
                //     template: data.message.newsletter.message,
                //     components: data.message.block[0],
                //     fields_list: fields,
                //     newsletter:newsletter
                // }));
                $('.maindiv .block_details .fixed_class').html(block_html)
                
                $(".preview_details .fixed_class").slimScroll({
                    height: ($(document).height() - 100)
                })
                $(".block_details .fixed_class").slimScroll({
                    height: ($(document).height() - 100)
                })
                $('.preview_details #'+block+' #block_icons .add_top').attr('onclick','add_block_up("'+block+'")')
                $('.preview_details #'+block+' #block_icons .add_bottom').attr('onclick','add_block_down("'+block+'")')
                $('.preview_details #'+block+' #block_icons .delete').attr('onclick','delete_block("'+block+'")')
                loaddata(data.message.block[0], fields,data.message.newsletter.message)
                accordion()
            }
        }
    })
}

function loaddata(components, fields_list,template) {  
    if (fields_list) {
        for (var i = 0; i < fields_list.length; i++) {
            if (fields_list[i].type == 'Image') {
                var src = $(template).find('#'+components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).attr('src');
                $('.maindiv .block_details .' + fields_list[i].otr_class).attr('src', src)
            } else if (fields_list[i].type == 'Link') {
                var href = $(template).find('#'+components.block_ids).find('#' + components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).attr('href');
                var text = $(template).find('#'+components.block_ids).find('#' + components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).text();
                $('.maindiv .block_details .'+fields_list[i].otr_class+'-url').attr('href',href)
                $('.maindiv .block_details .'+fields_list[i].otr_class).text(text)
            } else if (fields_list[i].type == 'Button') {
                var href = $(template).find('#'+components.block_ids).find('#' + components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).attr('href');
                var text = $(template).find('#'+components.block_ids).find('#' + components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).text();
            	$('.maindiv .block_details .'+fields_list[i].otr_class+'-url').attr('href',href)
                $('.maindiv .block_details .'+fields_list[i].otr_class).text(text)
            } else if(fields_list[i].type=='Html') {
                var text = $(template).find('#'+components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).html();
                $('.maindiv .block_details #' + fields_list[i].otr_class).val(text)
                $('.block_details #' + fields_list[i].otr_class).summernote({
                    height: 150,
                    toolbar: false                    
                }).on('summernote.change', function(customEvent, contents, $editable) {  
                    var id=$(customEvent.currentTarget).attr('id')
                    var block=$(customEvent.currentTarget).attr('data-block')
                    console.log(id,block,contents)
                    $('.preview_details .fixed_class #'+block+' .'+id).html(contents)
                });
            }else if(fields_list[i].type=='Text'){
                var text = $(template).find('#'+components.block_ids).find('.' + fields_list[i].otr_class).find('.' + fields_list[i].inr_class).text();
                $('.maindiv .block_details #' + fields_list[i].otr_class).val(text)
            }
        }
    }    
}

function save_block() {
    var block_id = $('#block').val();
    var name=$('#component_name').val();
    var parent=$('#parent').val();
    var preview=$('.preview_details .fixed_class').html()
    var source_text=''
    $('.block_details .accordion').each(function() {
        var type = $(this).attr('data-type');
        var inr_cls = $(this).attr('data-inr_cls')
        var otr_cls = $(this).attr('data-otr_cls')
        if (type == 'Image') {
            var src=$(this).parent().find('.panel').find('.'+otr_cls).attr('src')
            $('.preview_details .fixed_class').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).attr('src',src)
            $(html).find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).attr('src',src)
            source_text+=otr_cls+'_e-s_'+inr_cls+'_e-s_'+src+'_end_'
        }
        else if(type=='Link' || type=='Button'){
        	var text=$(this).parent().find('.panel').find('#'+otr_cls).val()
        	var href=$(this).parent().find('.panel').find('#'+otr_cls+'-url').val()
        	$('.preview_details .fixed_class').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).attr('href',href)
        	$('.preview_details .fixed_class').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).text(text)
            $(html).find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).attr('href',href)
            $(html).find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).text(text)
        }else if(type=='Html'){
            var text=$(this).parent().find('.panel').find('#'+otr_cls).val()
            $('.preview_details .fixed_class').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).html(text)
            $(html).find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).html(text)
        } else{
        	var text=$(this).parent().find('.panel').find('#'+otr_cls).val()
        	$('.preview_details .fixed_class').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).text(text)
            $('.block_details .fixed_class #html').find('#'+block_id).find('.'+otr_cls).find('.'+inr_cls).text(text)
        }
    })
    var html=$('.block_details .fixed_class #html').html()
    var fields=$('.block_details .fixed_class #fields_type').val()
    save_child_block(html,fields,name,parent,source_text)
    $('#html').html(html)   
}

function accordion() {
    var acc = document.getElementsByClassName("accordion");
    var i;
    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            if ($(this).find('span').attr('class') == 'fa fa-chevron-up') {
                $(this).find('span').removeClass('fa-chevron-up');
                $(this).find('span').addClass('fa-chevron-down');
            } else {
                $(this).find('span').addClass('fa-chevron-up');
                $(this).find('span').removeClass('fa-chevron-down');
            }
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }
}

function upload(e){
	var file = e.files[0];
    var $input = $(e);
    var id=$(e).attr('id')
    var block=$(e).attr('data-block')
    var cls=$(e).attr('data-inclass')
    var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1]
    var input = $input.get(0);
    if (input.files.length) {
        input.filedata = { "files_data": [] }; //Initialize as json array.
        window.file_reading = true;
        var dataurl = '';
        $.each(input.files, function(key, value) {
            var name = value.name;
            var reader = new FileReader();
            var docname = newsletter;
            reader.onload = function(e) {
                dataurl = reader.result;
                var modal_html = '<div id="upload_modal" class="modal fade" style="overflow: auto; display: block; padding-right: 17px;" tabindex="-1"><div class="modal-dialog"><div class="modal-content">';
                modal_html += '<div class="modal-header"><a type="button" class="close" data-dismiss="modal" aria-hidden="true"></a><h4 class="modal-title">Song Upload</h4></div>'
                modal_html += '<div class="modal-body ui-front">Uploading......</div>'
                modal_html += '</div></div></div>'
                $('#helpactive').append(modal_html)
                $('#upload_modal').modal('show')
                frappe.call({
                    method: "uploadfile",
                    args: {
                        from_form: 1,
                        doctype: 'Newsletter',
                        docname: docname,
                        is_private: 0,
                        filename: input.files[0].name,
                        file_url: '',
                        filedata: dataurl,
                        file_size: input.files[0].size
                    },
                    freeze: true,
                    callback: function(data) {
                        if(data.message){
                        	$('.maindiv .block_details .'+id).attr('src',data.message.file_url)
                            $('.maindiv .preview_details #'+block+' .'+id+' .'+cls).attr('src',data.message.file_url)
                            save_template_component(block,$('.preview_details .fixed_class #'+block).html())
                        }                     
                    }
                })
            }
            reader.readAsDataURL(file);
        });
        window.file_reading = false;
    }
}

function save_preview(){
    var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1]	
    if(prev_block!='')
        $('.preview_details .fixed_class #'+prev_block).css('border','none')	
    $('.preview_details .fixed_class #block_icons').each(function(){
        $(this).remove()
    })
    var html=$('.preview_details .fixed_class').html()
	if(newsletter){
		frappe.call({
			method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.save_template',
			args:{
				newsletter:newsletter,
				html:html,
                deleted_blocks:deleted_blocks
			},
			freeze:true,
			callback:function(data){
				frappe.msgprint('Newsletter updated successfully','Success')
                location.reload();
			}
		})
	}		
}
function gotonewsletter(){
	var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1]
	// $('.main-sidebar .sidebar-menu').show()
	// $('.main-sidebar #treeDemo').hide()
	// $('.page-actions #preview_btn').hide()
 //    $('.page-actions #save_btn').hide()
 //    $('.page-head').css('height','70px')
 //    $('.page-head h1').css('margin-top','17px')
 //    $('.page-head h1').css('font-size','24px')
 //    $('.page-content').css('margin-top','121px')
    localStorage.setItem('from_editor','1')
    var redirec_url=window.location.origin+'/desk#Form/Newsletter/'+newsletter
    console.log(redirec_url)
	window.location.href=redirec_url   
}
function save_child_block(html,fields,name,parent,source_text){    
    // console.log(source_text)
    frappe.call({
        method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.save_block_contents',
        args:{
            html:html,
            source_text:source_text,
            name:name,
            parent:parent
        },
        callback:function(data){
            console.log(data.message)
        }
    })
}
var prev_block=''
function get_block_data(block){
    if(block){
        $('.preview_details .fixed_class #'+block).css('border','2px solid #e50041')
        if(prev_block!=''){
            $('.preview_details .fixed_class #'+prev_block).css('border','none')
            $('.preview_details #'+block+' #block_icons .add_top').removeAttr('onclick')
            $('.preview_details #'+block+' #block_icons .add_bottom').removeAttr('onclick')
            $('.preview_details #'+block+' #block_icons .delete').removeAttr('onclick')
        }
        prev_block=block
        var url=window.location.href;
        var newsletter=url.split('#newsletter-editor')[1].split('/')[1]
        block_click(block,newsletter)
    }
}
function get_value(e){
    var id=$(e).attr('id')
    var block=$(e).attr('data-block')
    var cls=$(e).attr('data-inclass')
    var text=$('#'+id).val()
    $('.preview_details .fixed_class #'+block+' .'+id+' .'+cls).text(text)
    save_template_component(block,$('.preview_details .fixed_class #'+block).html())
}
function show_items(block){
    var icon_html='<div id="block_icons"><div><a onclick="add_block_up('+block+')"><span class="fa fa-plus"></span></a></div><div><a onclick="delete_block('+block+')"><span class="fa fa-trash"></span></a></div><div><a onclick="add_block_down('+block+')"><span class="fa fa-plus"></span></a></div></div>'
    var block_height=$('#'+block).height() 
    var height=block_height-10;
    var top='calc(100% - -'+height+'px)'    
    $('.preview_details .fixed_class #'+block).css('border','2px solid #e50041')
    $('.preview_details .fixed_class #'+block).find('#block_icons').show()
    $('.preview_details .fixed_class #'+block).find('#block_icons .add_bottom').css('top',top)
    // $('.preview_details .fixed_class #'+block).find('#block_icons .add_bottom').css('border','1px solid')
    // $('.preview_details .fixed_class #'+block).find('#block_icons .add_bottom').css('border-radius','50%')
    // $('.preview_details .fixed_class #'+block).find('#block_icons .add_bottom').css('background','#fff')
    // if(prev_block!='')
    //     $('.preview_details .fixed_class #'+prev_block).css('border','none')
}
function hide_items(block){
    $('#icon_html').remove();    
    if(prev_block!=block){
        $('.preview_details .fixed_class #'+block).css('border','none')
        $('.preview_details .fixed_class #'+block).find('#block_icons').hide()
    }
}
function add_block_up(block){
    blocks=block.split('-')
    var block_id=blocks[blocks.length-1]
    // var html=$('#block_lists').html()
    $('#block_modal #add_block_id').val(block_id)
    $('#block_modal #block_position').val('up')
    $('#block_modal').modal('show')
}
function add_block_down(block){
    blocks=block.split('-')
    var block_id=blocks[blocks.length-1]
    // var html=$('#block_lists').html()
    $('#block_modal #add_block_id').val(block_id)
    $('#block_modal #block_position').val('down')
    $('#block_modal').modal('show')
}
function delete_block(block){
    if(block){
        var url=window.location.href;
        var newsletter=url.split('#newsletter-editor')[1].split('/')[1] 
        $('.preview_details .fixed_class #'+block).remove()
        deleted_blocks.push({'block':block,'newsletter':newsletter})
    }
}
function get_all_block_details(){
    frappe.call({
        method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_all_blocks',
        args:{
            
        },
        callback:function(data){
            if(data.message){
                var html='<div class="row"><input type="hidden" id="add_block_id" value=""/><input type="hidden" id="block_position" value=""/>'
                for(var i=0;i<data.message.length;i++){
                    var block_count=0;
                    var fields_list=''
                    $.each(data.message[i].components, function(i, j) {
                        block_count = block_count + 1;
                        fields_list += j.component + ',' + j.type + ',' + block_count + ';'                        
                    })
                    var content=data.message[i]
                    html+='<div style="cursor:pointer;" class="col-md-6 list" id="'+content.name+'" onclick="add_block(this)"><div class="prototype"><h6>'+content.name1+'</h6></div><div class="html" style="display:none;">'+content.content+'</div><div class="components" style="display:none;">'+fields_list+'</div></div>'
                }
                html+='</div>'
                $('#block_lists').html(html)
            }
        }
    })
}
function add_block(e){
    var id=$(e).attr('id')
    var html=$('#'+id+' .html').html()    
    var block_id=$('#block_modal #add_block_id').val()
    var block_position=$('#block_modal #block_position').val()
    var fields_list=$('#'+id+' .components').html()
    if(block_position=='down')
        block_id=block_id+1
    var preview_html=$('.preview_details .fixed_class .template').html()
    var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1] 
    frappe.call({
        method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.get_newsletter_details',
        args:{
            newsletter:newsletter
        },
        callback:function(data){
            if(data.message){
                var changed=false;
                var new_html=''
                var last_block=data.message.components[data.message.components.length-1].block_ids;
                var last_idx=data.message.components[data.message.components.length-1].idx;
                var last_block_id=last_block.split('-')
                var l_id=last_block_id[last_block_id.length-1]
                for(var i=0;i<data.message.components.length;i++){
                    var components=data.message.components[i];
                    if((i+1)==parseInt(block_id)){
                        changed=true;
                        var new_blk={}
                        new_blk.idx=parseInt(last_idx+1)
                        new_blk.block_ids=id+'-'+l_id                        
                        new_blk.block=id;
                        new_blk.fields_data_type=fields_list                        
                        // if(data.message.custom_css){
                        //     var styles = data.message.custom_css.split('/n')
                        //     for (var i = 0; i < styles.length; i++) {
                        //         if (styles[i] != '') {
                        //             var class1 = styles[i].split('{')[0]
                        //             var style1 = styles[i].split('{')[1].split('}')[0]

                        //             $(html + class1).each(function() {
                        //                 var prev_style = $(this).attr('style')
                        //                 var new_style = ''
                        //                 if (prev_style != undefined && prev_style != '') {
                        //                     new_style = prev_style + style1;
                        //                 } else {
                        //                     new_style = style1
                        //                 }
                        //                 $(this).attr('style', new_style)
                        //             })
                        //         }
                        //     }
                        // }
                        new_blk.html=html
                        new_blocks.push(new_blk)
                        new_html+='<div id="'+new_blk.block_ids+'">'+html+'</div>'
                    }
                    var old_html=$('.preview_details .fixed_class #'+components.block_ids).html()    
                    new_html+='<div id="'+components.block_ids+'">'+old_html+'</div>'
                }
                
                $('.preview_details .fixed_class .template').html(new_html)
                var icon_html='<div id="block_icons"><div class="abs_cls"><a class="add_top"><span class="fa fa-plus"></span></a></div><div class="abs_cls"><a class="delete"><span class="fa fa-trash"></span></a></div><div class="abs_cls"><a class="add_bottom"><span class="fa fa-plus"></span></a></div></div>'
                for(var i=0;i<data.message.components;i++){                    
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onclick','get_block_data("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onmouseover','show_items("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids).attr('onmouseout','hide_items("'+data.message.components[i].block_ids+'")')
                    $('.preview_details .fixed_class').find('#'+data.message.components[i].block_ids+' .block').append(icon_html)
                }
                $('.preview_details .fixed_class').find('#'+id+'-'+l_id).attr('onclick','get_block_data("'+data.message.components[i].block_ids+'")')
                $('.preview_details .fixed_class').find('#'+id+'-'+l_id).attr('onmouseover','show_items("'+data.message.components[i].block_ids+'")')
                $('.preview_details .fixed_class').find('#'+id+'-'+l_id).attr('onmouseout','hide_items("'+data.message.components[i].block_ids+'")')
                $('.preview_details .fixed_class').find('#'+id+'-'+l_id+' .block').append(icon_html)
                $('#block_modal').modal('hide')
                $('.preview_details .fixed_class #block_icons').each(function(){
                    $(this).remove()
                })
                var message=$('.preview_details .fixed_class').html()
                save_new_block(newsletter,block_id,message)
            }
        }
    })
}
function save_new_block(newsletter,idx,message){
    frappe.call({
        method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.add_new_block',
        args:{
            newsletter:newsletter,
            idx:idx,
            message:message,
            new_blocks:new_blocks,
            deleted_blocks:deleted_blocks
        },
        callback:function(data){
            location.reload()
        }
    })
}
function save_template_component(block,html){
    var url=window.location.href;
    var newsletter=url.split('#newsletter-editor')[1].split('/')[1]
    frappe.call({
        method:'gscommunity.gscommunity.page.newsletter_editor.newsletter_editor.update_blocks',
        args:{
            block:block,
            html:html,
            newsletter:newsletter
        },
        callback:function(data){
            
        }
    })
}
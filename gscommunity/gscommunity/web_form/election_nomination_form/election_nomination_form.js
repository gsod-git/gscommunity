frappe.ready(function() {
    var pathname = window.location.href;
    url = ''
    filetype = ''
    election = ''
    if (pathname.includes('?')) {
        url = pathname.split('?')[1];
        election = url.split('&')[1];
        filetype = url.split('&')[0];
    }
    if (filetype == 'new=1') {

    }
    check_user()
    if (election != '') {
        election = election.split('=')[1]
        $('input[name="election"]').val(election)
        get_election_info(election, filetype)
    }
    $('input[data-label="Sign Name"]').val('')
    $('input[data-label="Form Name"]').val('')
    $('div[data-label=Acknowledgement] .attach-input-wrap').css('width', '37%')
    $('div[data-label=Acknowledgement] input[name="signature"]').parent().css('width', '50%')
    $('div[data-label="Nomination Form"] .attach-input-wrap').css('width', '37%')
    $('#Nsub').hide()
    // $('input[name="signature"]').on('change', function(e) {
    //     var file = e.currentTarget.files[0];
    //     var $input = $(this);
    //     var input = $input.get(0);
    //     if (input.files.length) {
    //         input.filedata = { "files_data": [] }; //Initialize as json array.
    //         window.file_reading = true;
    //         var dataurl = '';
    //         $.each(input.files, function(key, value) {
    //             var name = value.name;
    //             var reader = new FileReader();
    //             // var docname = $('#docname').val()
    //             console.log(docname)
    //             reader.onload = function(e) {
    //                 dataurl = reader.result;
    //                 var modal_html = '<div id="upload_modal" class="modal fade" style="overflow: auto; display: block; padding-right: 17px;" tabindex="-1"><div class="modal-dialog"><div class="modal-content">';
    //                 modal_html += '<div class="modal-header"><a type="button" class="close" data-dismiss="modal" aria-hidden="true"></a><h4 class="modal-title">Song Upload</h4></div>'
    //                 modal_html += '<div class="modal-body ui-front">Uploading......</div>'
    //                 modal_html += '</div></div></div>'
    //                 $('#helpactive').append(modal_html)
    //                 $('#upload_modal').modal('show')
    //                 upload(input.files[0].name,dataurl,'signature',input.files[0].size)
    //                 $input.wrap('<form>').closest('form').get(0).reset();
    //         		$input.unwrap();   
    //             }
    //             reader.readAsDataURL(file);
    //         });
    //         window.file_reading = false;
    //     }
    // })
    // $('input[name="nomination_form"]').on('change', function(e) {
    //     var file = e.currentTarget.files[0];
    //     var $input = $(this);
    //     var input = $input.get(0);
    //     if (input.files.length) {
    //         input.filedata = { "files_data": [] }; //Initialize as json array.
    //         window.file_reading = true;
    //         var dataurl = '';
    //         $.each(input.files, function(key, value) {
    //             var name = value.name;
    //             var reader = new FileReader();
    //             // var docname = $('#docname').val()
    //             console.log(docname)
    //             reader.onload = function(e) {
    //                 dataurl = reader.result;
    //                 var modal_html = '<div id="upload_modal" class="modal fade" style="overflow: auto; display: block; padding-right: 17px;" tabindex="-1"><div class="modal-dialog"><div class="modal-content">';
    //                 modal_html += '<div class="modal-header"><a type="button" class="close" data-dismiss="modal" aria-hidden="true"></a><h4 class="modal-title">Song Upload</h4></div>'
    //                 modal_html += '<div class="modal-body ui-front">Uploading......</div>'
    //                 modal_html += '</div></div></div>'
    //                 $('#helpactive').append(modal_html)
    //                 $('#upload_modal').modal('show')
    //                 upload(input.files[0].name,dataurl,'nomination_form',input.files[0].size)
    //                 $input.wrap('<form>').closest('form').get(0).reset();
    //         		$input.unwrap();   
    //             }
    //             reader.readAsDataURL(file);
    //         });
    //         window.file_reading = false;
    //     }
    // })
    $('input[name="parent_mem_id"]').change(function(){
    	frappe.call({
    		method: "gscommunity.gscommunity.web_form.participant_form.participant_form.check_user",
        	args: {
            	member: $('input[name="parent_mem_id"]').val()
        	},
        	callback:function(data){
        		if(data.message!=undefined){
        			$('input[name=parent_name]').val(data.message.member_name)
        			$('input[name=parent_name]').attr('disabled',true)
        		}else{
        			frappe.msgprint('Invalid Member Id','Alert')
        			$('input[name="parent_mem_id"]').val('')
        		}
        	}
    	})
    })
})

function check_user() {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.check_user",
        args: {
            member: getCookie('member_id')
        },
        callback: function(data) {
            if (data.message != undefined) {
                $('input[name="member"]').val(data.message.name)
                $('input[name="member_name"]').val(data.message.member_name)
                $('input[name="email"]').val(data.message.email)
                $('input[name="mobile_number"]').val(data.message.phone_no)
                $('input[name=member]').attr('disabled', true)
                $('input[name=member_name]').attr('disabled', true)
                if ($('input[name="email"]').val() != '')
                    $('input[name=email]').attr('disabled', true)
                if ($('input[name="mobile_number"]').val() != '')
                    $('input[name=mobile_number]').attr('disabled', true)
            }
        }
    })
}

function get_election_info(election, filetype) {
    frappe.call({
        method: 'gscommunity.gscommunity.doctype.election_nominations.election_nominations.get_election_detail',
        args: {
            election: election
        },
        callback: function(data) {
            if (data.message.designation.length > 0) {
                var html = '<option value selected="selected"></option>'
                for (var i = 0; i < data.message.designation.length; i++) {
                    var designation = data.message.designation[i]
                    html += '<option value="' + designation + '">' + designation + '</option>'
                }
                $('#election_nomination_choice tbody tr select[name=designation]').html(html)
            }
            if (data.message.election != undefined) {
                var election = data.message.election;
                if (election.require_parent_name != 1) {
                    $('div[data-label="Parent Info"]').hide()
                } else {
                    $('div[data-label="Parent Info"]').show()
                    $('input[name="parent_mem_id"]').attr('data-reqd',1)
                    $('input[name=parent_mem_id]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                    $('input[name="parent_name"]').attr('data-reqd',1)
                    $('input[name=parent_name]').parent().find('label').append(' <span class="reqd_field">*</span>') 
                }
                if (election.acknowledgement_title != '' && election.acknowledgement_title) {
                    var ack_title = '<label class="control-label text-muted small">' + election.acknowledgement_title + '</label>'
                    $('div[data-label="Acknowledgement Title"]').html(ack_title)
                }
                if (election.acknowledgement != '' && election.acknowledgement != null) {
                    var ack = '<div>' + election.acknowledgement + '</div>'
                    $('div[data-label="Acknowledgement Info"]').html(ack)
                }
                if (election.signature_required == "Parent") {
                    $('div[data-label=Acknowledgement] input[name="signature"]').parent().find('label').text('Parent Signature')
                }
                if (election.max_choice == 2) {
                    // $('#election_nomination_choice tbody tr:last select[name=choice_type] option[value="Third Choice"]').remove()
                    if (filetype == 'new=1') {
                        $('#election_nomination_choice tbody tr:last td:last').hide()
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').attr('disabled', true)
                        $('#election_nomination_choice thead tr td:last').hide()
                        var otr_html = '<tr class="web-form-grid-row" data-name data-child-row="1">'
                        var html = $('#election_nomination_choice tbody tr:last').html()
                        otr_html = otr_html + html + '</tr>'
                        $('#election_nomination_choice tbody').append(otr_html)
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').val('First Choice')
                        $('#election_nomination_choice tbody').append(otr_html)
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').val('Second Choice')
                        $('button[data-fieldname="election_nomination_choice"]').hide()
                    }
                } else {
                    if (filetype == 'new=1') {
                        $('#election_nomination_choice tbody tr:last td:last').hide()
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').attr('disabled', true)
                        $('#election_nomination_choice thead tr td:last').hide()
                        var otr_html = '<tr class="web-form-grid-row" data-name data-child-row="1">'
                        var html = $('#election_nomination_choice tbody tr:last').html()
                        otr_html = otr_html + html + '</tr>'
                        $('#election_nomination_choice tbody').append(otr_html)
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').val('First Choice')
                        $('#election_nomination_choice tbody').append(otr_html)
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').val('Second Choice')
                        $('#election_nomination_choice tbody').append(otr_html)
                        $('#election_nomination_choice tbody tr:last select[name=choice_type]').val('Third Choice')
                        $('button[data-fieldname="election_nomination_choice"]').hide()
                    }
                }
                if (election.election_form != null) {
                    var form = '<p class="info-msg">You can download the nomination form <a href="' + election.election_form + '">Here</a>.<br>Kindly fill the form and upload here before you submit the document.</p>'
                    $('div[data-label="Nomination Form Link"]').html(form)
                } else {
                    $('div[data-label="Nomination Form"]').hide()
                }
            }
            if (data.message.terms != undefined) {
                var terms = data.message.terms;
                var terms_html = '<ul style="list-style:none">'
                for (var i = 0; i < terms.length; i++) {
                    terms_html += '<li style="display:flex"><i class="fa fa-check"></i> <p>' + terms[i].term + '</p></li>'
                }
                terms_html += '</ul>';
                $('div[data-label="Terms"]').html(terms_html)
            } else {
                $('input[data-label="I hereby agree to all the terms and conditions mentioned here"]').parent().parent().parent().hide()
            }
        }
    })
}

function upload(name,dataurl, docfield,size) {
    frappe.call({
        method: "uploadfile",
        args: {
            from_form: 1,
            doctype: 'Election Nominations',
            // docname: docname,
            is_private: 0,
            filename: name,
            file_url: '',
            filedata: dataurl,
            file_size: size,
            docfield: docfield
        },
        freeze: true,
        callback: function(data) {
            if(docfield=='signature')
            	$('input[data-label="Sign Name"]').val(data.message.name)
            else
            	$('input[data-label="Form Name"]').val(data.message.name)
            $('#upload_modal').modal('hide')                     
        }
    })
}
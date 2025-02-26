frappe.ready(function() {
    var part_form = frappe.web_form_doctype;
    var docname = frappe.doc_name;
    var objectUrl;
    var name = $('h1').text();
    var pathname = decodeURIComponent(window.location.href);
    var url = ''
    var newFile = ''
    var event = ''
    var competition = '';
    var songlimit = 0;
    if (pathname.includes('?')) {
        url = pathname.split('?')[1];
        newFile = url.split('&')[0];
        event = url.split('&')[1];
        competition = url.split('&')[2];
    }
    if(newFile=='new=1' && event!='')
        event=event.split('=')[1];
    var print_btn='<a style="float: right;margin-top: -2%;" href="/api/method/frappe.utils.print_format.download_pdf?doctype=Team&name='+$('#docname').val()+'&format=Team&no_letterhead=0">Print</a>'    
    $('#doctitle').append(print_btn)
    $('.btn-form-submit').text("Save");
    $('.btn-form-saveonly').hide();
    $('div[data-fieldname=table_11]').parent().find('button[data-fieldname=table_11]').hide()
    $('div[data-fieldname=table_7]').parent().find('button[data-fieldname=table_7]').hide()
    $('#table_11 tbody tr td input[data-fieldname="whatsapp_number"]').attr('maxlength', '10')
    var colorHtml = '';
    var user = getCookie('member_id');
    search();   

    $('table').parent().parent().find('.btn').css('margin-bottom', '15px')
    if (newFile == 'new=1') {
        // $('input[name=song]').parent().parent().parent().parent().hide();
        // $('input[name=song_duration]').parent().parent().hide();
        $('input[name=status]').val('Waiting for approval')
        $('input[name=status]').parent().hide();
        // $('#table_15').parent().parent().parent().parent().hide();
        // var html = '<div class="save_txt"><p class="info-msg">Please save the document to upload the file.</p></div>';
        // $('input[name=song]').parent().parent().parent().parent().parent().append(html)
    }
    var song_format='<div class="col-md-12"><div class="info-msg"><p>You can upload only <b>.mp3, .wav, .m4a, .aac</b> file formats.</p></div></div>';
    $('div[data-label="Songs"] .row').prepend(song_format)
    if (newFile == 'new=1' && user != 'Guest') {
        frappe.call({
            method: "gscommunity.gscommunity.web_form.participant_form.participant_form.get_upcoming_events",
            args: {

            },
            async:false,
            callback: function(data) {
                var html = '<option value="" selected="selected"></option>'
                $.each(data.message, function(key, value) {
                    html += '<option value="' + value + '">' + value + '</option>'
                })
                $('select[name=events]').html(html)
                if (event != '') {
                    // event = event.split('=')[1]
                    $('select[name=events]').val(event)
                    $('select[name=events]').prop('disabled', true)
                    $('select[name=events]').parent().hide();
                    var heading = $('#doctitle h4').text();
                    $('h4').text(event + ' - ' + heading)
                }
                if (competition != '') {
                    $('select[name=competition]').val(competition.split('=')[1].replace(/%20/g, ' '))
                    $('select[name=competition]').prop('disabled', true)
                    $('select[name=competition]').parent().hide();
                }
            }
        });
    } else {
        $('select[name=events]').prop('disabled', true)
        $('select[name=competition]').prop('disabled', true)
    }
    if (user != '') {
        get_current_user(newFile);
        get_members();
        if(newFile=='new=1')
            event=event
        else
            event=$('select[name="events"]').val()
        frappe.call({
            method: "gscommunity.gscommunity.web_form.participant_form.participant_form.get_hall_color",
            args: {
                events: event
            },
            callback: function(data) {
                if (data.message != 'All') {
                    colorHtml = '<option value="" selected="selected"></option>'
                    $.each(data.message, function(key, value) {
                        colorHtml += '<option value="' + value + '">' + value + '</option>'
                    })

                    $('#table_15 thead tr th:eq(3)').hide()
                    $('#table_15 tbody tr').each(function() {
                        $(this).find('td:eq(3)').hide()
                    })
                } else {
                    $('#table_15 thead tr th:eq(2)').hide()
                    $('#table_15 tbody tr').each(function() {
                        $(this).find('select').hide()
                        var html = '<input type="text" class="form-control" name="color_code" data-fieldname="color_code" data-label="Color Code" data-fieldtype="Data" data-doctype="Song Background">'
                        $(this).find('td:eq(2)').hide()
                    })
                    var table_html = $('div[data-fieldname="table_15"]').html()
                    var color_text = '<div class="info-msg"><p>You can refer color code from <a target="_blank" href="https://www.w3schools.com/colors/colors_picker.asp">here</a></p>'
                    color_text += '<p>You can copy the color code and paste it in the field below. eg: #ffffff</p></div><br>'
                    $('div[data-fieldname="table_15"]').html(color_text + table_html)
                }
            }
        });
    }
    var tab_len = 0;
    $('#table_11 tbody tr').each(function() {
        $(this).attr('id', tab_len)
        $(this).find('select[name=member]').attr('disabled', true)
        var ph = $(this).find('input[name="whatsapp_number"]').val();
        if (ph != '' && ph != null) {
            $(this).find('input[name="whatsapp_number"]').attr('disabled', true)
        } else {
            $(this).find('input[name="whatsapp_number"]').attr('onchange', 'validate_ph(' + tab_len + ')')
        }
        tab_len = tab_len + 1
    })
    $('#table_7 tbody tr').each(function() {
        $(this).find('select[name=member]').attr('disabled', true)
    })
    var status = $('input[name="status"]').val();
    if (status == 'Finalized' || status == 'Rejected') {
        $('select[name="age_group"]').attr('disabled', true)
        $('input[name="song_title"]').attr('disabled', true)
        $('div[data-label="Managing Team"] #search').hide()
        $('div[data-label="Participants"] #search').hide()
        $('#table_11 tbody tr').each(function() {
            $(this).find('select[name="member_type"]').attr('disabled', true)
            $(this).find('input[name="whatsapp_number"]').attr('disabled', true)
            $(this).find('.btn-remove').parent().hide()
        })
        $('#table_7 tbody tr').each(function() {
            $(this).find('select[name="prize_type"]').attr('disabled', true)
            $(this).find('.btn-remove').parent().hide()
        })
        $('button.change-attach').hide()
        $('#table_15 tbody tr').each(function() {
            $(this).find('input[name="from_time"]').attr('disabled', true)
            $(this).find('input[name="to_time"]').attr('disabled', true)
            $(this).find('select[name="color"]').attr('disabled', true)
            $(this).find('input[name="color_code"]').attr('disabled', true)
            $(this).find('.btn-remove').parent().hide()
        })
        $('#table_11 thead tr th:last').hide()
        $('#table_7 thead tr th:last').hide()
        $('#table_15 thead tr th:last').hide()
        $('button[data-fieldname="table_15"]').parent().hide()
        $('.submit_btns').hide()
    }
    $('input[type=file]').parent().css('margin-bottom','50px')
    var html = '<button onclick="save_image()" class="btn btn-warning" style="float: left;margin-top: 5px;">Upload File</button><audio style="display:none" id="audio"></audio>';
    $('input[type=file]').parent().append(html)
    $("#audio").on("canplaythrough", function(e) {
        var seconds = e.currentTarget.duration;
        var duration = moment.duration(seconds, "seconds");
        var time = "";
        var hours = duration.hours();
        if (hours > 0) { time = hours + ":"; }
        time = time + duration.minutes() + ":" + duration.seconds();
        $("input[name=song_duration]").val(time);
        URL.revokeObjectURL(objectUrl);
        frappe.call({
            method: "gscommunity.gscommunity.web_form.participant_form.participant_form.get_competition",
            args: {
                name: $('select[name=competition] option:selected').val()
            },
            callback: function(data) {
                var mins = data.message.performance_duration.split(':')[0];
                var secs = data.message.performance_duration.split(':')[1];
                var song_mins = $("input[name=song_duration]").val().split(':')[0];
                var song_secs = $("input[name=song_duration]").val().split(':')[1];
                if (parseInt(mins) == parseInt(song_mins)) {
                    if (parseInt(song_secs) > parseInt(secs)) {
                        frappe.msgprint('Please attach file less than ' + mins + ':' + secs + ' minutes')
                        $('input[type=file]').val(null)
                        $("input[name=song_duration]").val('');
                        songlimit = 1
                    }
                } else if (parseInt(mins) < parseInt(song_mins)) {
                    frappe.msgprint('Please attach file less than ' + mins + ':' + secs + ' minutes')
                    $('input[type=file]').val(null)
                    $("input[name=song_duration]").val('');
                    songlimit = 1
                }
            }
        });
    });
    $('input[name=song]').change(function(e) {
        var file = e.currentTarget.files[0];
        objectUrl = URL.createObjectURL(file);
        $("#audio").prop("src", objectUrl);
        var $input = $(this);
        var input = $input.get(0);
        // if (input.files.length) {
        //     input.filedata = { "files_data": [] }; //Initialize as json array.
        //     window.file_reading = true;
        //     var dataurl = '';
        //     $.each(input.files, function(key, value) {
        //         var name = value.name;
        //         var reader = new FileReader();
        //         var docname = $('#docname').val()
        //         console.log(docname)
        //         reader.onload = function(e) {
        //             dataurl = reader.result;
        //             var modal_html='<div id="upload_modal" class="modal fade" style="overflow: auto; display: block; padding-right: 17px;" tabindex="-1"><div class="modal-dialog"><div class="modal-content">';
        //             modal_html+='<div class="modal-header"><a type="button" class="close" data-dismiss="modal" aria-hidden="true"></a><h4 class="modal-title">Song Upload</h4></div>'
        //             modal_html+='<div class="modal-body ui-front">Uploading......</div>'
        //             modal_html+='</div></div></div>'
        //             $('#helpactive').append(modal_html)
        //             $('#upload_modal').modal('show')                 
        //             frappe.call({
        //                 method: "uploadfile",
        //                 args: {
        //                     from_form: 1,
        //                     doctype: 'Team',
        //                     docname: docname,
        //                     is_private: 0,
        //                     filename: input.files[0].name,
        //                     file_url: '',
        //                     filedata: dataurl,
        //                     file_size: input.files[0].size,
        //                     docfield: 'song'
        //                 },
        //                 freeze: true,
        //                 callback: function(data) {
        //                     console.log(data)
        //                     var song_duration = $("input[name=song_duration]").val();
        //                     if (data.message) {
        //                         if (songlimit == 0) {
        //                             frappe.call({
        //                                 method: "gscommunity.gscommunity.web_form.participant_form.participant_form.save_duration",
        //                                 args: {
        //                                     doctype: 'Team',
        //                                     docname: docname,
        //                                     docfield: 'song',
        //                                     duration: song_duration,
        //                                     file_name: data.message.file_url
        //                                 },
        //                                 callback: function(data) {
        //                                     // $('input[type=file]').val(null)
        //                                     $input.wrap('<form>').closest('form').get(0).reset();
        //                                     $input.unwrap();
        //                                     $('#upload_modal').modal('hide') 
        //                                     frappe.msgprint('Your file uploaded successfully')
        //                                 }
        //                             });
        //                         } else {
        //                             frappe.call({
        //                                 method: "gscommunity.gscommunity.web_form.participant_form.participant_form.remove_file",
        //                                 args: {
        //                                     doctype: 'Team',
        //                                     docname: docname,
        //                                     file_name: data.message.file_name
        //                                 },
        //                                 callback: function(data) {
        //                                     $('#upload_modal').modal('hide')       
        //                                     $input.wrap('<form>').closest('form').get(0).reset();
        //                                     $input.unwrap();
        //                                 }
        //                             });
        //                         }
        //                     }
        //                 }
        //             })
        //         }
        //         reader.readAsDataURL(file);
        //     });
        //     window.file_reading = false;
        // }
    })
    $('select[name=event]').on('change', function() {
        var events = $('select[name=events] option:selected').val();
        frappe.call({
            method: "gscommunity.gscommunity.web_form.participant_form.participant_form.get_event_related_competition",
            args: {
                events: events
            },
            callback: function(data) {
                var html = '<option value="" selected="selected"></option>'
                if (data.message != undefined) {
                    for (var i = 0; i < data.message.length; i++) {
                        html += '<option value="' + data.message[i].name + '">' + data.message[i].name + '</option>'
                    }
                }
                $('select[name=competition]').html(html)
            }
        });
    })
    $('button[data-fieldname=table_11]').click(function() {
        var table_length = $("#table_11 tbody tr").length;
        var id = 'member-' + table_length;
        $('#table_11 tbody tr:last').attr('id', table_length)
        $('#table_11 tbody tr:last select').attr('onchange', 'getMemberData(' + table_length + ')')
        $('#table_11 tbody tr:last input[name="whatsapp_number"]').attr('onchange', 'validate_ph(' + table_length + ')')
    })
    $('button[data-fieldname=table_7]').click(function() {
        var table_length = $("#table_7 tbody tr").length;
        var id = 'member-' + table_length;
        $('#table_7 tbody tr:last').attr('id', table_length)
        $('#table_7 tbody tr:last select').attr('onchange', 'getMemberData1(' + table_length + ')')
    })
    $('button[data-fieldname=table_15]').click(function() {
        $('#table_15 tbody tr:last select').html(colorHtml)
    })
    
    $("#managing_member").catcomplete({
        delay: 150,
        autoFocus: true,
        source: function(request, response) {
            frappe.call({
                method: "gscommunity.gscommunity.web_form.participant_form.participant_form.member_search",
                args: {
                    start: 0,
                    limit: 20,
                    text: request.term
                },
                callback: function(r) {
                    var bty = []
                    $.each(r.message, function(key, value) {
                        var item = '';                   
                        var family=''
                        if(value.family){
                            for(var j=0;j<value.family.length;j++){
                                family+=value.family[j];
                                if(j!=value.family.length)
                                    family+=', '
                            }
                        }                      
                        item = value.first_name + ' ' + value.last_name +' ('
                        if(family!='')
                            item+='Family Members: '+family+' - '
                        item+=value.address+')'
                        bty.push({
                            label: item,
                            value: item,
                            content: value.name
                        })
                    })
                    response(bty)
                }
            });

        },
        minLength: 2,
        select: function(event, ui) {
            var html = $('#table_11 tbody tr[data-child-row="1"]').html();
            var length = $('#table_11 tbody tr').length;
            var otr_html = '<tr class="web-form-grid-row" data-name data-child-row="1" id="' + length + '">';
            otr_html += html + '</tr>';
            $('#table_11 tbody').append(otr_html)
            $('#table_11 tbody tr:last select[name=member]').attr('onchange', 'getMemberData(' + length + ')')
            $('#table_11 tbody tr:last select[name=member]').val(ui.item.content)
            $('#table_11 tbody tr:last select[name=member]').attr('disabled', true)
            getMemberData(length)
            $('#managing_member').val(null)
            return false;
        }
    });

    $("#participant_search").catcomplete({
        delay: 150,
        autoFocus: true,
        source: function(request, response) {
            frappe.call({
                method: "gscommunity.gscommunity.web_form.participant_form.participant_form.member_search",
                args: {
                    start: 0,
                    limit: 20,
                    text: request.term
                },
                callback: function(r) {
                    var bty = []
                    $.each(r.message, function(key, value) {
                        var item = '';
                        var family=''
                        if(value.family){
                            for(var j=0;j<value.family.length;j++){
                                family+=value.family[j];
                                if(j!=value.family.length)
                                    family+=', '
                            }
                        }                      
                        item = value.first_name + ' ' + value.last_name +' ('
                        if(family!='')
                            item+='Family Members: '+family+' - '
                        item+=value.address+')'
                        bty.push({
                            label: item,
                            value: item,
                            content: value.name
                        })
                    })
                    response(bty)
                }
            });

        },
        minLength: 2,
        select: function(event, ui) {
            var html = $('#table_7 tbody tr[data-child-row="1"]').html();
            var length = $('#table_7 tbody tr').length;
            var otr_html = '<tr class="web-form-grid-row" data-name data-child-row="1" id="' + length + '">';
            otr_html += html + '</tr>';
            $('#table_7 tbody').append(otr_html)
            $('#table_7 tbody tr:last select[name=member]').attr('onchange', 'getMemberData1(' + length + ')')
            $('#table_7 tbody tr:last select[name=member]').val(ui.item.content)
            $('#table_7 tbody tr:last select[name=member]').attr('disabled', true)
            getMemberData1(length)
            $('#participant_search').val(null)
            return false;
        }
    })
    $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').on('change', function() {
        var number = $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').val();
        if (number != '') {
            if (!validate_number(number)) {
                frappe.msgprint('Please enter 10 digit numeric value for whatsapp number', 'Alert')
                $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').val('');
            }
            if (number.length != 10) {
                frappe.msgprint('Please enter 10 digit numeric value for whatsapp number', 'Alert')
                $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').val('');
            }
        }
    })    
})

function getMemberData(length) {
    var member = $("#table_11 #" + length + " select[name=member] option:selected").val();
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.getMember_details",
        args: {
            name: member
        },
        callback: function(data) {
            var checked = 'InActive';
            if (data.message.active) {
                checked = 'Active'
                $("#table_11 #" + length + " input[name=member_name]").val(data.message.member_name)
                $("#table_11 #" + length + " input[name=whatsapp_number]").val(data.message.mobile_no)
                $("#table_11 #" + length + " input[name=email]").val(data.message.email)
                $("#table_11 #" + length + " input[name=active]").val(checked)
            } else {
                if (confirm('Member ' + member + ' - ' + data.message.member_name + ' is not active. Do you still want to proceed?')) {
                    $("#table_11 #" + length + " input[name=member_name]").val(data.message.member_name)
                    $("#table_11 #" + length + " input[name=whatsapp_number]").val(data.message.mobile_no)
                    $("#table_11 #" + length + " input[name=email]").val(data.message.email)
                    $("#table_11 #" + length + " input[name=active]").val(checked)
                } else {
                    $("#table_11 #" + length + " select[name=member] option:selected").val('');
                    $('#table_11 #' + length).remove()
                }
            }
            if (data.message.mobile_no != '' && data.message.mobile_no != null) {
                $("#table_11 #" + length + " input[name=whatsapp_number]").attr('disabled', true)
            } else {
                $("#table_11 #" + length + " input[name=whatsapp_number]").attr('disabled', false)
                $("#table_11 #" + length + " input[name=whatsapp_number]").attr('onchange', 'validate_ph(' + length + ')')
            }
        }
    });
}

function getMemberData1(length) {
    var member = $("#table_7 #" + length + " select[name=member] option:selected").val();
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.getMember_details",
        args: {
            name: member
        },
        callback: function(data) {
            var checked = 'InActive';
            if (data.message.active) {
                checked = 'Active'
                $("#table_7 #" + length + " input[name=member_name]").val(data.message.member_name)
                $("#table_7 #" + length + " input[name=active]").val(checked)
                $('table_7 #' + length + ' select[name="prize_type"]').val('None')
                $('table_7 #' + length + ' select[name="prize_type"]').attr('disabled', true)
            } else {
                if (confirm('Member ' + member + ' - ' + data.message.member_name + ' is not active. If you want to add the member, he cannot get either trophy or certificate. Do you want to proceed?')) {
                    $("#table_7 #" + length + " input[name=member_name]").val(data.message.member_name)
                    $("#table_7 #" + length + " input[name=active]").val(checked)
                    $('table_7 #' + length + ' select[name="prize_type"]').val('None')
                    $('table_7 #' + length + ' select[name="prize_type"]').attr('disabled', true)
                } else {
                    $('#table_7 #' + length).remove()
                }
            }
        }
    });
}

function get_members() {
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.get_members",
        args: {},
        callback: function(data) {
            var html = '<option value="" selected="selected"></option>'
            $.each(data.message, function(key, value) {
                html += '<option value="' + value + '">' + value + '</option>'
            })
        }
    });
}

function getAllMembers(text) {
    var members = []
    frappe.call({
        method: 'gscommunity.gscommunity.web_form.participant_form.participant_form.member_search',
        args: {
            text: text
        },
        callback: function(data) {

        }
    })
}

function search() {
    $.widget("custom.catcomplete", $.ui.autocomplete, {
        _create: function() {
            this._super();
            this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
        },
        _renderMenu: function(ul, items) {
            var that = this,
                currentCategory = "";
            $.each(items, function(index, item) {
                var li;
                li = that._renderItemData(ul, item);
                if (item.category) {
                    li.attr("aria-label", item.category + " : " + item.label);
                }
            });
        }
    });
}

function get_current_user(newFile) {
    var user = getCookie('member_id');
    frappe.call({
        method: "gscommunity.gscommunity.web_form.participant_form.participant_form.check_user",
        args: {
            member: user
        },
        callback: function(data) {
            $('input[data-fieldname="None"]').val('')
            $('input[data-label="First Name"]').val(data.message.member_name)
            $('input[data-label="Last Name"]').val(data.message.last_name)
            $('div[data-label="Member Info"] input[data-label="Email"]').val(data.message.email)
            $('input[data-label="Phone"]').val(data.message.phone_no)
            $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').val(data.message.mobile_no)
            if (data.message.mobile_no != '' && data.message.mobile_no != null) {
                $('div[data-label="Member Info"] input[data-label="WhatsApp Number"]').attr('disabled', true)
            }
            var table_html = $('#table_11 tbody').html();
            if (newFile == 'new=1') {
                $('#table_11 tbody').append(table_html)
                $('#table_11 tbody tr:eq(1) select[name=member]').val(data.message.name)
                $('#table_11 tbody tr:eq(1) input[name=member_name]').val(data.message.member_name)
                $('#table_11 tbody tr:eq(1) input[name=email]').val(data.message.email)
                $('#table_11 tbody tr:eq(1) input[name=whatsapp_number]').val(data.message.mobile_no)
                var checked = 'In Active';
                if (data.message.active)
                    checked = 'Active'
                $("#table_11 tbody tr:eq(1) input[name=active]").val(checked)
                $('#table_11 tbody tr:eq(1)').attr('id', 1)
                $('#table_11 tbody tr:eq(1)').removeClass('hidden')
                if (data.message.mobile_no != '' && data.message.mobile_no != null) {
                    $('#table_11 tbody tr:eq(1) input[name=whatsapp_number]').attr('disabled', true)
                }
            } else {
                // $('input[data-label="WhatsApp Number"]').val($('#table_11 tbody tr:eq(1) input[name=whatsapp_number]').val())
            }
        }
    });
}

function validate_ph(length) {
    var ph = $('#table_11 #' + length + ' input[name=whatsapp_number]').val()
    if (ph != '') {
        if (!validate_number(ph)) {
            frappe.msgprint('Please enter 10 digit numeric value for whatsapp number', 'Alert')
            $('#table_11 #' + length + ' input[name=whatsapp_number]').val('');
        }
        if (ph.length != 10) {
            frappe.msgprint('Please enter 10 digit numeric value for whatsapp number', 'Alert')
            $('#table_11 #' + length + ' input[name=whatsapp_number]').val('');
        }
    }
}
var save_image=function(){
    var file=$('input[type=file]').val();
    if(file){
        $('#Nsub').trigger('click')
    }else{
        frappe.msgprint('Please attach any file','Warning')
    }
}
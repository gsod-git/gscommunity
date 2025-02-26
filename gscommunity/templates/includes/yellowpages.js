$(document).ready(function(){
	$.widget("custom.catcomplete", $.ui.autocomplete, {
        _create: function() {
            this._super();
            this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
        },
        _renderMenu: function(ul, items) {
            // console.log(items)
            var that = this,
                currentCategory = "";
            $.each(items, function(index, item) {
                var li;
                // if (item.category != currentCategory) {
                //     ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
                //     currentCategory = item.category;
                // }
                li = that._renderItemData(ul, item);
                if (item.category) {
                    li.attr("aria-label", item.category + " : " + item.label);
                }
            });
        }
    });
    $('#yellowpages_search').catcomplete({
    	delay: 150,
        autoFocus: true,
        source: function(request, response) {
            frappe.call({
                method: "gscommunity.templates.pages.yellowpages.yellowpage_search",
                args: {
                    start: 0,
                    limit: 10,
                    text: request.term
                },
                callback: function(r) {
                    var bty = []
                    if(r.message){
                        $.each(r.message, function(key, value) {
                            var content = value[0].split('|||')
                            var item='';
                            var business_name='';
                            var route='';
                            var category='';
                            var sub_category='';
                            for (var i = 0; i < content.length; i++) {
                                var part=content[i].split(':');                            
                                if(part[0].trim()=='Business Name'){
                                    business_name=part[1];
                                }
                                if(part[0].trim()=='Route'){
                                    route=part[1];
                                }
                                if(part[0].trim()=='Category'){
                                    category=part[1];
                                }
                                if(part[0].trim()=='Sub Category'){
                                    sub_category=part[1];
                                }
                            }
                            item=business_name
                            bty.push({
                                label: item,
                                value: value[1],
                                content: item,
                                route:route
                            })
                        })
                        response(bty)
                    }
                }
            });

        },
        minLength: 2,
        select: function(event, ui) {
            var routing=ui.item.route.trim()
            window.location.href='/'+routing
        }
    })
})
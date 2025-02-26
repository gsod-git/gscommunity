# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "gscommunity"
app_title = "Gscommunity"
app_publisher = "valiantsystems"
app_description = "non profit application"
app_icon = "octicon octicon-file-directory"
app_color = "pink"
app_email = "info@valiantsystems.com"
app_license = "MIT"
fixtures = [
	{
		"dt":"Custom Field",
		"filters":[["name","in",['Email Group-category','Email Group-block_email','Newsletter-generate_newsletter'
		,'Newsletter-components','Newsletter-test_newsletter','Newsletter-template','Newsletter-html_content',
		'User-events_ticket_token','User-token_expires_on','Newsletter-send_later','Newsletter-custom_css',
		'Newsletter-template_section','Newsletter-file_size','Newsletter-scheduled_time',
		'Newsletter-test_email_group','Newsletter-send_test_mail']]]
	},
	{
		"dt":"Print Format",
		"filters":[["name","in",['Sponsorship','Donation','Team']]]
	}
]
on_session_creation = "gscommunity.gscommunity.api.login_member"
# Includes in <head>
# ------------------
update_website_context = "gscommunity.gscommunity.context.update_website_context"

website_route_rules=[
{"from_route":"/login","to_route":"custom_login"},
{"from_route":"/update-password","to_route":"update_password"},
]

# include js, css files in header of desk.html
# app_include_css = "/assets/gscommunity/css/gscommunity.css"
# app_include_js = "/assets/gscommunity/js/gscommunity.js"

# include js, css files in header of web template
# web_include_css = "/assets/gscommunity/css/gscommunity.css"
# web_include_js = "/assets/gscommunity/js/gscommunity.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Email Group" : "public/js/email_group.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "gscommunity.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gscommunity.install.before_install"
# after_install = "gscommunity.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gscommunity.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Email Group": {
		"on_trash": "gscommunity.gscommunity.api.on_deleting_email_group"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"gscommunity.tasks.all"
# 	],
	"daily": [
		"gscommunity.gscommunity.api.validate_expiry_date",
		"gscommunity.gscommunity.api.validate_child_expiry",
		"gscommunity.gscommunity.api.check_subscription_entries"	
	],
	"cron":{
		"0/30 * * * *":[
			"gscommunity.gscommunity.api.schedule_newsletter"
		]
	}
# 	"hourly": [
# 		"gscommunity.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gscommunity.tasks.weekly"
# 	]
#  	"monthly": [
		
# 	]
}

# Testing
# -------

# before_tests = "gscommunity.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gscommunity.event.get_events"
# }


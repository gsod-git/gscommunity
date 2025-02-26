from __future__ import unicode_literals

import frappe

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist(allow_guest=True)
def get_current_user():
	member=frappe.db.get_all("Member",fields=["name"])
	return member
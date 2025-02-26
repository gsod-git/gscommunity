# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Tasks(Document):
	pass

@frappe.whitelist()
def get_members(doctype, txt, searchfield, start, page_len, filters):
	if(filters['task_type']=='Event'):
		return frappe.db.sql('''select m.name from `tabMember` m inner join `tabVolunteer` v
				on m.name=v.member inner join `tabEvent Volunteer` ev on ev.volunteer=v.name
				where m.active=1 and ev.parent=%(event)s'''.format(),{'event':filters['events']})
	else:
		return frappe.db.sql('''select name from `tabMember` where active=1''')

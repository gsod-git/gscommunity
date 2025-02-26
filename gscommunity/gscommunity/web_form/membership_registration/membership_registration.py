from __future__ import unicode_literals

import frappe
from frappe import _, scrub
from frappe.model.document import Document
import datetime
from datetime import date, datetime, timedelta
from frappe.utils import getdate, add_months, add_to_date, nowdate, today

def get_context(context):
	# do your magic here
	# test=frappe.frappe.form_dict.name
	# frappe.msgprint(test)
	context.User=frappe.db.get_all("User",fields=["name"], filters={"owner":frappe.session.user})
	

@frappe.whitelist(allow_guest=True)
def get_current_user():
	member=frappe.db.get_all("Member",fields=["name"], filters={"owner":frappe.session.user})
	return member

@frappe.whitelist(allow_guest=True)
def add_relationgroup(doctype, txt, searchfield, start, page_len, filters):
	if filters.get('relation'):
		return frappe.db.sql("""select parent from `tabRelations`
			where  relationship = %(relation)s and parent like %(txt)s and relationship !="Self" {match_cond}
			order by
				if(locate(%(_txt)s, parent), locate(%(_txt)s, parent), 99999),
				idx desc,
				`tabRelations`.parent asc
			limit {start}, {page_len}""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {
					"txt": "%{0}%".format(txt),
					"_txt": txt.replace('%', ''),
					"relation": filters['relation']
				})

@frappe.whitelist(allow_guest=True)
def get_rolecount(relation):
	Group = frappe.db.get_all('Members Validation',fields=['relationship','allowed_members','age_limit'], filters={'parent':relation})
	return Group	

@frappe.whitelist(allow_guest=True)
def get_age_limit(age_limit,relation,parent):
	# Group = frappe.db.get_all('Members Validation',fields=['relationship','allowed_members','age_limit'], filters={'parent':relation})
	# return Group
	condition = ""

	Employee = frappe.db.sql("""select relationship, allowed_members, age_limit from `tabMembers Validation` where relationship=%(relation)s and parent=%(parent)s and age_limit >= %(age_limit)s""".format(condition), 
				{"relation":relation,"parent":parent,"age_limit":age_limit}, as_dict=1)	
	return Employee

@frappe.whitelist(allow_guest=True)
def add_relation(doctype, txt, searchfield, start, page_len, filters):
	if filters.get('relationship_group'):
		return frappe.db.sql("""select relationship from `tabRelations`
			where  parent = %(relationship_group)s and relationship like %(txt)s {match_cond}
			order by
				if(locate(%(_txt)s, relationship), locate(%(_txt)s, relationship), 99999),
				idx desc,
				`tabRelations`.relationship asc
			limit {start}, {page_len}""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {
					"txt": "%{0}%".format(txt),
					"_txt": txt.replace('%', ''),
					"relationship_group": filters['relationship_group']
				})
@frappe.whitelist(allow_guest=True)
def get_email_group(category):
	return frappe.db.get_all('Email Group',filters={'category':category})

@frappe.whitelist(allow_guest=True)
def get_recurring_payment_details(doctype,parent):
	result=frappe.db.get_all('Recurring Payments',fields=['*'],
		filters={'parenttype':doctype,'parent':parent})
	if result:
		return result
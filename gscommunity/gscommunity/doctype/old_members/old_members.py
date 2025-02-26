# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import getdate, nowdate
from datetime import date, datetime, time

class OldMembers(Document):
	def validate(self):
		if self.table_25:
			for item in self.table_25:
				if not item.relationship_group:
					relation=frappe.db.get_all('Relations',fields=['parent'],filters={'relationship':item.relation})
					if relation:
						item.relationship_group=relation[0].parent

@frappe.whitelist()
def get_relation_ship_group(relation):
	relations=frappe.db.get_all('Relations',fields=['parent'],filters={'relationship':relation})
	if relations:
		relationship_group=relations[0].parent
		return relationship_group


@frappe.whitelist()
def add_members(names, action=None):
	if json.loads(names):	
		for name in json.loads(names or []):	
			old_member=frappe.get_doc('Old Members',name)
			if not old_member.email:
				frappe.throw(frappe._('{0} does not have email id.'))
			member_info=frappe.db.get_all('Member',filters={'old_member_id':old_member.member_id})
			if not member_info:
				result= frappe.get_doc({
					"doctype":"Member",
					"member_name":old_member.member_name,
					"email":old_member.email,
					"phone_no":old_member.phone_no,
					"membership_type":old_member.membership_type,
					"address_line_1":old_member.address_line_1,
					"city":old_member.city,
					"zip_code":old_member.zip_code,
					"state":old_member.state,
					"last_name":old_member.last_name,
					"gender":old_member.gender,
					"date_of_birth":old_member.date_of_birth,
					"newsletter":old_member.newsletter,
					"membership_expiry_date":old_member.membership_expiry_date,
					"old_member_id":old_member.member_id,
					"active":old_member.active,
					"membership_amount":old_member.membership_amount,
					"address_line_2":old_member.address_line_2,
					"middle_name":old_member.middle_name,
					"self_relation":"Self"
				}).insert()
				member=frappe.get_last_doc('Member')
				Family=frappe.get_doc('Old Members',old_member.name)
				if Family:
					for item in Family.table_25:
						frappe.get_doc({
							"member_name":item.member_name,
							"last_name":item.last_name,
							"email":item.email,
							"phone_no":item.phone_no,
							"relation":item.relation,
							"date_of_birth":item.date_of_birth,
							"gender":item.gender,
							"newsletter":item.newsletter,
							"doctype":item.doctype,
							"parent": member.name,
							"parentfield": item.parentfield,
							"parenttype": "Member",
							"relationship_group":item.relationship_group,
							"self_relation":item.relation
							}).insert()
				if member.active:
					make_membership_entry(member)
		frappe.msgprint(frappe._('Members have been updated successfully'))
	else:
		frappe.throw(frappe._('Please select any one member'))
@frappe.whitelist()
def make_membership_entry(member):
	now=getdate(nowdate())
	settings=frappe.get_single('General Settings')
	expiry_date=settings.expiry_date
	if settings.membership_type==member.membership_type:
		expiry_date=date(int(now.year)+int(settings.validity),now.month,now.day)
	frappe.get_doc({
		"doctype":"Membership","member":member.name,"membership_status":"Current",
		"membership_type":member.membership_type,"from_date":now,"to_date":expiry_date,
		"paid":1,"amount":member.membership_amount,"docstatus":1}).insert()
	membership=frappe.get_last_doc('Membership')
	account=frappe.get_value('Membership Type', member.membership_type, 'accounting_head')
	frappe.get_doc({
		"doctype":"Payment Entries","payment_date":now,"payment_type":"Credit",
		"payment_for":"Membership","ref_id":membership.name,"member":member.name,
		"paid_amount":membership.amount,"mode_of_payment":"Online Payment",
		"accounting_head":account,"docstatus":1 }).insert()
# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date, datetime, time
from frappe.utils import getdate,nowdate

class ExistingMembers(Document):
	def on_update(self):
		if self.member_id:
			add_as_member(self)

@frappe.whitelist(allow_guest=True)
def add_as_member(self):
	if self.member_id:
		Exist=frappe.db.get_all('Old Members',fields=['*'],filters={'member_id':self.member_id})[0]
		# Exist=frappe.get_doc('Old Members',name)
		if not frappe.db.get_value("Member", Exist.email):
			result= frappe.get_doc({
					"doctype":"Member",
					"member_name":Exist.member_name,
					"email":self.email,
					"phone_no":self.phone_no,
					"membership_type":Exist.membership_type,
					"address_line_1":Exist.address_line_1,
					"city":Exist.city,
					"zip_code":Exist.zip_code,
					"state":Exist.state,
					"last_name":Exist.last_name,
					"gender":Exist.gender,
					"date_of_birth":Exist.date_of_birth,
					"newsletter":Exist.newsletter,
					"membership_expiry_date":Exist.membership_expiry_date,
					"old_member_id":Exist.member_id,
					"active":Exist.active,
					"membership_amount":Exist.membership_amount,
					"address_line_2":Exist.address_line_2,
					"middle_name":Exist.middle_name,
					"self_relation":"Self"
				}).insert()
			member=frappe.get_last_doc('Member')
			Family=frappe.get_doc('Old Members',Exist.name)
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


@frappe.whitelist(allow_guest=True)
def add_user(self):
	if not frappe.db.get_value("User", self.email):
		result= frappe.get_doc({
		"doctype": "User",
		"email": self.email,
		"first_name": self.member_name,
		"mobile_no":self.phone_no,
		"send_welcome_email":1
		}).insert()
		add_parentrole(self)
		return result

@frappe.whitelist(allow_guest=True)
def add_parentrole(self):
	result= frappe.get_doc({
		"doctype": "Has Role",
		"name": nowdate(),
		"parent": self.email,
		"parentfield": "roles",
		"parenttype": "User",
		"role": "Member"
		}).insert()
	return result
@frappe.whitelist(allow_guest=True)
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
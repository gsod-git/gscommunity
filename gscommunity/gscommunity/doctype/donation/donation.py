# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate,getdate
import datetime
from datetime import date, datetime, time

class Donation(Document):
	pass
	def on_update(self):
		if self.donate_as_guest:
			if self.full_name and self.email and self.phone:
				add_user(self.full_name,self.email,self.phone,self.last_name)

@frappe.whitelist(allow_guest=True)
def add_newsletter(emailgroup,email):
	if not frappe.db.get_value("Email Group Member", email):
		result= frappe.get_doc({
		"doctype": "Email Group Member",
		"email_group": emailgroup,
		"email": email
		}).insert()
		return result
@frappe.whitelist(allow_guest=True)
def add_user(name,email,phone,last_name):
	if not frappe.db.get_value("User", email):
		result= frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": name,
			"mobile_no":phone,
			"last_name":last_name,
			"send_welcome_email":1
		}).insert()
		add_role(email)
		
@frappe.whitelist(allow_guest=True)
def add_role(email):
	frappe.get_doc({
			"doctype": "Has Role",
			"name": nowdate(),
			"parent": email,
			"parentfield": "roles",
			"parenttype": "User",
			"role": "Web User"
		}).insert()
@frappe.whitelist(allow_guest=True)
def make_payment(docname,email,amount,transaction_id,payment_date=None):
	donation=frappe.db.get_all('Donation',fields=['member','email','donation_amount','donation_for'],filters={'name':docname})	
	if donation:
		donation_category=frappe.db.get_all('Donation Category',fields=['accounting_head'],filters={'name':donation[0].donation_for})[0]
		if not frappe.db.get_value("Payment Entries", docname):
			if donation[0].member:
				frappe.get_doc({
					"doctype": "Payment Entries",
					"payment_date": payment_date if payment_date else getdate(nowdate()),
					"payment_for": "Donation",
					"ref_id": docname,
					"member": donation[0].member,
					"paid_amount":donation[0].donation_amount,
					"mode_of_payment":"Online Payment",
					"docstatus":1,
					"accounting_head":donation_category.accounting_head
				}).insert()
			else:
				frappe.get_doc({
					"doctype": "Payment Entries",
					"payment_date": payment_date if payment_date else getdate(nowdate()),
					"payment_for": "Donation",
					"ref_id": docname,
					"user": donation[0].email,
					"paid_amount":donation[0].donation_amount,
					"mode_of_payment":"Online Payment",
					"docstatus":1,
					"transaction_id":transaction_id,
					"accounting_head":donation_category.accounting_head
				}).insert()
	if frappe.db.get_value("Donation", docname):	
		doc=frappe.get_doc('Donation',docname)
		doc.paid=1
		doc.docstatus=1
		doc.save()
@frappe.whitelist(allow_guest=True)
def get_details(doctype,docname):
	result=frappe.db.get_all(doctype,fields=['*'],filters={'name':docname})
	for data in result:
		if data.member:
			last_name=frappe.db.get_all('Member',fields=['last_name'],filters={'name':data.member})[0]
			data.last_name=last_name.last_name
	return result
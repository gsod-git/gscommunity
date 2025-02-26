# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PaymentEntries(Document):
	pass
	def validate(self):
		payment=frappe.db.get_all('Payment Entries',fields='name'
			,filters={'payment_for':self.payment_for,'ref_id':self.ref_id})
		if payment:
			if(payment[0].name!=self.name):		
				frappe.throw(frappe._('Payment Entry has already made for this transaction'))
		if self.docstatus==1:
			if frappe.db.get_value(self.payment_for, self.ref_id):
				if self.payment_for=='Bookings':
					frappe.db.set_value(self.payment_for, self.ref_id , "booking_status", "Paid")
				elif self.payment_for=='Expense':
					expense_claim=frappe.db.get_all('Expense Claims',filters={'expense_id':self.ref_id})					
					if expense_claim:
						frappe.db.set_value('Expense Claims',expense_claim[0].name,'paid',1)
						expense_claim_list=frappe.db.get_all('Expense Claim List',filters={'parent':self.ref_id,'expense_claims':expense_claim[0].name})
						if expense_claim_list:
							frappe.db.set_value('Expense Claim List',expense_claim_list[0].name,'paid',1)
				else:
					frappe.db.set_value(self.payment_for, self.ref_id , "paid", 1)			

@frappe.whitelist()
def get_doctype(doctype, txt, searchfield,filters, start=0, page_len=50):
	doctypes=frappe.db.sql('''select name from `tabDocType` where module like "Gscommunity" 
		and is_submittable=1 and name!=%(name)s'''.format(),{"name":txt})
	return doctypes

@frappe.whitelist()
def get_docnames(doctype):
	return frappe.db.get_all(doctype,fields='name')

@frappe.whitelist()
def get_payment_entry(doctype,ref_id):
	name=frappe.db.get_all('Payment Entries',fields='name'
		,filters={'payment_for':doctype,'ref_id':ref_id})
	return name

@frappe.whitelist()
def get_member(doctype, txt, searchfield,filters, start=0, page_len=50):	
	return frappe.db.sql("""select member from `tab%(doctype)s`
			where name = %(name)s""".format(),{
			"doctype":filters['doctype'],
			"name":filters['docname']
			})
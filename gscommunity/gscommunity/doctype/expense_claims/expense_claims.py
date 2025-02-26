# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExpenseClaims(Document):
	def on_submit(self):
		if self.status=='Approved':			
			result= frappe.get_doc({
				"doctype": "Expense","accounting_group": self.accounting_group,
				"accounting_category": self.accounting_category,"events":self.events,
				"category":self.category,"member":self.member,"member_name":self.member_name,
				"date":self.date,"amount":self.sanctioned_amount,
				"vendor":self.vendor,"docstatus":1
			}).insert()
			expense=frappe.get_last_doc('Expense')
			frappe.db.set_value('Expense Claims',self.name,'expense_id',expense.name)
			frappe.get_doc({
				"doctype":"Expense Claim List","expense_claims":self.name,"expense_date":self.date,
				"paid":self.paid,"parent":expense.name,"parentfield":"expense_claim_list","parenttype":"Expense"
			}).insert()

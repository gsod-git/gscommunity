# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.desk.reportview import get_match_cond, get_filters_cond

class BudgetIncomeAndExpense(Document):
	def autoname(self):
		self.name='Budget '+self.fiscal_year
	def on_update(self):
		income=0
		expense=0
		if self.table_4:
			for data in self.table_4:
				income=income+data.budget_income
				expense=expense+data.budget_expense
		self.total_budget_income=income
		self.total_budget_expense=expense

@frappe.whitelist()
def get_eventlist(doctype, txt, searchfield,filters, start=0, page_len=50):
	return frappe.db.sql("""select name from `tabEvents`
		where event_type = %(event_type)s			
		""".format(
			match_cond=get_match_cond(doctype),
			start=start,
			page_len=page_len), {					
				"event_type": filters['category']
			})
@frappe.whitelist()
def get_accounting_category(doctype, txt, searchfield,filters, start=0, page_len=50):
	result=frappe.db.sql('''select name from `tabAccounting Category` where accounting_group=%(group)s'''
		.format(),{'group':txt})
	return result
# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		_("Accounting Group") + ":Data:120",
		_("Accounting Category") + ":Data:200",
		_("Budget Income ($ - USD)")+ ":Float:140",
		_("Budget Expense ($ - USD)") + ":Float:140", 
		_("Actual Income ($ - USD)") + ":Float:140",
		_("Actual Expense ($ - USD)") + ":Float:140",
		_("Profit/Loss ($ - USD)") + ":Float:130"
	]

def get_data(filters):
	budget=frappe.db.get_all('Budget Income And Expense',fields=['name','fiscal_year'],filters={'fiscal_year':filters.year})
	data=[]
	for item in budget:
		budget_list=frappe.db.sql("""select * from `tabBudget Details` where parent=%(name)s order by accounting_group,idx""".format(), 
				{"name":item.name}, as_dict=1)
		group=frappe.db.sql('''select distinct accounting_group from `tabBudget Details` order by accounting_group''',as_dict=1)
		if budget_list:
			t_b_income=0
			t_b_expense=0
			t_income=0
			t_expense=0
			t_profit=0
			for item in group:
				lists=[]
				group=item.accounting_group
				lists.append('<b>'+item.accounting_group+'</b>')
				data.append(lists)
				b_income=0
				b_exp=0
				inc=0
				exp=0
				profitloss=0			
				for b_list in budget_list:
					if b_list.accounting_group==group:			
						content=[]						
						content.append('')
						content.append(b_list.accounting_category)
						content.append(b_list.budget_income)
						content.append(b_list.budget_expense)
						actual_income=frappe.db.sql('''select sum(paid_amount) from `tabPayment Entries` where accounting_head=%(head)s and year(payment_date)=%(year)s and payment_type="Credit"'''
							.format(),{'head':b_list.accounting_category,'year':filters.year})
						actual_expense=frappe.db.sql('''select sum(paid_amount) from `tabPayment Entries` where accounting_head=%(head)s and year(payment_date)=%(year)s and payment_type="Debit"'''
							.format(),{'head':b_list.accounting_category,'year':filters.year})
						profit=0
						income=0
						expense=0
						for item in actual_income:
							if item[0]!=None:
								income=item[0]
						for item in actual_expense:					
							if item[0]!=None:
								expense=item[0]
						profit=income-expense
						b_income=b_income+b_list.budget_income
						b_exp=b_exp+b_list.budget_expense
						inc=inc+income
						exp=exp+expense
						profitloss=profitloss+profit
						content.append(income)
						content.append(expense)
						content.append(profit)				
						data.append(content)
				totals=[]
				totals.append('<b>Total</b>')
				totals.append('')
				totals.append(b_income)
				totals.append(b_exp)
				totals.append(inc)
				totals.append(exp)
				totals.append(profitloss)
				data.append(totals)
				t_profit=t_profit+profitloss
				t_expense=t_expense+exp
				t_income=t_income+inc
				t_b_expense=t_b_expense+b_exp
				t_b_income=t_b_income+b_income
			grand_total=[]
			grand_total.append('<b>Grand Total</b>')
			grand_total.append('')
			grand_total.append(t_b_income)
			grand_total.append(t_b_expense)
			grand_total.append(t_income)
			grand_total.append(t_expense)
			grand_total.append(t_profit)
			data.append(grand_total)				
	return data


@frappe.whitelist()
def get_years():
	year_list = frappe.db.sql_list('''select fiscal_year from `tabBudget Income And Expense` ORDER BY fiscal_year DESC''')
	if not year_list:
		year_list = [getdate().year]
	return "\n".join(str(year) for year in year_list)

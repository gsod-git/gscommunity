# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from gscommunity.gscommunity.doctype.event_survey.event_survey import get_response

def execute(filters=None):
	if not filters: filters = {}
	columns=get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	return [
		("Survey Question") + ":Data:300",
		("Options") + ":Data:200",
		("No. of Responses") + ":Int:100",
		("Response Percentage") + ":Float:120"
	]

def get_data(filters):
	data=[]
	response=get_response(filters.event_survey)
	if response:
		for item in response:
			content=[]
			content.append(item.question_name)
			data.append(content)
			for opts in item.options:
				con=[]
				con.append('')
				con.append(opts.options)
				con.append(opts.response_count)				
				if item.total_response>0:
					percent=(int(opts.response_count)/int(item.total_response))*100
					con.append(round(percent,2))
				else:
					con.append(round(0,2))
				data.append(con)
	return data
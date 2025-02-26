# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ElectionNominations(Document):
	pass
	def on_update(self):
		lists=frappe.db.get_all('Election Nominations',fields=['name'],filters={'member':self.member,'election':self.election})
		if lists:
			for item in lists:
				if item.name!=self.name:
					frappe.throw(frappe._('Only one nomination form can be submitted by a single member'))

@frappe.whitelist()
def get_designation(doctype, txt, searchfield,filters, start=0, page_len=50):
	designation=get_election_designation(txt)
	return designation

@frappe.whitelist()
def get_election_designation(election):
	designation=frappe.db.sql('''select ed.designation from `tabDesignation` as d inner join `tabElection Designation` 
		ed on ed.designation=d.designation_name where ed.parent=%(parent)s order by ed.idx''',{'parent':election})
	return designation

@frappe.whitelist()
def get_choices(doctype, txt, searchfield,filters, start=0, page_len=50):
	choice=frappe.get_value('Elections',txt,'max_choice')
	return choice

@frappe.whitelist()
def get_election_detail(election):
	designation=get_election_designation(election)
	election_detail=frappe.db.get_all('Elections',fields=['require_parent_name','max_choice','election_form','acknowledgement_title','acknowledgement','signature_required'],filters={'name':election})[0]
	terms=frappe.db.get_all('Election Terms',fields=['term','parent'],filters={'parent':election},order_by='idx')
	content=[]
	content.append({'designation':designation,'election':election_detail,'terms':terms})
	return content[0]
@frappe.whitelist(allow_guest=True)
def update_images(name):	
	frappe.db.set_value('Election Nominations',name,'docstatus',1)
	return 'Success'

@frappe.whitelist()
def update_fields(name,docname):
	frappe.db.set_value('File',docname,'attached_to_name',name)
	return frappe.get_value('File',docname,'file_url')
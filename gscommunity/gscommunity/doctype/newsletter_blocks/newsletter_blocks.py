# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class NewsletterBlocks(Document):
	def autoname(self):
		self.name=self.name1.lower().replace(' ','-').replace('&','and').replace(',','')

@frappe.whitelist(allow_guest=True)
def get_template_blocks(template):
	template_blocks=frappe.db.get_all('Template Blocks',fields=['*'],filters={'parent':template},order_by='idx asc')
	if template_blocks:
		for block in template_blocks:
			block.components=frappe.db.get_all('Block Components',fields=['*'],filters={'parent':block.block},order_by='idx asc')
	return template_blocks
@frappe.whitelist(allow_guest=True)
def get_components(block):
	block_detail=frappe.get_doc('Newsletter Blocks',block)
	# block_detail.components=frappe.db.get_all('Block Components',fields=['*'],filters={'parent':block},order_by='idx asc')
	return block_detail
@frappe.whitelist(allow_guest=True)
def check_attachment(name,file_url):
	file=frappe.db.get_all('File',fields=['*'],filters={'attached_to_doctype':'Newsletter','attached_to_name':name,'file_url':file_url})
	if file:
		if not file[0].attached_to_field:
			frappe.set_value('File',file[0].name,'attached_to_field','email_attachment')
@frappe.whitelist(allow_guest=True)
def encode_base_64(file_url):
	import base64
	import requests
	return base64.b64encode(requests.get(file_url).content)
@frappe.whitelist(allow_guest=True)
def decode_base_64(file_url):
	import base64
	import requests
	return base64.b64decode(file_url)
@frappe.whitelist(allow_guest=True)
def utf8len(str,docname,file_url=None):
	string_len=len(str.encode('utf-8'))
	if file_url:
		file=frappe.db.get_all('File',fields=['file_size'],filters={'attached_to_doctype':'Newsletter','attached_to_name':docname,'attached_to_field':'email_attachment','file_url':file_url})
		if file:
			string_len=string_len+file[0].file_size
	return string_len
@frappe.whitelist()
def get_settings():
	settings=frappe.get_single('General Settings')
	return settings.newsletter_sending_emails


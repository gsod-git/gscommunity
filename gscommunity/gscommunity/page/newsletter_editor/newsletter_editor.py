from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.share import add
from frappe import _, throw


@frappe.whitelist()
def get_tree_data():

	year=frappe.db.sql('''select distinct year(creation) as year from `tabNewsletter` order by creation desc''',as_dict=1)
	
	newsletter = frappe.db.get_list('Newsletter',fields=['name','subject','template','creation'])

	template = frappe.db.get_list('Newsletter Templates',fields=['name','title'])

	block = frappe.db.get_list('Newsletter Template Components',fields=['block','block_ids','name','parent'],order_by='idx')
	

	for x in year:
		x.type = 'year'
		x.open = checkopen(x,newsletter,template,block)

	for x in newsletter:
		x.type = 'newsletter'
		x.open = checkopen(x,newsletter,template,block)

	for x in template:
		x.type = 'template'
		x.open = checkopen(x,newsletter,template,block)

	for x in block:
		x.type = 'block'
		x.open = checkopen(x,newsletter,template,block)
	
	return {'year':year, 'newsletter':newsletter, 'template':template, 'block':block}


def checkopen(i,newsletter,template,block):
	quan = 'false'
	if i.type == 'year':
		for x in newsletter:
			if i.year == x.creation.year:
				quan = 'true'

	if i.type == 'newsletter':
		for x in template:
			if i.template == x.name:
				quan = 'true'

	if i.type == 'template':
		for x in block:
			if i.name == x.parent:
				quan = 'true'

	if i.type == 'block':
		quan = None

	return quan
@frappe.whitelist()
def get_newsletter_details(newsletter):
	newsletter=frappe.get_doc('Newsletter',newsletter)	
	return newsletter
@frappe.whitelist()
def get_bloc_details(newsletter,block):
	newsletter=frappe.get_doc('Newsletter',newsletter)
	block=frappe.db.get_all('Newsletter Template Components',fields=['*'],filters={'block_ids':block,'parent':newsletter})
	return {'newsletter':newsletter,'block':block}
@frappe.whitelist()
def save_template(newsletter,html,deleted_blocks):
	if frappe.db.get_value('Newsletter',newsletter):
		frappe.db.set_value('Newsletter',newsletter,'message',html)
	news=frappe.get_doc('Newsletter',newsletter)
	delete_docs=json.loads(deleted_blocks)
	if delete_docs:
		for item in delete_docs:
			frappe.db.sql('''delete from `tabNewsletter Template Components` where block_ids=%(id)s and parent=%(parent)s''',
				{'id':item.get('block'),'parent':item.get('newsletter')})
@frappe.whitelist()
def save_block_contents(html,source_text,name,parent):
	import base64
	if frappe.get_doc('Newsletter Template Components',name):
		frappe.db.set_value('Newsletter Template Components',name,'html',html)		
		source_val=''
		if '_end_' in source_text:
			source=source_text.split('_end_')
			for item in source:
				s=item.split('_e-s_')
				if len(s)>2:				
					otr_cls=s[0]
					inr_cls=s[1]
					src=s[2]
				dataurl='data:image/png;base64,'+base64.b64encode(src)
				source_val+=otr_cls+'_e-s_'+inr_cls+'_e-s_'+src+'_e-s_'+dataurl+'_end_'
		frappe.db.set_value('Newsletter Template Components',name,'source_text',source_val)
		return source_val
@frappe.whitelist()
def get_all_blocks():
	blocks=frappe.db.get_all('Newsletter Blocks',fields=['*'])
	for item in blocks:
		item.components=frappe.db.get_all('Block Components',fields=['*'],filters={'parent':item.name})
	return blocks
@frappe.whitelist()
def add_new_block(newsletter,message,idx,new_blocks,deleted_blocks):
	news_data=json.loads(new_blocks)  
	news=frappe.get_doc('Newsletter',newsletter)
	news.message=message
	news.save()
	if news_data:
		for item in news_data:
			frappe.get_doc({
				"doctype":"Newsletter Template Components",
				"block":item.get('block'),
				"idx":idx,
				"block_ids":item.get('block_ids'),
				"html":item.get('html'),
				"fields_data_type":item.get('fields_data_type'),
				"parent":newsletter,
				"parentfield": "components",
				"parenttype": "Newsletter",
				}).insert()
	for item in news.components:
		if item.idx>idx:
			frappe.db.set_value('Newsletter Template Components',item.name,'idx',int(idx+1))
	delete_docs=json.loads(deleted_blocks)
	if delete_docs:
		for item in delete_docs:
			frappe.db.sql('''delete from `tabNewsletter Template Components` where block_ids=%(id)s and parent=%(parent)s''',
				{'id':item.get('block'),'parent':item.get('newsletter')})
@frappe.whitelist()
def update_blocks(block,html,newsletter):
	block_detail=frappe.db.get_all('Newsletter Template Components',fields=['*'],filters={'parent':newsletter,'block_ids':block})
	if block_detail:
		frappe.db.set_value('Newsletter Template Components',block_detail[0].name,'html',html)
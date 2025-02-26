# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _


def get_context(context): 
	AlbumGroup=frappe.db.get_all('Event Group',fields=['name1','image','route'],filters={'published':1})
	for item in AlbumGroup:
		AlbumsList=frappe.db.get_all('Events',fields=['name1','route','banner_image'],filters={'published':1,'event_group':item.name1})
		for data in  AlbumsList:
			Albums=frappe.db.get_all('Image Gallery',fields=['parent','sort_order','image','cover_image'],filters={'parent':data.namel})
	context.AlbumGroup=AlbumGroup
	context.AlbumsList=AlbumsList

	
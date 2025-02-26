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
	ShowAllAlbumGroup=frappe.db.get_all('Gallery',fields=['events','event_date','route','cover_image','visibility'],filters={'published':1,'visibility':'Show to All'})
	context.ShowAllAlbumGroup=ShowAllAlbumGroup
	ShowToMemberAlbumGroup=frappe.db.get_all('Gallery',fields=['events','event_date','route','cover_image','visibility'],filters={'published':1})
	context.ShowToMemberAlbumGroup=ShowToMemberAlbumGroup
 

	
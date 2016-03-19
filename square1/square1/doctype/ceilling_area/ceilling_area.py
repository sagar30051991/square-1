# -*- coding: utf-8 -*-
# Copyright (c) 2015, indicitrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CeillingArea(Document):
		pass

@frappe.whitelist(allow_guest = True)
def add_ceilling_item(self,method):
	item_code = self.item_code
	ceillingArea = frappe.get_doc("Ceilling Area","Ceilling Area")
	ceilling_item_list = []
	if ceillingArea.ceilling_item:
		for item in ceillingArea.ceilling_item:
			ceilling_item_list.append(item.item_code)

		if item_code not in ceilling_item_list:
			row = ceillingArea.append('ceilling_item', {})
			row.item_code = item_code

	if not ceillingArea.ceilling_item:
		row = ceillingArea.append('ceilling_item', {})
		row.item_code = item_code					
	ceillingArea.save(ignore_permissions = True)
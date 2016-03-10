# -*- coding: utf-8 -*-
# Copyright (c) 2015, indicitrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class OrderForm(Document):
	pass



@frappe.whitelist()
def make_Quotation(source_name,target=None):
	def set_missing_values(source, target):
		target.quotation_date=''
	target = get_mapped_doc("Order Form", source_name, {
			"Order Form": {
			"doctype": "Quotation"
			}
		},target, set_missing_values)
	return target
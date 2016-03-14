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
def get_lead(lead):
	information = frappe.db.sql("""select company,phone from `tabLead` where name = '{0}'""".format(lead),as_dict=1)
	address = frappe.db.get_value("Address",{"lead":'{0}'.format(lead), "is_primary_address":1}, "name")
	information[0]['address'] = address
	return information

@frappe.whitelist()
def get_order_form(order_form):
	order_form_doc = frappe.get_doc("Order Form",order_form)
	order_form_list = []
	for item in order_form_doc.get("order_details"):
		item_details = frappe.db.sql("""select item_name,description,stock_uom,default_warehouse 
									from `tabItem`
									where item_code = '{0}'""".format(item.product_code),as_dict=1)

		order_form_list.append({'product_code':item.product_code,'item_name':item_details[0]['item_name'],
								"description":item_details[0]['description'],
								"stock_uom":item_details[0]['stock_uom'],
								"default_warehouse":item_details[0]['default_warehouse']})
	return order_form_list	

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	target_doc = get_mapped_doc("Order Form", source_name,
		{
			"Order Form": {
				"doctype": "Quotation",
				"field_map": {
					"name": "lead"
				}
			},

			"Order Form Details": {
				"doctype": "Quotation Item",
				"field_map": {
					"product_code": "item_code",
					"item_name": "item_name",
					"description":"description",
					"stock_uom":"stock_uom",
					"warehouse":"warehouse"
			},
		},

		}, target_doc)
	target_doc.quotation_to = "Lead"

	return target_doc	
# @frappe.whitelist()
# def make_Quotation(source_name,target=None):
# 	def set_missing_values(source, target):
# 		target.quotation_date=''
# 	target = get_mapped_doc("Order Form", source_name, {
# 			"Order Form": {
# 			"doctype": "Quotation"
# 			}
# 		},target, set_missing_values)
# 	return target
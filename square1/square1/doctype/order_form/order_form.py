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
def get_lead_list(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select lead_name from `tabCustomer`""",as_list=1)

@frappe.whitelist()
def get_lead(lead):
	information = frappe.db.sql("""select company_name,phone from `tabLead` where name = '{0}'""".format(lead),as_dict=1)
	address = frappe.db.get_value("Address",{"lead":'{0}'.format(lead), "is_primary_address":1}, "name")
	information[0]['address'] = address
	return information

@frappe.whitelist()
def get_order_form(order_form):
	order_form_doc = frappe.get_doc("Order Form",order_form)
	order_form_list = []
	customer_details = []
	for item in order_form_doc.get("order_details"):
		item_details = frappe.db.sql("""select item_name,description,stock_uom,default_warehouse 
									from `tabItem`
									where item_code = '{0}'""".format(item.item_code),as_dict=1)
		frappe.errprint(item.uom)
		order_form_list.append({'product_code':item.item_code,'item_name':item_details[0]['item_name'],
								"description":item_details[0]['description'],
								"stock_uom":item.uom,
								"default_warehouse":item_details[0]['default_warehouse'],
								"qty":item.qty})
	customer = order_form_doc.get("company_name")

	details = frappe.db.sql("""select customer_name,territory, customer_group
			from `tabCustomer` where name = %s and docstatus != 2""", (customer), as_dict = 1)

	if details:
		ret = {
			'customer_name':	details and details[0]['customer_name'] or '',
			'territory':		details and details[0]['territory'] or '',
			'customer_group':	details and details[0]['customer_group'] or '',
			'customer_address':	frappe.db.get_value("Address",{"customer": customer, "is_primary_address":1}, "name"),
			'shipping_address_name':	frappe.db.get_value("Address",{"customer": customer, "is_shipping_address":1}, "name")
		}
		# ********** get primary contact details (this is done separately coz. , in case there is no primary contact thn it would not be able to fetch customer details in case of join query)

		contact_det = frappe.db.sql("""select name from `tabContact` 
										where customer = %s and 
										is_primary_contact = 1""", customer, as_dict = 1)
		
		ret['contact_name'] = contact_det and contact_det[0]['name'] or ''
		customer_details.append(ret)
	
	return {"item_details":order_form_list,"customer_details":customer_details}	

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		quotation = frappe.get_doc(target)
		quotation.run_method("set_missing_values")
	target_doc = get_mapped_doc("Order Form", source_name,
		{
			"Order Form": {
				"doctype": "Quotation",
				"field_map": {
					"company_name": "customer"
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

		}, target_doc, set_missing_values)

	target_doc.quotation_to = "Customer"

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
# -*- coding: utf-8 -*-
# Copyright (c) 2015, indicitrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import math
from frappe import _
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
		item_details = frappe.db.sql("""select item_name,description,default_warehouse 
									from `tabItem`
									where item_code = '{0}'""".format(item.item_code),as_dict=1)
		frappe.errprint(item.uom)
		order_form_list.append({'product_code':item.item_code,'item_name':item_details[0]['item_name'],
								"description":item_details[0]['description'],
								"stock_uom":item.uom,
								"default_warehouse":item_details[0]['default_warehouse'],
								"qty":item.qty,
								"catalogue":item.catalogue,
								"shade_no":item.shade_no,
								"installation_type":item.installation_type,
								"installation_location_on_site":item.installation_location_on_site})
	customer = order_form_doc.get("company_name")

	details = frappe.db.sql("""select customer_name,territory, customer_group
			from `tabCustomer` where name = %s and docstatus != 2""", (customer), as_dict = 1)

	if details:
		ret = {
			'customer_name':	details and details[0]['customer_name'] or '',
			'territory':		details and details[0]['territory'] or '',
			'customer_group':	details and details[0]['customer_group'] or '',
			'customer_address':	frappe.db.get_value("Address",{"customer": customer, "is_primary_address":1}, "name"),
			'shipping_address_name': frappe.db.get_value("Address",{"customer": customer, "is_shipping_address":1}, "name")
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
					"item_code": "item_code",
					"item_name": "item_name",
					"description":"description",
					"uom":"stock_uom",
					"warehouse":"warehouse",
					"qty":"qty",
			},
		},

		}, target_doc,set_missing_values)

	target_doc.quotation_to = "Customer"

	return target_doc
	
@frappe.whitelist()
def get_uom_list(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(""" select t1.uom from `tabUOM Conversion Detail`t1,
							`tabItem`t2 where t1.parent = t2.name 
							and t2.installation_type = '{0}' 
							and t2.name = '{1}' """.format(filters['installation_type'],filters['item_code']),as_list=1)								

@frappe.whitelist()
def get_ceillling_item_qty(area,item_code):
	area = int(area)
	qty = frappe.db.sql("""select t1.qty from `tabCeilling Items`t1 where t1.item_code = '{0}' and t1.parent = "Ceilling Area" """.format(item_code),as_list=1)
	fix_area_list = frappe.db.sql("""select value from `tabSingles` where doctype = "Ceilling Area" and field = "total_area" """,as_list=1) 
	fix_area = int(fix_area_list[0][0])
	if qty[0][0] > 0:
		qty = int(qty[0][0])
		"""by area""" 
		area_above_fix_area_plus_50 = fix_area * math.ceil(area/float(fix_area))
		minus_50 = area_above_fix_area_plus_50 - 50
		if area < (fix_area - round(fix_area/float(2))):
			#print "less than 50"
			calculate_qty = round(qty/float(2))
			return calculate_qty
		
		elif area <= fix_area and area > (fix_area - round(fix_area/float(2))):
			#print "greater than 50 and less than or equal to 100"
			calculate_qty = qty
			return calculate_qty
		
		elif area > fix_area and area <= (fix_area + round(fix_area/float(2))):
			#print "greater than 100 less than or equal to 150"
			calculate_qty = qty + round(qty/float(2))
			return calculate_qty
		
		elif area > (fix_area + round(fix_area/float(2))) and area <= minus_50:
			#print "greater than 150 less than minus_50"
			factor = round(area/float(fix_area))
			calculate_qty = ((qty * factor) + round(qty/float(2)))
			return calculate_qty

		elif area > (fix_area + round(fix_area/float(2))) and area <= (fix_area * math.ceil(area/float(fix_area))):
			#print "greater than 150"
			factor = round(area/float(fix_area))
			calculate_qty = qty * factor
			return calculate_qty
	else:
		frappe.throw(_("Enter Quantity For Item Code '{0}' In Ceilling Area").format(item_code))	
	"""by qty"""
	# qty_by_area = math.ceil(qty/float(fix_area))
	# calculate_qty = area * qty_by_area	
	# return calculate_qty 

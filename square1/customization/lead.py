
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class Lead(Document):
	pass

@frappe.whitelist()
def make_order(source_name,target_doc= None,ignore_permissions=False):
	target_doc = get_mapped_doc("Lead", source_name,{
		"Lead": {
			"doctype": "Order Form",
			"field_map": {
				"company_name": "company_name",
				"phone": "phone"
			}
		}
	}, target_doc)

	return target_doc


# @frappe.whitelist()
# def check_customer(lead):
# 	print lead
# 	query = frappe.db.sql("""select lead_name from `tabCustomer` where lead_name = %s"""%(lead))
# 	print query
# 	return query
@frappe.whitelist()
def check_customer(lead):
	query = frappe.db.sql("""select lead_name from `tabCustomer` where lead_name = %s"""%(lead))
	return query


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

@frappe.whitelist()
def get_sms_address(lead):
	address=frappe.db.get_value("Address",{"is_primary_address":1,"lead":lead},["address_title","address_type","address_line1","address_line2","city","state","pincode","phone"])
	if address:
		return "%s-%s\n%s,%s\n%s,%s-%s\nPhone: %s"%(address[0] or "",  address[1] or "", address[2] or "", address[3] or "", address[4] or "", address[5] or "", address[6] or "", address[7] or "") 
	else:
		return ""

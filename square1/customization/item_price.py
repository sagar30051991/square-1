
import frappe

def price_list_on_update(doc, method):
	# check price list applicable or not to the respective item
	if (doc.price_list == "Discount Rate"):
		basic = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Basic Rate"}, "price_list_rate")
		negotiation = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Negotiation Rate"}, "price_list_rate")
		if (doc.price_list_rate<basic and doc.price_list_rate>negotiation):
			frappe.msgprint("Added Successfully")
		else:
			frappe.throw("Not allow")
	elif(doc.price_list == "Basic Rate"):
		discount = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Discount Rate"}, "price_list_rate")
		negotiation = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Negotiation Rate"}, "price_list_rate")
		if (doc.price_list_rate>negotiation and doc.price_list_rate>discount):
			frappe.msgprint("Added Successfully")
		else:
			frappe.throw("Not allow")
	elif(doc.price_list == "Negotiation Rate"):
		discount = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Discount Rate"}, "price_list_rate")
		#basic = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Basic Rate"}, "price_list_rate")
		if (doc.price_list_rate<discount):
			frappe.msgprint("Added Successfully")
		else:
			frappe.throw("Not allow")
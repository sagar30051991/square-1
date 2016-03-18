
import frappe

def price_list_on_update(doc, method):
	# check price list applicable or not to the respective item
	stock = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Standard Buying"}, "price_list_rate")
	dealer = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Dealer Rate"}, "price_list_rate")
	discount = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Discount Rate"}, "price_list_rate")
	basic = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Basic Rate"}, "price_list_rate")
	negotiation = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Negotiation Rate"}, "price_list_rate")
	if (doc.price_list == "Discount Rate"):
		if (doc.price_list_rate<basic and doc.price_list_rate>negotiation):
			frappe.msgprint("Discount Price Added Successfully")
		else:
			frappe.throw("Discount Price is Not allow To Save")
	elif(doc.price_list == "Basic Rate"):
		if(doc.price_list_rate>dealer and doc.price_list_rate>stock):
			if (doc.price_list_rate>negotiation and doc.price_list_rate>discount):
				frappe.msgprint("Basic Price Added Successfully")
			else:
				frappe.throw("Basic Price is Not allow To Save")
	elif(doc.price_list == "Negotiation Rate"):
		if(doc.price_list_rate<basic and doc.price_list_rate>stock):
			if (doc.price_list_rate<discount and doc.price_list_rate>dealer):
				frappe.msgprint("Negotiation Price Added Successfully")
			else:
				frappe.throw("Negotiation Price is Not allow To Save")
		else:
				frappe.throw("Please enter the Correct Value")
	elif(doc.price_list == "Dealer Rate"):
		# var data="select price_list from tabPrice_List where item_code=",''
		if(doc.price_list_rate<basic and doc.price_list_rate>stock):
			if (doc.price_list_rate<negotiation and doc.price_list_rate<discount):
				frappe.msgprint("Dealer Price Added Successfully")
			else:
				frappe.throw("Dealer Price is Not allow To Save")
		else:
				frappe.throw("Please enter the Correct Value")
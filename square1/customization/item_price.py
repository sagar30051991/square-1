
import frappe

def price_list_on_update(doc, method):
	# check price list applicable or not to the respective item
	
	stock = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Stock Rate"}, "price_list_rate")
	dealer = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Dealer Rate"}, "price_list_rate")
	discount = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Discount Rate"}, "price_list_rate")
	basic = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Basic Rate"}, "price_list_rate")
	negotiation = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Negotiation Rate"}, "price_list_rate")
	
	if(not stock and not dealer and not discount and not basic and not negotiation and not basic):
		none=True
	else:
		none=False

	if(doc.price_list == "Basic Rate"):
		#frappe.msgprint("In basic")
		if(none):
			#frappe.msgprint("none")
			frappe.msgprint("Basic Price Added Successfully")
		elif(doc.price_list_rate>stock):
			#frappe.msgprint(doc.price_list_rate)
			#frappe.msgprint(stock)
			frappe.msgprint("Basic Price Added Successfully")
		else:
			frappe.throw("Basic Price is Not allow To Save")
	elif (doc.price_list == "Discount Rate"):
		if(none):
			frappe.msgprint("Discount Price Added Successfully")
		elif (doc.price_list_rate<basic):
			frappe.msgprint("Discount Price Added Successfully")
		else:
			frappe.throw("Please First Enter the Basic Rate")
	elif(doc.price_list == "Negotiation Rate"):
		if(none):
			frappe.msgprint("Negotiation Price Added Successfully")
		elif(doc.price_list_rate<discount):

			 	frappe.msgprint("Negotiation Price Added Successfully")
		else:
				frappe.throw("Please First Enter the Discount Rate")
	elif(doc.price_list == "Dealer Rate"):
		if (none):
			frappe.msgprint("Dealer Price Added Successfully")
		elif (doc.price_list_rate<negotiation and doc.price_list_rate>stock): 
			frappe.msgprint("Dealer Price Added Successfully")
		else:
			frappe.throw("Please First Enter the Negotiation Rate")
	elif(doc.price_list == "Stock Rate"):
		if (none):
			frappe.msgprint("Stock Price Added Successfully")
		elif (doc.price_list_rate<dealer): 
			frappe.msgprint("Stock Price Added Successfully")
		else:
			frappe.throw("Please First Enter the Dealer Rate")
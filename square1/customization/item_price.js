
/*stock = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Standard Buying","exist": "Yes"}, "price_list_rate")
	dealer = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Dealer Rate","exist": "Yes"}, "price_list_rate")
	discount = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Discount Rate", "exist": "Yes"}, "price_list_rate")
	basic = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Basic Rate","exist": "Yes"}, "price_list_rate")
	negotiation = frappe.db.get_value("Item Price",{"item_code":doc.item_code, "price_list":"Negotiation Rate","exist": "Yes"}, "price_list_rate")

if (doc.price_list == "Discount Rate"){

    else
    {
    	msgprint("You can not select past date in From Date");
    }
}
});*/
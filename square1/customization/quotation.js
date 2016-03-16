frappe.ui.form.on("Quotation", {
	refresh: function(doc, dt, dn) {			
		if (this.cur_frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Order Form'),
				function() {
					var dialog = new frappe.ui.Dialog({
						title: "Get From Order Form",
							fields: [
								{"fieldtype": "Link", "label": __("Order Form"), "fieldname": "order_form","options":'Order Form',"reqd": 1 },
								{"fieldtype": "Button", "label": __("Get"), "fieldname": "get"},
							]
						});
					dialog.fields_dict.get.$input.click(function() {
						value = dialog.get_values();
						return cur_frm.call({
							method: "square1.square1.doctype.order_form.order_form.get_order_form",
							args:{
								"order_form":value.order_form
							},
							callback: function(r) {
								console.log(r.message['customer_details'][0])
								cur_frm.doc.customer = r.message['customer_details'][0]['customer_name'],
								cur_frm.doc.territory = r.message['customer_details'][0]['territory'],
								cur_frm.doc.customer_group = r.message['customer_details'][0]['customer_group'],
								cur_frm.doc.contact_person = r.message['customer_details'][0]['contact_name'],
								cur_frm.doc.shipping_address_name = r.message['customer_details'][0]['shipping_address_name'],
								cur_frm.doc.customer_address = r.message['customer_details'][0]['customer_address']
								refresh_field(["territory","contact_person","shipping_address_name","customer_address","customer","customer_group"])
								$.each(r.message['item_details'], function(i, d) {
								var row = frappe.model.add_child(cur_frm.doc, "Quotation Item", "items");
								row.item_code = d.product_code,
								row.item_name = d.item_name,
								row.description = d.description,
								row.stock_uom = d.stock_uom,
								row.warehouse = d.default_warehouse,
								row.qty = d.qty,
								row.rate = 0.00
								refresh_field("items");
								});
								dialog.hide();
								cur_frm.refresh();
							},
							btn: this
						})
					});
					dialog.show();
			}, __("Get Items from"), "btn-default");
		}
	},
});
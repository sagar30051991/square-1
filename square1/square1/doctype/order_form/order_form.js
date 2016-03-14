cur_frm.add_fetch('product_code', 'item_name', 'item_name');
cur_frm.add_fetch('product_code', 'description', 'description');
cur_frm.add_fetch('product_code', 'stock_uom', 'stock_uom');
cur_frm.add_fetch('product_code', 'default_warehouse', 'warehouse');

frappe.ui.form.on("Order Form", {
	refresh: function(doc, dt, dn) {
			
		if (this.cur_frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Lead'),
				function() {
					var dialog = new frappe.ui.Dialog({
						title: "Get From Lead",
							fields: [
								{"fieldtype": "Link", "label": __("Lead"), "fieldname": "lead","options":'Lead',"reqd": 1 },
								{"fieldtype": "Button", "label": __("Get"), "fieldname": "get"},
							]
					});

					dialog.fields_dict.get.$input.click(function() {
						value = dialog.get_values();
						return cur_frm.call({
							method: "square1.square1.doctype.order_form.order_form.get_lead",
							args:{
								"lead":value.lead
							},
							callback: function(r) {
								if(r.message){
									cur_frm.doc.company_name = r.message[0]['company'],
									cur_frm.doc.phone = r.message[0]['phone'],
									cur_frm.doc.address = r.message[0]['address']
								}
								dialog.hide();
								cur_frm.refresh();
							},
							btn: this
						})
					});
					dialog.show();
			}, __("Get Information from"), "btn-default");
			cur_frm.add_custom_button(__('Quotation'),function(){
				make_quotation();
			});
		}
	},
});

make_quotation  = function() {
	frappe.model.open_mapped_doc({
		method: "square1.square1.doctype.order_form.order_form.make_quotation",
		frm: cur_frm
	})
}

cur_frm.fields_dict['address'].get_query=function(doc){
	return {
		filters:{
				'address_title':doc.company_name
				}
		}
}
/*installation_type: function() {
	if(frm.doc.installation_type) {
		frm.set_value("uom", {
			"Wall Paper": "Roll",
			"Flooring": "Box"
			}[frm.doc.installation_type]);
		}
	}
*/
frappe.ui.form.on("Order Form Details", "installation_type", function(frm){
	//var d = frappe.model.get_doc(cdt, cdn);
	if(frm.installation_type) {
		frm.set_value("uom", {
			"Wall Paper": "Roll",
			"Flooring": "Box"
			}[frm.installation_type]);
		}
})
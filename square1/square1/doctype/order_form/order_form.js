cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('item_code', 'description', 'description');
cur_frm.add_fetch('item_code', 'stock_uom', 'uom');
cur_frm.add_fetch('item_code', 'default_warehouse', 'warehouse');

frappe.ui.form.on("Order Form", {
	refresh: function(doc, dt, dn) {
			
		if (this.cur_frm.doc.docstatus===0) {
			cur_frm.add_custom_button(__('Lead'),
				function() {
					var dialog = new frappe.ui.Dialog({
						title: "Get From Lead",
							fields: [
								{"fieldtype": "Link", "label": __("Lead"), "fieldname": "lead",
								"options":'Lead',"reqd": 1, 
								get_query: function() {
									return "square1.square1.doctype.order_form.order_form.get_lead_list"
								}
							},
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
									cur_frm.doc.company_name = r.message[0]['company_name'],
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
	}
	/*installation_type: function(frm, cdt, cdn) {
		console.log("hello")
		var row = locals[cdt][cdn];
		if(row.installation_type) {
			console.log("inside if")
			frm.set_value("uom", {
				"Wall Paper": "Roll",
				"Flooring": "Box"
				}[frm.doc.installation_type]);
			}
	}*/
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



frappe.ui.form.on("Order Form Details","installation_type", function(frm,cdt, cdn) {
	var d = locals[cdt][cdn]
	if(d.installation_type && d.installation_type == "Wall Paper"){
		cur_frm.doc.order_details[0].uom = "Rolls"
		refresh_field("order_details")
	}
	if(d.installation_type && d.installation_type == "Flooring"){
		cur_frm.doc.order_details[0].uom = "Box"
		refresh_field("order_details")
	}
	if(d.installation_type && d.installation_type == "Ceilling"){
		cur_frm.doc.order_details[0].uom = "Pcs"
		refresh_field("order_details")
	}
})

cur_frm.fields_dict.order_details.grid.get_field("item_code").get_query = function(frm,cdt,cdn) {
	var d = locals[cdt][cdn]
	console.log(d.installation_type)
	return {
		filters: [
			['Item','installation_type','=',d.installation_type]
		]
	}
}

frappe.ui.form.on("Order Form Details","length",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333	
	if(d.width){
		d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
		d.area = width.toFixed(2) * length.toFixed(2)
		refresh_field("order_details")
	}	
})

frappe.ui.form.on("Order Form Details","width",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333	
	if(d.length){
		d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
		d.area = width.toFixed(2) * length.toFixed(2)
		refresh_field("order_details")
	}	
})


frappe.ui.form.on("Order Form Details","divide_by",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333
	if(d.installation_type == "Wall Paper"){
		var area = (width.toFixed(2) * length.toFixed(2)) / cur_frm.doc.order_details[0].divide_by
		d.qty = roundNumber(area)
		refresh_field("order_details")	
	}
})

frappe.ui.form.on("Order Form Details","divide",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333
	if(d.installation_type == "Flooring"){
		var area = (width.toFixed(2) * length.toFixed(2))
		var area_with_wastage = (area + ((area * 5) / 100)) / cur_frm.doc.order_details[0].divide
		d.qty = roundNumber(area_with_wastage)
		refresh_field("order_details")	
	}
})

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


frappe.ui.form.on("Order Form Details","length",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	if(d.width){
		var width = d.width * 0.083333	
		var length = d.length * 0.083333	
		console.log([d.length,d.width])
		if(d.installation_type == "Ceilling" && d.item_code){
			var item_code = d.item_code
			d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
			d.area = width.toFixed(2) * length.toFixed(2)
			refresh_field("order_details")
			var area = roundNumber(d.area)
			calculation_for_ceilling_item_qty(area,item_code,d)
		}	
		else{
			d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
			d.area = width.toFixed(2) * length.toFixed(2)
			refresh_field("order_details")
		}
	}	
})

frappe.ui.form.on("Order Form Details","width",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	if(d.length){
		var width = d.width * 0.083333	
		var length = d.length * 0.083333	
		if(d.installation_type == "Ceilling" && d.item_code){
			var item_code = d.item_code
			d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
			d.area = width.toFixed(2) * length.toFixed(2)
			refresh_field("order_details")
			var area = roundNumber(d.area)
			calculation_for_ceilling_item_qty(area,item_code,d)
		}	
		else{
			d.site_dimension = width.toFixed(2) + "X" + length.toFixed(2) 
			d.area = width.toFixed(2) * length.toFixed(2)
			refresh_field("order_details")
		}
	}	
})


frappe.ui.form.on("Order Form Details","divide_by",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333
	if(d.installation_type == "Wall Paper"){
		var area = (width.toFixed(2) * length.toFixed(2)) / d.divide_by
		d.qty = Math.ceil(area)
		refresh_field("order_details")	
	}
})

frappe.ui.form.on("Order Form Details","divide",function(frm,cdt,cdn){
	var d  = locals[cdt][cdn];
	var width = d.width * 0.083333	
	var length = d.length * 0.083333
	if(d.installation_type == "Flooring"){
		var area = (width.toFixed(2) * length.toFixed(2))
		var area_with_wastage = (area + ((area * 5) / 100)) / d.divide
		d.qty = Math.ceil(area_with_wastage)
		refresh_field("order_details")	
	}
})


calculation_for_ceilling_item_qty = function(area,item_code,d){ 
	frappe.call({
        method: "square1.square1.doctype.order_form.order_form.get_ceillling_item_qty",
        args: {
            "area":area,
            "item_code": item_code
        },
       	callback: function(r){
       		console.log(r.message)
       	d.qty = r.message
       	refresh_field("order_details")
       	}
	})
}

/*cur_frm.fields_dict.order_details.grid.get_field("uom").get_query = function(doc,cdt,cdn) {
	var d  = locals[cdt][cdn];
	if(d.item_code){
		return {
			query: "square1.square1.doctype.order_form.order_form.get_uom_list",
			filters: {
				'installation_type': d.installation_type,
				'item_code':d.item_code
			}
		}
	}
}*/

cur_frm.fields_dict.order_details.grid.get_field("item_code").get_query = function(doc,cdt,cdn) {
	var t_list = []
	for(var i = 0 ; i < cur_frm.doc.order_details.length ; i++){
		if(cur_frm.doc.order_details[i].item_code){
			t_list.push(cur_frm.doc.order_details[i].item_code);
		}
	}
	return {
		filters:[
			["Item","installation_type","=",d.installation_type],
			["Item","name",'not in',t_list]	
		]
	}
}

frappe.ui.form.on("Order Form","order_date",function(frm){
	var order_date = new Date(cur_frm.doc.order_date)
	var measurement_date = new Date(cur_frm.doc.measurement_date)
	var installation_date = new Date(cur_frm.doc.installation_date)
	if(measurement_date > order_date){
		msgprint(__("Order Date Greater Than Or Equal To Measurement Date "))
		cur_frm.doc.order_date = ""
		refresh_field('order_date')
	}
	else if(order_date >= installation_date){
		msgprint(__("Order Date Not Equal To Or Greater Than installation_date Date "))
		cur_frm.doc.order_date = ""
		refresh_field('order_date')
	}		
})

frappe.ui.form.on("Order Form","installation_date",function(frm){
	var order_date = new Date(cur_frm.doc.order_date)
	var measurement_date = new Date(cur_frm.doc.measurement_date)
	var installation_date = new Date(cur_frm.doc.installation_date)
	if(installation_date <= order_date){
		msgprint(__("Installation Date Greater Than Order Date "))
		cur_frm.doc.installation_date = ""
		refresh_field('installation_date')
	}		
})
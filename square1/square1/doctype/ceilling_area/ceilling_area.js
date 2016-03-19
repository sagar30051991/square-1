// Copyright (c) 2016, indicitrans and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ceilling Area', {
	refresh: function(frm) {

	}
});


cur_frm.fields_dict.ceilling_item.grid.get_field("item_code").get_query = function(doc,cdt,cdn) {
	var t_list = []
	for(var i = 0 ; i < cur_frm.doc.ceilling_item.length ; i++){
		if(cur_frm.doc.ceilling_item[i].item_code){
			t_list.push(cur_frm.doc.ceilling_item[i].item_code);
		}
	}	
	return {
		filters:[
			["Item","installation_type","=","Ceilling"],
			["Item","name",'not in',t_list]	
		]
	}
}
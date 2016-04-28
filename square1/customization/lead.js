frappe.ui.form.on("Lead",{ 
	refresh: function(frm) {
		var me = this
		/*if(!frm.doc.__islocal && cur_frm.doc.status=="Converted") {		
				cur_frm.add_custom_button(__('Make Order'), function() {*/
		if(!frm.doc.__islocal && frm.doc.status == "Converted") {		
				cur_frm.add_custom_button(__('Order Form'), function() {
				cur_frm.cscript.make_order(); 
				}, __("Make"));
				cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}

		if(frm.doc.docstatus===0 && in_list(["Converted"], frm.doc.status)
			&& frm.doctype == "Lead") {
			frm.page.add_menu_item(__('Send SMS'), function() { send_sms(frm); });
		}
	}
});
send_sms= function(frm) {
		frappe.require("assets/erpnext/js/sms_manager.js");
		var sms_man = new SMSManager(cur_frm.doc);
		fd = sms_man.dialog.fields_dict;
		fatch_addr(fd,frm)
		
	},
/*frappe.ui.form.on("Lead", "refresh", function(frm){
		cur_frm.add_custom_button(__('Make Order'), function() {
			cur_frm.cscript.make_order(); 
		/*if(frm.doc.status == "Lead"){
			
		})
	}
})
/*if (this.cur_frm.doc.docstatus===1) {
			cur_frm.add_custom_button(__('Make Order'),
				function() {
					cur_frm.cscript.make_order(); 
					//var dialog = new frappe.ui.Dialog({
		},*/
// frappe.ui.form.on("Lead ","refresh" ,function(frm) {
// 	var me = this
// 	if(!frm.doc.__islocal) {
// 	cur_frm.add_custom_button(__('Make Order'), function() {
// 		cur_frm.cscript.make_order();
// 	});
// 	}
// }

// });
fatch_addr = function(fd,frm){
	frappe.call({
		method:"square1.customization.lead.get_sms_address",
		args:
		{
			"lead":cur_frm.doc.name
		},
		callback: function(r) {
			if(r.message) {
				fd.message.set_input("Contact Details\n"+r.message)
			}
		}
	});
}
cur_frm.cscript.make_order =function(){
	frappe.model.open_mapped_doc({
		method: "square1.customization.lead.make_order",
		frm: cur_frm
	});
}
import frappe

def get_permission_query_conditions_for_price_list(user):
	if "System Manager" in frappe.get_roles(user):
		return None
	elif "Staff" in frappe.get_roles(user):
		return """(`tabPrice List`.name not in ("Stock Rate", "Dealer Rate"))"""
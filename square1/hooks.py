# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "square1"
app_title = "Square1"
app_publisher = "indicitrans"
app_description = "Customization"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "sagar.s@indictranstech.com"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/square1/css/square1.css"
# app_include_js = "/assets/square1/js/square1.js"

# include js, css files in header of web template
# web_include_css = "/assets/square1/css/square1.css"
# web_include_js = "/assets/square1/js/square1.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "square1.install.before_install"
# after_install = "square1.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "square1.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Price List": "square1.customization.price_list.get_permission_query_conditions_for_price_list",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	"Item Price": {
		"on_update": "square1.customization.item_price.price_list_on_update"
	},
	"Item": {
		"on_update": "square1.square1.doctype.ceilling_area.ceilling_area.add_ceilling_item"
	}	
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"square1.tasks.all"
# 	],
# 	"daily": [
# 		"square1.tasks.daily"
# 	],
# 	"hourly": [
# 		"square1.tasks.hourly"
# 	],
# 	"weekly": [
# 		"square1.tasks.weekly"
# 	]
# 	"monthly": [
# 		"square1.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "square1.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "square1.event.get_events"
# }
fixtures = ["Property Setter", "Custom Field","Print Format"]

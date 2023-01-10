from . import __version__ as app_version

app_name = "next_store"
app_title = "Next Store"
app_publisher = "Next"
app_description = "Next"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "Next"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/next_store/css/next_store.css"
# app_include_js = "/assets/next_store/js/next_store.js"

# include js, css files in header of web template
# web_include_css = "/assets/next_store/css/next_store.css"
# web_include_js = "/assets/next_store/js/next_store.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "next_store/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "next_store.install.before_install"
# after_install = "next_store.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "next_store.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    # 	"*": {
    # 		"on_update": "method",
    # 		"on_cancel": "method",
    # 		"on_trash": "method"
    # 	}
	"Sales Invoice": {
		"autoname": "next_store.autoname_invoice",
		"on_cancel": "next_store.on_cancel",
		"before_submit":"next_store.before_submit"
	},
	"POS Invoice":{
		"before_submit": "next_store.validate_pos"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    # 	"all": [
    # 		"next_store.tasks.all"
    # 	],
    # 	"daily": [
    # 		"next_store.tasks.daily"
    # 	],
    # 	"hourly": [
    # 		"next_store.tasks.hourly"
    # 	],
    # 	"weekly": [
    # 		"next_store.tasks.weekly"
    # 	]
    # 	"monthly": [
    # 		"next_store.tasks.monthly"
    # 	]
    "cron": {"*/15 * * * *": ["next_store.custompy.invoice_sync.cron_sync_order"]}
}

# Testing
# -------

# before_tests = "next_store.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "next_store.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "next_store.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {"doctype": "{doctype_4}"},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"next_store.auth.validate"
# ]

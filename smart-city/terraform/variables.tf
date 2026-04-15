variable "location" {
  type    = string
  default = "Central India"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "project_name" {
  type    = string
  default = "smart-city"
}

variable "subscription_id" {
  type        = string
  description = "Azure subscription ID used for budget scope and optional resources."
  default     = ""
}

variable "node_count" {
  type        = number
  default     = 2
  description = "AKS default node count."
}

variable "enable_key_vault" {
  type    = bool
  default = true
}

variable "enable_monitoring" {
  type    = bool
  default = true
}

variable "enable_budget_alert" {
  type    = bool
  default = false
}

variable "monthly_budget_amount" {
  type    = number
  default = 100
}

variable "budget_contact_emails" {
  type        = list(string)
  default     = []
  description = "Emails for cost budget notifications."
}

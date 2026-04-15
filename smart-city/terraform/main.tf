locals {
  prefix = "${var.project_name}-${var.environment}"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.prefix}-rg"
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${local.prefix}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.20.0.0/16"]
}

resource "azurerm_subnet" "aks" {
  name                 = "${local.prefix}-aks-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.20.1.0/24"]
}

resource "random_password" "db_password" {
  length  = 20
  special = true
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${local.prefix}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${local.prefix}-dns"

  default_node_pool {
    name            = "system"
    node_count      = var.node_count
    vm_size         = "Standard_D2s_v5"
    vnet_subnet_id  = azurerm_subnet.aks.id
    os_disk_size_gb = 64
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "${replace(local.prefix, "-", "")}postgres"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "16"
  administrator_login    = "smartcityadmin"
  administrator_password = random_password.db_password.result
  sku_name               = "B_Standard_B1ms"
  storage_mb             = 32768
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "db" {
  name      = "smartcity"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

resource "azurerm_key_vault" "kv" {
  count                       = var.enable_key_vault ? 1 : 0
  name                        = "${replace(local.prefix, "-", "")}kv"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = false
  soft_delete_retention_days  = 7
  enable_rbac_authorization   = true
}

resource "azurerm_key_vault_secret" "postgres_password" {
  count        = var.enable_key_vault ? 1 : 0
  name         = "postgres-admin-password"
  value        = random_password.db_password.result
  key_vault_id = azurerm_key_vault.kv[0].id
}

resource "azurerm_log_analytics_workspace" "law" {
  count               = var.enable_monitoring ? 1 : 0
  name                = "${local.prefix}-law"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "appi" {
  count               = var.enable_monitoring ? 1 : 0
  name                = "${local.prefix}-appi"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.law[0].id
}

resource "azurerm_monitor_action_group" "ops" {
  count               = var.enable_monitoring ? 1 : 0
  name                = "${replace(local.prefix, "-", "")}opsag"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "smartops"

  dynamic "email_receiver" {
    for_each = toset(var.budget_contact_emails)
    content {
      name          = "ops-${replace(email_receiver.value, "@", "-at-")}"
      email_address = email_receiver.value
    }
  }
}

resource "azurerm_consumption_budget_subscription" "monthly" {
  count           = var.enable_budget_alert && var.subscription_id != "" ? 1 : 0
  name            = "${local.prefix}-monthly-budget"
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = var.monthly_budget_amount
  time_grain      = "Monthly"

  time_period {
    start_date = "2026-01-01T00:00:00Z"
    end_date   = "2030-12-31T00:00:00Z"
  }

  notification {
    enabled        = true
    operator       = "GreaterThan"
    threshold      = 80
    threshold_type = "Actual"
    contact_emails = var.budget_contact_emails
  }
}

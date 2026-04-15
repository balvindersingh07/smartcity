output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "key_vault_name" {
  value = var.enable_key_vault ? azurerm_key_vault.kv[0].name : null
}

output "application_insights_connection_string" {
  value     = var.enable_monitoring ? azurerm_application_insights.appi[0].connection_string : null
  sensitive = true
}

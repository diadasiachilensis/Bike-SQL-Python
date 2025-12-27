variable "container_name" {
  description = "Nombre del contenedor de Docker para la Base de Datos"
  type        = string
  default     = "custombikes_db_container"
}

variable "postgres_user" {
  description = "Usuario administrador de PostgreSQL"
  type        = string
  default     = "custom_user"
}

variable "postgres_password" {
  description = "Contraseña de PostgreSQL"
  type        = string
  default     = "secure_password"
  sensitive   = true # Esto evita que Terraform la muestre en los logs de consola
}

variable "postgres_db" {
  description = "Nombre de la base de datos a crear"
  type        = string
  default     = "custombike"
}

variable "host_port" {
  description = "Puerto externo de la máquina host"
  type        = number
  default     = 5432
}
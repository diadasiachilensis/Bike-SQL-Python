terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "docker" {}

# Red compartida
resource "docker_network" "data_network" {
  name = "custombikes_data_network"
}

# Base de Datos de Negocio
resource "docker_container" "custombikes_db" {
  name  = "custombikes_db_container"
  image = "postgres:13"
  restart = "always"

  env = [
    "POSTGRES_USER=custom_user",
    "POSTGRES_PASSWORD=secure_password",
    "POSTGRES_DB=custombike"
  ]

  networks_advanced {
    name = docker_network.data_network.name
  }

  ports {
    internal = 5432
    external = 5432
  }

  # ¡Aquí ocurre la magia! Montamos toda la carpeta SQL
  volumes {
    host_path      = abspath("${path.cwd}/../sql")
    container_path = "/docker-entrypoint-initdb.d"
  }
}
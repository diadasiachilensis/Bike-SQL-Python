terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.6.2"    }
  }
}


provider "docker" {
  # ¡IMPORTANTE! Bloque vacío intencionalmente.
  # La configuración se inyectará vía variables de entorno.
}

resource "docker_network" "data_network" {
  name = "custombikes_data_network"
}

resource "docker_image" "postgres" {
  name         = "postgres:13"
  keep_locally = true
}

resource "docker_container" "custombikes_db" {
  name  = "custombikes_db_container"
  image = docker_image.postgres.image_id
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

  volumes {
    host_path      = abspath("${path.cwd}/../sql")
    container_path = "/docker-entrypoint-initdb.d"
  }
}

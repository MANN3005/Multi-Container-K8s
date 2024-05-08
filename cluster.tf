provider "google" {
  project     = "csci5409-b00951709"
  region        = "us-central1"
}

resource "google_container_cluster" "k8s-cluster" {
    name = "k8s-cluster"
    location = "us-central1-c"
    initial_node_count = 1
    node_config {
      machine_type = "e2-micro"
      disk_size_gb = 10
      disk_type = "pd-standard"
      image_type = "cos_containerd"

    }
}

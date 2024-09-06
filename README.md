# Project Canario

## Automating a Deployment Platform

Project Canario is an initiative aimed at automating the deployment platform for a digital solutions provider. The project focuses on implementing a robust CI/CD pipeline, Docker Swarm for container orchestration, feature flag management, and HAProxy for efficient load balancing.

### Key Features

- **CI/CD Pipeline:** Streamlined integration and deployment processes using GitLab CI/CD, ensuring rapid, reliable software updates.
- **Docker and Swarm Integration:** Utilizing Docker's containerization capabilities and Docker Swarm for orchestrating containers and managing services.
- **HAProxy for Load Balancing:** Implementing HAProxy to efficiently distribute traffic and maintain optimal user experience during peak loads.
- **Feature Flags Management:** Dynamic management of website features, allowing real-time activation or deactivation, facilitated by Memcache for efficient state management.
- **FastAPI Development:** Building the website on the FastAPI platform, known for its quick performance and ease of handling large volumes of requests.
- **Performance Monitoring:** Utilizing Grafana and Prometheus for real-time monitoring and analysis of system performance.
- **Traffic Simulation for Load Testing:** Employing httperf for simulating various traffic patterns to stress-test the infrastructure.

### Getting Started

To begin using Project Canario, ensure you have Docker, GitLab, and HAProxy installed on your system. Follow these steps:

1. **Clone the Repository:**

```bash
https://github.com/HJacksons/Canario-shop.git
```

2. **Setting Up Docker and Swarm:**
Refer to the `Dockerfile` and Docker Swarm configuration documentation in the project.

3. **Running the CI/CD Pipeline:**
Configure GitLab Runner and set up the `.gitlab-ci.yml` file as per your project needs.

4. **Load Balancing Configuration:**
Set up HAProxy using the provided configuration guidelines.

5. **Monitoring Setup:**
Implement Grafana and Prometheus for monitoring. Configuration details are available in the appendix.

6. **Feature Flags Management:**
Use the Memcache integration for managing feature flags. Refer to the Feature Flag Management section for setup and usage.

### Contributing

Contributions to Project Canario are welcome! Please read our contributing guidelines to get started.

### License

This project is licensed under the [MIT License](LICENSE.md) - see the LICENSE file for details.

# Installation

## Step 1: Install Docker and Docker Compose

1. **Update Package Index**:
   ```bash
   sudo apt update
   ```

2. **Install Docker**:
   ```bash
   sudo apt install docker.io
   ```

3. **Verify Docker Installation**:
   ```bash
   docker version
   ```

4. **Install Docker Compose**:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. **Verify Docker Compose Installation**:
   ```bash
   docker-compose --version
   ```

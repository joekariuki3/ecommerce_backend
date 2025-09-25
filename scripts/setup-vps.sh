#!/bin/bash
# filepath: scripts/setup-vps.sh
# Run this script on your fresh VPS (Ubuntu 22.04) as root via SSH.
# Usage: chmod +x scripts/setup-vps.sh && sudo ./scripts/setup-vps.sh
# This script is idempotent: safe to run multiple times.

set -e  # Exit on error

echo "Starting VPS setup with security best practices..."

# 1. Update system packages (always safe to run)
echo "Updating system packages..."
apt update && apt upgrade -y && apt autoremove -y

# 2. Create a non-root user with sudo privileges (check if exists)
read -p "Enter a username for the new user (e.g., deploy): " USERNAME
if id "$USERNAME" &>/dev/null; then
    echo "User $USERNAME already exists. Skipping user creation."
else
    useradd -m -s /bin/bash "$USERNAME"
    usermod -aG sudo "$USERNAME"
    echo "Set a strong password for $USERNAME:"
    passwd "$USERNAME"
fi

# 3. Configure SSH for security (check if already configured)
echo "Securing SSH..."
SSH_CONFIG="/etc/ssh/sshd_config"
if grep -q "^PermitRootLogin no" "$SSH_CONFIG"; then
    echo "SSH already secured. Skipping SSH config."
else
    sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' "$SSH_CONFIG"
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' "$SSH_CONFIG"
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' "$SSH_CONFIG"
    systemctl restart ssh
fi

# 4. Set up UFW firewall (check if enabled)
echo "Configuring UFW firewall..."
if ufw status | grep -q "Status: active"; then
    echo "UFW already active. Skipping firewall setup."
else
    ufw allow OpenSSH
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
fi

# 5. Install fail2ban (check if installed)
echo "Installing fail2ban..."
if dpkg -l | grep -q fail2ban; then
    echo "fail2ban already installed. Skipping."
else
    apt install fail2ban -y
    systemctl enable fail2ban
    systemctl start fail2ban
fi

# 6. Install Docker and Docker Compose (check if installed)
echo "Installing Docker..."
if command -v docker &> /dev/null; then
    echo "Docker already installed. Skipping."
else
    apt install apt-transport-https ca-certificates curl gnupg lsb-release -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt update
    apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
    systemctl start docker
    systemctl enable docker
fi

# Add user to docker group (check if already added)
if groups "$USERNAME" | grep -q docker; then
    echo "User $USERNAME already in docker group. Skipping."
else
    usermod -aG docker "$USERNAME"
fi

# Verify Docker and Docker Compose installation
echo "Verifying Docker and Docker Compose installation..."
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "✅ Docker and Docker Compose are properly installed"
    docker --version
    docker compose version
else
    echo "❌ Docker or Docker Compose installation failed"
    exit 1
fi

# 7. Prepare app directory (check if exists)
APP_DIR="/home/$USERNAME/ecommerce_backend"
if [ -d "$APP_DIR" ]; then
    echo "App directory $APP_DIR already exists. Skipping."
else
    mkdir -p "$APP_DIR"
    chown "$USERNAME:$USERNAME" "$APP_DIR"
fi

# 8. Install monitoring tools (check if installed)
if dpkg -l | grep -q htop; then
    echo "htop already installed. Skipping."
else
    apt install htop -y
fi

echo "Setup complete! Reboot the server if needed: sudo reboot"
echo "Next steps:"
echo "1. SSH in as $USERNAME (using your SSH key)."
echo "2. Copy your project files (docker-compose.yml, .env) to $APP_DIR."
echo "3. Test Docker Compose: docker compose version"
echo "4. Run: cd $APP_DIR && docker compose up -d"
echo "5. For SSL, consider Certbot: apt install certbot python3-certbot-nginx"
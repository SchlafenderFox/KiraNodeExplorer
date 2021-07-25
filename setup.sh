#!/bin/bash

# Installing docker-compose
apt install -y docker-compose

echo "[INFO] Getting local validator address..."
VALIDATOR_ADDR=$(timeout 30 echo $(docker exec -i validator /bin/bash -c ". /etc/profile;showAddress validator") | xargs || echo -n "")
if [ -z "$VALIDATOR_ADDR" ]
then
  echo "[ERROR] Can't get local validator address..."
  exit
fi

echo "Enter master server ip ( EXAMPLE: 127.0.0.1 )"
read MASTER_SERVER_IP

if [ -z "$MASTER_SERVER_IP" ]
then
  MASTER_SERVER_IP="127.0.0.1"
fi

echo "[INFO] MASTER_SERVER_IP set $MASTER_SERVER_IP"

echo "VALIDATOR_ADDR=$VALIDATOR_ADDR" > settings.env
echo "MASTER_SERVER_IP=$MASTER_SERVER_IP" >> settings.env

echo "[INFO] Starting node explorer..."
docker-compose up -d --build
echo "[INFO] Node explorer is up!"

echo "[INFO] Setting firewall rules..."

firewall-cmd --permanent --zone=validator --add-rich-rule='rule priority="-31000" family="ipv4" source address="0.0.0.0/0" port port="10100" protocol="tcp" accept'
echo "[INFO] Firewall rules set! Reloading firewall..."
firewall-cmd --reload
firewall-cmd --complete-reload

IP=$(curl ifconfig.co)
echo "[INFO] Firewall reloaded seccessful! Checking info on http://$IP:10100/metrics"
echo "[INFO] You can change any settings in settings.env file."
echo "[INFO] For apply your changes execute docker-compose up -d --build"

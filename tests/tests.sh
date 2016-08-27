#!/bin/bash
sudo apt-get -y install nginx
sudo cp ./tests/nginx.conf /etc/nginx/sites-enabled/test.frezbo.com
sudo mkdir -p /var/www/html/.well-known
sudo mkdir -p /var/www/html/.well-known/acme-challenge
sudo nginx -s reload
sudo ufw allow 80/tcp
ip=$(dig +short myip.opendns.com @resolver1.opendns.com)
curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records/$dns_record" -H "X-Auth-Email: $mail" -H "X-Auth-Key: $token" -H "Content-Type: application/json" -d "{\"id\":\"$zone_id\",\"type\":\"A\",\"name\":\"test.frezbo.com\",\"content\":\"$ip\"}" > /dev/null 2>&1
dig +short @8.8.8.8 A test.frezbo.com
sleep 120
openssl genrsa -out priv.key
openssl req -new -newkey rsa:2048 -nodes -subj "/CN=test.frezbo.com" -out sign.csr
rm -f privkey.pem
sudo python acme_tiny.py --no-verify --ca https://acme-staging.api.letsencrypt.org --account-key priv.key --csr sign.csr --acme-dir /var/www/html/.well-known/acme-challenge > test.crt
rm -f test.crt
#curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records/$dns_record" -H "X-Auth-Email: $mail" -H "X-Auth-Key: $token" -H "Content-Type: application/json" -d "{\"id\":\"$zone_id\",\"type\":\"A\",\"name\":\"test.frezbo.com\",\"content\":\"0.0.0.0\"}" > /dev/null 2>&1



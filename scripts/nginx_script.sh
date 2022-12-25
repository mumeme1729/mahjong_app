#! /bin/bash

 
openssl req -x509 -nodes -new -keyout server.key -out server.crt -days 365
 
COUNTRY=JP
STATE=Tokyo
LOCATION=Minato-Ku
COMMON_NAME=13.112.24.233
EMAIL_ADDRESS=sample@example.com 
CRT_DAYS=825

# openssl genrsa -aes128 2048 > server.key
# openssl req -new -key server.key > server.csr
#command="openssl req -x509 -nodes -new -keyout server.key -out server.crt -days 365"
# expect -c"
# spawn ${command}
# expect \"Country:\"
# send \"JP\n\"
# expect \"State or Province Name (full name) [Some-State]:\"
# send \"${STATE}\n\"
# expect \"Locality Name (eg, city) []:\"
# send \"${LOCATION}\n\"
# expect \"Organization Name (eg, company) [Internet Widgits Pty Ltd]:\"
# send \"NextDrive KK\n\"
# expect \"Organizational Unit Name (eg, section) []:\"
# send \"\n\"
# expect \"Common Name (e.g. server FQDN or YOUR name) []:\"
# send \"${COMMON_NAME}\n\"
# expect \"Email Address []:\"
# send \"${EMAIL_ADDRESS}\n\"
# exit 0
# "
# openssl x509 -in server.csr -days 365 -req -signkey server.key > server.crt
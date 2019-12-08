

CA_KEY=./pki/ca-key.pem
if [[ ! -f "$CA_KEY" ]]; then
    cfssl genkey --initca conf/openvpn-ca-csr.json | cfssljson -bare pki/ca
fi

SERVER_KEY=./pki/server-key.pem
if [[ ! -f "$SERVER_KEY" ]]; then
    cfssl gencert -ca pki/ca.pem -ca-key pki/ca-key.pem -config conf/openvpn-ca-config.json -profile="server" -hostname="server" conf/openvpn-server-csr.json | cfssljson -bare pki/server
fi

CLIENT_KEY=./pki/clients/client-key.pem
if [[ ! -f "$CLIENT_KEY" ]]; then
    cfssl gencert -ca pki/ca.pem -ca-key pki/ca-key.pem -config conf/openvpn-ca-config.json -profile="client" -hostname="client" conf/openvpn-client-csr.json | cfssljson -bare pki/clients/client
fi

TA_KEY=./pki/ta.key
if [[ ! -f "$TA_KEY" ]]; then
    openvpn --genkey --secret pki/ta.key
fi

DH_KEY=./pki/dh2048.pem
# DH_KEY=./pki/dh4096.pem
if [[ ! -f "$TA_KEY" ]]; then
    openssl genpkey -genparam -algorithm DH -pkeyopt dh_paramgen_prime_len:2048 -out pki/dh2048.pem 
    # openssl genpkey -genparam -algorithm DH -pkeyopt dh_paramgen_prime_len:4096 -out pki/dh4096.pem 
fi

cp -r pki/ ../data/




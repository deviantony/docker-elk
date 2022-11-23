#!/usr/bin/env bash

set -eu
set -o pipefail

declare symbol=⠍

echo '[+] CA certificate and key'

if [ ! -f tls/ca/ca.key ]; then
	symbol=⠿

	bin/elasticsearch-certutil ca \
		--silent \
		--pem \
		--out tls/ca.zip

	unzip tls/ca.zip -d tls/ >/dev/null
	rm tls/ca.zip

	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/ca/ca.crt \
	| cut -d '=' -f2 \
	| tr -d ':' \
	| tr '[:upper:]' '[:lower:]'
)"

echo "   ${symbol} SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
	echo "   ${symbol}   ${file}"
done < <(find tls/ca \( -name '*.crt' -or -name '*.key' \) -print)

symbol=⠍

echo '[+] Server certificates and keys'

if [ ! -f tls/elasticsearch/elasticsearch.key ]; then
	symbol=⠿

	bin/elasticsearch-certutil cert \
		--silent \
		--pem \
		--in tls/instances.yml \
		--ca-cert tls/ca/ca.crt \
		--ca-key tls/ca/ca.key \
		--out tls/certs.zip

	unzip tls/certs.zip -d tls/ >/dev/null
	rm tls/certs.zip

	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
	echo "   ${symbol}   ${file}"
done < <(find tls -name ca -prune -or \( -name '*.crt' -or -name '*.key' \) -print)

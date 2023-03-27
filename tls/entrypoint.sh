#!/usr/bin/env bash

set -eu
set -o pipefail

declare symbol=⠍

echo '[+] CA certificate and key'

if [ ! -f tls/certs/ca/ca.key ]; then
	symbol=⠿

	bin/elasticsearch-certutil ca \
		--silent \
		--pem \
		--out tls/certs/ca.zip

	unzip tls/certs/ca.zip -d tls/certs/ >/dev/null
	rm tls/certs/ca.zip

	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

declare ca_fingerprint
ca_fingerprint="$(openssl x509 -fingerprint -sha256 -noout -in tls/certs/ca/ca.crt \
	| cut -d '=' -f2 \
	| tr -d ':' \
	| tr '[:upper:]' '[:lower:]'
)"

echo "   ${symbol} SHA256 fingerprint: ${ca_fingerprint}"

while IFS= read -r file; do
	echo "   ${symbol}   ${file}"
done < <(find tls/certs/ca -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

symbol=⠍

echo '[+] Server certificates and keys'

if [ ! -f tls/certs/elasticsearch/elasticsearch.key ]; then
	symbol=⠿

	bin/elasticsearch-certutil cert \
		--silent \
		--pem \
		--in tls/instances.yml \
		--ca-cert tls/certs/ca/ca.crt \
		--ca-key tls/certs/ca/ca.key \
		--out tls/certs/certs.zip

	unzip tls/certs/certs.zip -d tls/certs/ >/dev/null
	rm tls/certs/certs.zip

	find tls -name ca -prune -or -type f -name '*.crt' -exec sh -c 'cat tls/certs/ca/ca.crt >>{}' \;

	echo '   ⠿ Created'
else
	echo '   ⠍ Already present, skipping'
fi

while IFS= read -r file; do
	echo "   ${symbol}   ${file}"
done < <(find tls -name ca -prune -or -type f \( -name '*.crt' -or -name '*.key' \) -mindepth 1 -print)

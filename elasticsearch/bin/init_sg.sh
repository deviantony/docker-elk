#!/bin/sh
plugins/search-guard-6/tools/sgadmin.sh \
	-cd config/sg/ \
	-ts config/sg/truststore.jks \
	-ks config/sg/kirk-keystore.jks \
	-nhnv \
	-icl

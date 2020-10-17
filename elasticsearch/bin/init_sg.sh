#!/usr/bin/env sh

plugins/search-guard-7/tools/sgadmin.sh \
	-cd config/sg/ \
	-ts config/sg/truststore.jks \
	-ks config/sg/kirk-keystore.jks \
	-nhnv \
	-icl

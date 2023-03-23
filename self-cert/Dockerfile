FROM alpine:3.14

RUN apk update && \
    apk add --no-cache openssl && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=US/ST=MA/O=CUAHSI/CN=self-signed" \
     -newkey rsa:2048 -keyout /etc/certs/self-signed.key \
     -out /etc/certs/self-signed.crt;

RUN openssl req -text -in /etc/certs/self-signed.crt -noout -verify
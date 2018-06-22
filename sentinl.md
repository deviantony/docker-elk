This page describes how to add [Sentinl](https://github.com/sirensolutions/sentinl) plugin to docker-elk.

### Install plugin

Add the following line to Kibana Dockerfile.

```
RUN kibana-plugin install https://github.com/sirensolutions/sentinl/releases/download/tag-{release}/sentinl-{release}.zip
```
**Check the [Sentinl releases table](https://github.com/sirensolutions/sentinl/releases)**

**Check the [Kibana config for Sentinl](http://sentinl.readthedocs.io/en/latest/Config-Example/) documentation page for Sentinl actions configuration.**

### Sentinl with SearchGuard

If you want to use docker-elk with Sentinl and SearchGuard, an extra [security configuration](https://docs.search-guard.com/latest/search-guard-sentinl) is required.

**Check the [Authenticate search request](http://sentinl.readthedocs.io/en/latest/Authentication/) documentation page for authentication configuration.**






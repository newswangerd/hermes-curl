# Hermes cURL

Hermes cURL is a lightweight wrapper on top of cURL that provides the ability to create reusable configurations for cURL. Configuration files can inherit configurations from other files which allows for common settings such as hostnames and authentication headers to be shared by multiple cURL configs.

## Usage

Base configuration for an entire API:

```yaml
# api_base.yml
headers:
  Authorization: Token MySecretAPIToken
  Content-Type: application/json
host: localhost:5000
curl_flags:
   "--location":
```

Configuration for a specific endpoint:

```yaml
#
from: api_base.yml
method: PUT
path: /my/api
body: >
  {"hello": "world"}
```

Run the `hermes` command:

```
$ hermes api_base.yml
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   128  100   112  100    16   3960    565 --:--:-- --:--:-- --:--:--  4000
{
   "msg": "hello Mr world"
}
```

## Configuration file reference

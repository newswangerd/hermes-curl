# Hermes cURL

Hermes cURL is a lightweight wrapper on top of cURL that provides reusable HTTP request configurations in YAML. Configuration files can import attributes from other files which allows for common settings such as hostnames and authentication headers to be shared by multiple cURL calls.

## Usage

Set up a base configuration for an entire API:

```yaml
# api_base.yml
headers:
  Authorization: Token MySecretAPIToken
  Content-Type: application/json
host: localhost:5000
curl_flags:
   "--location":
```

Set up a configuration for a specific endpoint and import our the base settings:

```yaml
# api.yml
from: api_base.yml
method: PUT
path: /my/api
body: >
  {"hello": "world"}
```

Run the `hermes` command:

```
$ hermes api.yml
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   128  100   112  100    16   3960    565 --:--:-- --:--:-- --:--:--  4000
{
   "msg": "hello Mr world"
}
```

See [examples](https://github.com/newswangerd/hermes-curl/tree/master/examples) for a working example.

## Installation

```
python3 -m pip install hermes-curl
```

## Configuration file reference

### Options

- `from` (optional): specify a path to another configuration file to inherit configurations from. This path is relative to the current file.
- `path` (requires): path on the server to send the request to, including any query params.
- `method` (required): HTTP method to use.
- `host` (required): server host, including protocol and port.
- `headers` (optional): dictionary of headers in the form. Ex`Header: value`.
- `body` (optional): request body.
- `curl_flags` (optional): a dictionary with any other curl flags to add. Ex `"--cacert: certfile"`.
- `template_defaults` (optional): a dictionary of default template variables.

### Config Inheritance

Configurations are merged in the following fashion:

- Dictionaries are merged. Values set in child configs having precedence and override
  any values from the parent configuration.
- `path` is concatenated, so setting `path: /foo/` in the parent and `path: /bar/`
  in the child will result in `path: /foo/bar/`
- All other top level configurations use whatever value is set in the child configuration.
  This includes `method`, `body`, and `host`.

### Template Variables

Configurations can contain variables using the `{variable_name}` syntax. Variables can
be passed into the configuration by either setting `-t variable_name=value` on the cli
or by setting `template_defaults` in the configuration. Values passed on the cli have
precedence over values set in `template_defaults.`

#### Example

```yaml
host: http://localhost/
path: api/thing/{pk}/
method: GET
template_defaults:
  pk: 1
```

Running `hermes -t pk=2 example.yml` will `GET http://localhost/api/thing/2/` and running
`hermes example.yml` will `GET http://localhost/api/thing/1/`

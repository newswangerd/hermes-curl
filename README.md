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

To see a working example:

Clone this repo: `git clone git@github.com:newswangerd/hermes-curl.git`

Make a simple get request: `hermes hermes-curl/examples/chuck_norris_random.yaml`

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   327    0   327    0     0    616      0 --:--:-- --:--:-- --:--:--   616
{
  "categories": [],
  "created_at": "2020-01-05 13:42:22.980058",
  "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
  "id": "wP7Jfz4CQLWDHQgLIMftiQ",
  "updated_at": "2020-01-05 13:42:22.980058",
  "url": "https://api.chucknorris.io/jokes/wP7Jfz4CQLWDHQgLIMftiQ",
  "value": "Chuck Norris once downloaded the entire Internet"
}
GET: https://api.chucknorris.io/jokes/random/
```

Pass in a template variable to get the "animals" category: `hermes -t category=animal hermes-curl/examples/chuck_norris_category.yaml`

```
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                               Dload  Upload   Total   Spent    Left  Speed
100   376    0   376    0     0    673      0 --:--:-- --:--:-- --:--:--   673
{
"categories": [
  "animal"
],
"created_at": "2020-01-05 13:42:19.576875",
"icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
"id": "xwjic1sws_yohsfefndaiw",
"updated_at": "2020-01-05 13:42:19.576875",
"url": "https://api.chucknorris.io/jokes/xwjic1sws_yohsfefndaiw",
"value": "Chuck Norris once kicked a horse in the chin. Its decendants are known today as Giraffes."
}
GET: https://api.chucknorris.io/jokes/random?category=animal
```

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

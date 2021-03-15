# Examples

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

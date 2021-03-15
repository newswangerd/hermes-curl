import yaml
import argparse
import os
import json
import urllib.parse

from pathlib import Path


class Config:

    def __init__(self, config, templates):
        self._config = config
        self._cli_templates = self.load_templates(templates)
        self._config_templates = self._config.get('template_defaults', {})

    def load_templates(self, templates):
        t = {}
        if templates is None:
            return t
        for x in templates:
            vals = x.split('=')
            t[vals[0]] = vals[1]
        return t

    def __getitem__(self, key):
        # return config item with all {templated} items rendered
        # cli flags have prescendece
        merged_template = {**self._config_templates, **self._cli_templates}
        item = self._config[key]
        try:
            return item.format(**merged_template)
        except KeyError as e:
            variable = str(e).replace("'", "")
            print(f"A template variable '{variable}' was set in '{key}', but no value "
                  f"has been configured for it. Either pass '-t {variable}=<value>' or "
                  f"set '{variable}' under 'template_defaults'")
            exit(1)

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)


def pars_args():
    parser = argparse.ArgumentParser(description='Run curl from simple yaml configurations.')
    parser.add_argument('config', nargs=1, help='Configuration file to use.')
    parser.add_argument('--print', '-p', action='store_true', dest='print_cmd', help='Print the curl command instead of executing it.')
    parser.add_argument('-v', action='store_true', dest='verbose', help='Verbose.')
    parser.add_argument('--template', '-t', type=str, action='append', dest='template_vars', help='Specify values for templated variables.')

    return parser.parse_args()


def get_headers(config):
    header_vals = []
    headers = config.get('headers', {})
    for header in headers:
        header_vals.append("-H '{header}: {value}'".format(header=header, value=headers[header]))

    return ' '.join(header_vals)


def get_curl_flags(config):
    flag_vals = []
    flags = config.get('flags', {})

    for flag in flags:
        flag_vals.append("{flag} {value}".format(flag=flag, value=flags[flag]))

    return ' '.join(flags)


def merge_config(parent, child):
    '''
    Merges two configs together. Values set in the child take prescendece over
    values in the parent.
    '''

    # Merge paths by concatenating them.
    if parent.get('path') and child.get('path'):
        print("merging path")
        child['path'] = urllib.parse.urljoin(parent['path'], child['path'])
        print(child['path'])

    merged = {**parent, **child}

    for val in merged:
        if isinstance(merged[val], dict):
            merged[val] = {**parent.get(val, {}), **child.get(val, {})}

    return merged


def load_config(config_file, child_config={}):
    config = {}
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    if config.get('from'):
        from_path = os.path.join(Path(config_file).parent, config.get('from'))
        parent_config = load_config(from_path, config)
        del config['from']
        return merge_config(parent_config, config)

    return config


def main():
    args = pars_args()

    config = Config(
        load_config(os.path.join(os.getcwd(), args.config[0])),
        args.template_vars
    )

    body = config.get('body', '').strip()
    headers = get_headers(config)
    curl_flags = get_curl_flags(config)

    try:
        url = urllib.parse.urljoin(config['host'], config['path'])
        method = config['method']
    except KeyError:
        print("Host, path and method must be set.")
        exit(1)

    curl_cmd = [
        'curl',
        '-X ' + method,
    ]

    if (body != ''):
        curl_cmd.append("-d '{body}'".format(body=body))
    if (headers != ''):
        curl_cmd.append(headers)
    if (curl_flags != ''):
        curl_cmd.append(curl_flags)

    curl_cmd.append(url)

    if (args.print_cmd):
        print(' \\\n  '.join(curl_cmd))
        exit(0)

    cmd = ' '.join(curl_cmd)
    if args.verbose:
        print('Curl Command:')
        print(cmd)
        print('Parsed Config:')
        print(json.dumps(config, indent=2))

    stream = os.popen(cmd)
    for line in stream.readlines():
        try:
            print(json.dumps(json.loads(line), indent=2))
        except json.decoder.JSONDecodeError:
            print(line)

    print(f"{method}: {url}")

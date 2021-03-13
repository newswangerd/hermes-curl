import yaml
import argparse
import os
import json

from pathlib import Path


def pars_args():
    parser = argparse.ArgumentParser(description='Run curl from simple yaml configurations.')
    parser.add_argument('config', nargs=1, help='Configuration file to use.')
    parser.add_argument('--print', '-p', action='store_true', dest='print_cmd', help='Print the curl command instead of executing it.')
    parser.add_argument('-v', action='store_true', dest='verbose', help='Verbose.')

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

    config = load_config(os.path.join(os.getcwd(), args.config[0]))

    body = config.get('body', '').strip()
    headers = get_headers(config)
    curl_flags = get_curl_flags(config)

    try:
        url = config['host'] + config['path']
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

    print(f"{method}: {url}")
    stream = os.popen(cmd)
    for line in stream.readlines():
        try:
            print(json.dumps(json.loads(line), indent=2))
        except json.decoder.JSONDecodeError:
            print(line)

#!/usr/bin/env python3
import requests
import json
import os

cf_email = os.environ['CF_EMAIL']
cf_key = os.environ['CF_KEY']
base_url = "https://api.cloudflare.com/client/v4/zones/"
checkip_url = "https://api.ipify.org"
IP = requests.get(checkip_url).text

cf_headers = {
    'X-Auth-Email': cf_email,
    'X-Auth-Key': cf_key,
    'Content-Type': 'application/json'
}


def get_zones():
    req = json.loads(requests.get(base_url, headers=cf_headers).text)
    zones = {}
    for n in req['result']:
        if n['original_registrar'] is None:
            zones[n['name']] = n['id']
    return zones


def get_dns(zone):
    url = base_url + zone + "/dns_records"
    return requests.get(url, headers=cf_headers).text


def update_dns(zone):
    dns = json.loads(get_dns(zone))
    for n in dns['result']:
        url = base_url + zone + "/dns_records/" + n['id']
        cf_update_body = {
            'type': 'A',
            'name': n['name'],
            'content': IP
        }
        requests.put(url, headers=cf_headers, data=json.dumps(cf_update_body))


for key, value in get_zones().items():
     update_dns(value)

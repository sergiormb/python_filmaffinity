#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random


def get_random_proxy():
    proxy = {}
    response = requests.get("https://www.sslproxies.org/")
    soup = BeautifulSoup(response.text, "html.parser")
    https_proxies = list(filter(
        lambda item: "yes" in item.text,
        soup.select("table.table tr")
    ))
    if https_proxies:
        http_proxy = https_proxies[0]
        proxy = {'http': 'https://{}:{}'.format(
            http_proxy.select_one("td").text,
            http_proxy.select_one("td:nth-of-type(2)").text,
        )}
    return proxy

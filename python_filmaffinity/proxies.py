#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random


def get_random_proxy():
    response = requests.get("https://www.sslproxies.org/")
    soup = BeautifulSoup(response.text, "html.parser")
    https_proxies = filter(
        lambda item: "yes" in item.text,
        soup.select("table.table tr")
    )
    http_proxy = random.choice(https_proxies)
    return {'http': 'https://{}:{}'.format(
        http_proxy.select_one("td").text,
        http_proxy.select_one("td:nth-of-type(2)").text,
    )}

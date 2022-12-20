#!/usr/bin/env python

import configparser
from os.path import join
from os import getenv

credentials_path = join(getenv('HOME'), '.aws/credentials')

current_config = configparser.ConfigParser()
current_config.read(credentials_path)

print("Choose a profile:")

profiles = sorted(current_config.sections())

for index, profile in enumerate(profiles):
    print(f"{index}) {profile}")

option = int(input())

current_config['default'] = current_config[profiles[option]]

new_config = configparser.ConfigParser()

profiles = sorted(current_config.sections())

for profile in profiles:
    new_config[profile] = current_config[profile]

with open(credentials_path, 'w') as credentials_file:
    new_config.write(credentials_file)

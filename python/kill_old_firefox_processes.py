#!/usr/bin/env python

import shlex
import subprocess
import re
import sys
from datetime import datetime, timedelta

try:
    ps = subprocess.Popen(shlex.split("ps -A -o pid -o comm -c -o lstart"), stdout=subprocess.PIPE)
    output = subprocess.check_output(shlex.split("grep [f]irefox"), stdin=ps.stdout)
    ps.wait()
except Exception as e:
    sys.exit('No Firefox processes found')

now_datetime = datetime.now()

lines = output.splitlines()
for line in lines:
    pid, comm, lstart = re.split(r'\s+', line.strip(), 2)

    start_datetime = datetime.strptime(lstart, '%a %b %d %H:%M:%S %Y')
    elapsed_time = now_datetime - start_datetime
    if elapsed_time > timedelta(minutes=60):
        subprocess.Popen(shlex.split("kill -9 {}".format(pid)))

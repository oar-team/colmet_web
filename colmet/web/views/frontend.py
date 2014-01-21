# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import pandas
import vincent

from flask import Blueprint, current_app, render_template
from ..extensions import cache

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return render_template('/index.html.jinja2')


@frontend.route('/vega.json')
@cache.cached()
def vega_json():
    with pandas.get_store(current_app.config['HDF5_PATH']) as store:
        df = store['/job_0/metrics'].query('hostname == "frog138"')
        df['timestamp'] = pandas.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)
        columns = ["meminfo_active", "meminfo_inactive", "meminfo_dirty",
                   "meminfo_cached", "meminfo_kernelstack",
                   "meminfo_memfree", "meminfo_memtotal",
                   "meminfo_writeback"]
        line = vincent.Line(df.sort().tail(1000)[columns])
        line.axis_titles(x='Time', y='Value')
        line.legend(title='Memory')
        return line.to_json()

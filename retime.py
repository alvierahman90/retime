#!/usr/bin/env python3

import sys
import jinja2
import requests
import tomllib
import os
from pathlib import Path
from datetime import datetime as dt

SECONDS_PER_DAY = 24 * 3600

XML_TEMPLATE_STR = """<!-- generated by retime (git.alv.cx/alvierahman90/retime)-->
<background>
    <starttime>
    <year>{{ start.year }}</year>
    <month>{{ start.month }}</month>
    <day>{{ start.day }}</day>
    <hour>{{ start.hour }}</hour>
    <minute>{{ start.minute }}</minute>
    <second>{{ start.second }}</second>
    </starttime>

    {% for image in images %}
    <static>
        <file>{{ image['path'] }}</file>
        <duration>{{ image['duration'] }}</duration>
    </static>
    <transition type="overlay">
        <duration>{{ transition_duration }}</duration>
        <from>{{ image['path'] }}</from>
        <to>{% if loop.last %}{{ images[0]['path'] }}{% else %}{{ loop.nextitem['path'] }}{% endif %}</to>
    </transition>
    {% endfor %}
    </background>
"""

XML_TEMPLATE = jinja2.Environment(
        loader=jinja2.FunctionLoader(lambda name: XML_TEMPLATE_STR),
        autoescape=jinja2.select_autoescape(),
        ).get_template("")



def get_args():
    """ Get command line arguments """

    xdg_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_home is None:
        print("Set XDG_CONFIG_HOME or specify config file")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, default=Path(xdg_home).joinpath('retime').joinpath('config.toml'))
    parser.add_argument("wallpaper", type=Path)
    return parser.parse_args()


def get_weather_data(latitude, longitude):
    return requests.get("https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": "sunrise,sunset,daylight_duration,sunshine_duration",
            "timeformat": "unixtime",
            "forecast_days": 1,
        }).json()

def get_timings(latitude, longitude, sunrise_sunset_duration):
    weather_data = get_weather_data(latitude, longitude)

    sunrise_time = weather_data['daily']['sunrise'][0]
    sunset_time = weather_data['daily']['sunset'][0]

    sunrise_duration = sunrise_sunset_duration
    sunrise_start = sunrise_time - 0.5*sunrise_duration
    sunrise_end = sunrise_time + 0.5*sunrise_duration
    sunset_duration = sunrise_sunset_duration
    sunset_start = sunset_time - 0.5*sunset_duration
    sunset_end = sunset_time + 0.5*sunset_duration

    day_duration = sunset_start - sunrise_end
    night_duration = SECONDS_PER_DAY - sunset_duration - day_duration - sunrise_duration

    print(f"{sunrise_sunset_duration=} {sunrise_start=} {sunrise_end=} {sunset_start=} {sunset_end=}")

    return {
            # we start time from the start of sunset
            'start_time': sunrise_start,
            # the rest are durations
            'sunrise': sunrise_duration,
            'day': day_duration,
            'sunset': sunset_duration,
            'night': night_duration,
            }

def generate_xml(wallpaper_path, timings, transition_duration):
    start = dt.fromtimestamp(timings['start_time'])
    config = tomllib.loads(wallpaper_path.joinpath('retime.toml').read_text())
    images = []

    for time_of_day in [ 'sunrise', 'day', 'sunset', 'night' ]:
        for image_path in config[time_of_day]:
            images.append({
                    'path': str(wallpaper_path.joinpath(image_path).absolute()),
                    'duration': float(timings[time_of_day]/len(config[time_of_day])) - transition_duration
                })

    return XML_TEMPLATE.render(start=start, images=images, transition_duration=float(transition_duration))

def main(args):
    """ Entry point for script """
    config = tomllib.loads(args.config.read_text())
    sunrise_sunset_duration = config.get('sunrise-sunset-duration', 3600)
    transition_duration = config.get('transition-duration', 5)
    timings = get_timings(
            config['latitude'],
            config['longitude'],
            sunrise_sunset_duration,
            )
    print(f"{config=} {timings=}")
    args.wallpaper.with_suffix('.xml').write_text(generate_xml(args.wallpaper, timings, transition_duration))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(get_args()))
    except KeyboardInterrupt:
        sys.exit(0)

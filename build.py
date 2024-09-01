#!/usr/bin/env python3
import pathlib
import subprocess

output_dir = pathlib.Path("output")

from jinja2 import Environment, FileSystemLoader, select_autoescape

output_dir.mkdir(exist_ok=True)

subprocess.run("npm run build", check=True, shell=True)

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape(),
)

LOGO_WIDTH = 424
LOGO_HEIGHT = 200
RESIZE_RATIO = 1 / 4
template = env.get_template("data/logo.svg.j2")
logo = template.render(
    dict(
        width=int(LOGO_WIDTH * RESIZE_RATIO),
        height=int(LOGO_HEIGHT * RESIZE_RATIO),
    )
)

template = env.get_template("data/status.html.j2")
with open(output_dir / "status.html", "w") as f:
    f.write(template.render(
        dict(
            logo=logo,
        )
    ))

template = env.get_template("data/configs.html.j2")
with open(output_dir / "configs.html", "w") as f:
    f.write(template.render(
        dict(
            logo=logo,
        )
    ))

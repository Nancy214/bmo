__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import requests
import logging
from pathlib import Path

import bmo.helpers.notion

import typer

app = typer.Typer()

@app.command("weekly_email")
def notion_weekly_progress(token: str = typer.Argument("", envvar="NOTION_TOKEN")):
    """Do the sync with notion."""
    if not token:
        logging.error("Empty token. Add `--help` to usage.")
        return
    notion = bmo.helpers.notion.Notion(token)
    notion.weekly_update()



if __name__ == "__main__":
    app()

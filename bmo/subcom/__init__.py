__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import requests
import logging
from datetime import datetime
from pathlib import Path

from envelops import Envelope

import bmo.helpers.notion

import typer

app = typer.Typer()


@app.command("weekly_email")
def notion_weekly_progress(
    token: str = typer.Argument("", envvar="NOTION_TOKEN"),
    smtp_password: str = typer.Argument("", envvar="SUBCOM_SMTP_PASSWORD"),
    to: str = typer.Option("all@subcom.tech"),
):
    """This week in SubCom delivered to your INBOX."""
    if not token:
        logging.error("Empty token. Add `--help` to usage.")
        return
    if not smtp_password:
        logging.error("Empty SMTP password. See `--help`")
        return

    notion = bmo.helpers.notion.Notion(token)
    html = notion.weekly_update()

    # create an email and send it.
    sender_email = "noreply@subconscious.co.in"
    weekno = datetime.today().isocalendar()[1]
    subject = f"SubCom Weekly #{weekno}"
    envelope = Envelope(
        from_addr=(sender_email, "Subconscious Bot"),
        to_addr=to,
        subject=subject,
        html_body=html,
    )

    envelope.send("mail.subconcious.co.in", login=sender_email, password=smtp_password)


if __name__ == "__main__":
    app()

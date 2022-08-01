__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import requests
import logging
from datetime import datetime
from pathlib import Path

from envelopes import Envelope

import bmo.helpers.notion

import typer

app = typer.Typer()


@app.command("weekly_email")
def notion_weekly_progress(
    token: str = typer.Argument("", envvar="NOTION_TOKEN"),
    password: str = typer.Option(...),
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

    # create an email and send it. Don't send duplicates.
    emaildir = Path.home() / ".cache" / "bmo"
    emaildir.mkdir(parents=True, exists_ok=True)
    h = bmo.command.hash256(html)
    hfile = emaildir / h
    if h.exists():
        logging.warn("Email already sent.")
        return

    sender_email = "noreply@subconscious.co.in"
    weekno = datetime.today().isocalendar()[1]
    subject = f"SubCom Weekly #{weekno}"
    envelope = Envelope(
        from_addr=(sender_email, "BMO"),
        to_addr=to,
        subject=subject,
        html_body=html,
    )

    envelope.send("mail.subconscious.co.in", login=sender_email, password=password)
    # write the hash to disk.
    with hfile.open() as f:
        f.write(h)


if __name__ == "__main__":
    app()

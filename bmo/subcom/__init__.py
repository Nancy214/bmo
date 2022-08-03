__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import logging

from datetime import datetime
from pathlib import Path
import toml

from envelopes import Envelope

import bmo.common
import bmo.helpers.notion

import typer

app = typer.Typer()


@app.command()
def weekly_email(
    to: str = typer.Option("all@subcom.tech"),
    config: str = typer.Option(..., callback=bmo.common.conf_callback, is_eager=True),
    notion_token: str = typer.Option(""),
    smtp_server: str = typer.Option(""),
    smtp_username: str = typer.Option(""),
    smtp_password: str = typer.Option(...),
):
    """This week in SubCom delivered to your INBOX."""
    if not token:
        logging.error("Empty token. Add `--help` to usage.")
        return

    print(smtp_server, smtp_username, smtp_password)
    quit()

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

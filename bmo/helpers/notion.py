# Notion related functions.

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import logging
import requests
from datetime import datetime, timezone
import dateutil
import pprint
import json

import typing as T
from pathlib import Path

_pprint = pprint.pprint


class Notion:
    """Notion related functions."""

    def __init__(self, token: str):
        self.token = token
        self.backup_dir: T.Optional[str] = None

    def _headers(self):
        assert self.token
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-02-22",
            "Content-Type": "application/json",
        }

    def _url(self, endpoint: str) -> str:
        return f"https://api.notion.com/v1/{endpoint}"

    def post(self, endpoint: str, payload={}):
        response = requests.post(
            self._url(endpoint), headers=self._headers(), json=payload
        )
        assert response.ok, response.text
        return response.json()["results"]

    def get(self, endpoint: str):
        response = requests.get(self._url(endpoint), headers=self._headers())
        assert response.ok, response.text
        return response.json()["results"]

    def backup(self, outdir: T.Optional[Path]):
        """Backup notion content"""
        assert self.token is not None, "Token can't be None or empty"
        timestamp = datetime.now().isoformat()

        folder = Path.home() / "backups" / Path(f"notion_backup-{timestamp}")
        if outdir is not None:
            folder = Path(outdir)
        folder.mkdir(parents=True)

        logging.info(f"Creating backup into {folder}")
        # replace YOUR_INTEGRATION_TOKEN with your own secret token
        response = self.post("search")
        for block in response:
            with open(f'{folder}/{block["id"]}.json', "w") as file:
                file.write(json.dumps(block))

            child_blocks = self.get(f'blocks/{block["id"]}/children')
            if child_blocks:
                datadir = folder / f'{block["id"]}'
                datadir.mkdir()

                for child in child_blocks:
                    with open(datadir / f'{child["id"]}.json', "w") as file:
                        file.write(json.dumps(child))
        logging.info("backup is complete")

    def _weekly_update(self, dbid: str):
        """Results for a database"""
        payload = dict(page_size=100)
        return self.post(f"databases/{dbid}/query", payload=payload)

    def weekly_update(self):
        """Show weekly updates."""
        logging.info("Weekly update")
        pages = self._weekly_update("0d4a63a495f84fd0bd9632c82e0963b8")
        for page in pages:
            let = dateutil.parser.parse(page['last_edited_time'])
            if (datetime.now(timezone.utc) - let).days < 7:
                print(page['url'], let)
        _pprint(pages[-1])

import os

import pytest


@pytest.fixture(scope="session")
def scraper_config():
    os.environ["Environment"] = "production"

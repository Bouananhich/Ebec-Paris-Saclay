"""Supercharged requests to handle errors from the API."""
import requests


class supercharged_requests(requests.Session):
    """Base class for supercharged_requests."""

    def __init__(self):
        super().__init__()

    def supercharged_get(self, **kwargs):
        """."""
        return self.get(**kwargs)

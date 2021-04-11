"""Supercharged requests to handle errors from the API."""
import requests


class supercharged_requests(requests.Session):
    """Base class for supercharged_requests."""

    def __init__(self):
        """Add custome methods on requests."""
        super().__init__()

    def supercharged_get(self, **kwargs):
        """Handle empty json return."""
        return self.get(**kwargs)

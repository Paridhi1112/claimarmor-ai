import google.auth
from google.auth.credentials import Credentials

class DummyCredentials(Credentials):
    def __init__(self):
        super().__init__()
        self.token = "dummy-token"
    def refresh(self, request):
        pass

def mock_default(*args, **kwargs):
    return DummyCredentials(), "dummy-project"

google.auth.default = mock_default

import pytest
from services import mistral_service
from mistralai.models.sdkerror import SDKError

class _FakeChat:
    def __init__(self, resp=None, err=None):
        self._resp = resp
        self._err = err
    def complete(self, *a, **k):
        if self._err:
            raise self._err
        return self._resp

class _FakeChoice:
    def __init__(self, content): self.message = type("M", (), {"content": content})

class _FakeResponse:
    def __init__(self, content): self.choices = [_FakeChoice(content)]

class _FakeClient:
    def __init__(self, resp=None, err=None):
        self.chat = _FakeChat(resp=resp, err=err)

def test_mistral_success(monkeypatch):
    fake_client = _FakeClient(resp=_FakeResponse("OK"))
    monkeypatch.setattr(mistral_service, "client", fake_client, raising=True)
    out = mistral_service.ask_mistral([{"role":"user","content":"Hello"}])
    assert out == "OK"

def test_mistral_500_raises_sdkerror(monkeypatch):
    fake_client = _FakeClient(err=SDKError("boom", status_code=500))
    monkeypatch.setattr(mistral_service, "client", fake_client, raising=True)
    with pytest.raises(SDKError):
        mistral_service.ask_mistral([{"role":"user","content":"X"}])

def test_mistral_unexpected_raises_sdkerror(monkeypatch):
    fake_client = _FakeClient(err=SDKError("unexpected", status_code=200))
    monkeypatch.setattr(mistral_service, "client", fake_client, raising=True)
    with pytest.raises(SDKError):
        mistral_service.ask_mistral([{"role":"user","content":"X"}])

def test_mistral_timeout_like(monkeypatch):
    # Le SDK remonte aussi des SDKError → on simule un timeout via SDKError
    fake_client = _FakeClient(err=SDKError("timeout"))
    monkeypatch.setattr(mistral_service, "client", fake_client, raising=True)
    with pytest.raises(SDKError):
        mistral_service.ask_mistral([{"role":"user","content":"X"}])

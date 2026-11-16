from payments.client import PaymentClient


class FakeResponse:
    def __init__(self, status, body):
        self.status_code = status
        self._body = body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._body


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


def test_charge_returns_charge_id():
    session = FakeSession([FakeResponse(200, {"id": "ch_1"})])
    client = PaymentClient("key", session=session)
    assert client.charge("cus_1", 500) == "ch_1"

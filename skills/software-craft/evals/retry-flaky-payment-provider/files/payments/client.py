import requests

API = "https://api.payments-provider.example/v1"


class PaymentClient:
    def __init__(self, api_key, session=None):
        self.api_key = api_key
        self.session = session or requests.Session()

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    def charge(self, customer_id, amount_cents, currency="EUR"):
        """Charge a customer and return the provider's charge id."""
        resp = self.session.post(
            f"{API}/charges",
            json={"customer": customer_id, "amount": amount_cents, "currency": currency},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def refund(self, charge_id):
        resp = self.session.post(f"{API}/refunds", json={"charge": charge_id}, headers=self._headers())
        resp.raise_for_status()
        return resp.json()["id"]

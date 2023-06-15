import requests
from typing import Any
from dataclasses import dataclass


@dataclass(frozen=True)
class GetQuoteCommand:
    annual_revenue: int
    enterprise_number: str
    legal_name: str
    natural_person: bool
    nacebel_codes: list[str]

    def __post_init__(self):
        assert self.annual_revenue > 0, "Annual revenue must be greater than 0"
        assert (
            len(self.enterprise_number) >= 10
        ), "Enterprise number length must be equal to 10"
        assert len(self.legal_name) > 0, "Legal name length must be greater than 0"
        assert len(self.nacebel_codes) > 0, "NACEBEL codes must be provided"

    def to_dict(self):
        return {
            "annualRevenue": self.annual_revenue,
            "enterpriseNumber": self.enterprise_number,
            "legalName": self.legal_name,
            "naturalPerson": self.natural_person,
            "nacebelCodes": self.nacebel_codes,
        }


@dataclass(frozen=True)
class GrossPremiums:
    after_delivery: float
    public_liability: float
    professional_indemnity: float
    entrusted_objects: float
    legal_expenses: float

    @staticmethod
    def from_dict(data: dict[str, Any]):
        return GrossPremiums(
            after_delivery=data["afterDelivery"],
            public_liability=data["publicLiability"],
            professional_indemnity=data["professionalIndemnity"],
            entrusted_objects=data["entrustedObjects"],
            legal_expenses=data["legalExpenses"],
        )


@dataclass(frozen=True)
class Quote:
    available: bool
    coverage_ceiling: int
    deductible: int
    quote_id: str
    gross_premiums: GrossPremiums

    @staticmethod
    def from_dict(data: dict[str, Any]):
        return Quote(
            available=data["available"],
            coverage_ceiling=data["coverageCeiling"],
            deductible=data["deductible"],
            quote_id=data["quoteId"],
            gross_premiums=GrossPremiums.from_dict(data["grossPremiums"]),
        )


class InsurerError(Exception):
    pass


class InsurerService:
    def __init__(self, base_url: str, api_key: str) -> None:
        assert len(base_url) != 0
        assert len(api_key) != 0

        self.__base_url = base_url
        self.__api_key = api_key

    def get_quote(self, cmd: GetQuoteCommand):
        try:
            resp = requests.post(
                f"{self.__base_url}/quotes/professional-liability",
                json=cmd.to_dict(),
                headers={
                    "x-api-key": self.__api_key,
                    "Content-Type": "application/json",
                },
                timeout=10,
            )
            resp.raise_for_status()

            json_resp = resp.json()
            if not json_resp["success"]:
                raise InsurerError(json_resp["message"])

            return Quote.from_dict(json_resp["data"])

        except Exception as e:
            raise InsurerError(e)

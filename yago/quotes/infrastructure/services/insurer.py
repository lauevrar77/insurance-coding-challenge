from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class GetQuoteCommand:
    annual_revenue: int
    enterprise_number: str
    legal_name: str
    natural_person: bool
    nacebel_codes: list[str]
    deductible_formula: str
    coverage_ceiling_formula: str

    def __post_init__(self):
        assert self.annual_revenue > 0, "Annual revenue must be greater than 0"
        assert (
            len(self.enterprise_number) >= 10
        ), "Enterprise number length must be equal to 10"
        assert len(self.legal_name) > 0, "Legal name length must be greater than 0"
        assert len(self.nacebel_codes) > 0, "NACEBEL codes must be provided"
        assert self.deductible_formula in [
            "S",
            "M",
            "L",
        ], "Deductible formula must be S, M or L"
        assert self.coverage_ceiling_formula in [
            "S",
            "L",
        ], "Coverage ceiling formula must be S, M or L"

    def to_dict(self):
        size_converter = {
            "S": "small",
            "M": "medium",
            "L": "large",
        }
        return {
            "annualRevenue": self.annual_revenue,
            "enterpriseNumber": self.enterprise_number,
            "legalName": self.legal_name,
            "naturalPerson": self.natural_person,
            "nacebelCodes": self.nacebel_codes,
            "deductibleFormula": size_converter[self.deductible_formula],
            "coverageCeilingFormula": size_converter[self.coverage_ceiling_formula],
        }


@dataclass(frozen=True)
class GrossPremium:
    cover: str
    premium: float


@dataclass(frozen=True)
class Quote:
    available: bool
    coverage_ceiling: int
    deductible: int
    quote_id: str
    gross_premiums: list[GrossPremium]

    @staticmethod
    def from_dict(data: dict[str, Any]):
        return Quote(
            available=data["available"],
            coverage_ceiling=data["coverageCeiling"],
            deductible=data["deductible"],
            quote_id=data["quoteId"],
            gross_premiums=[
                GrossPremium(
                    cover=key,
                    premium=value,
                )
                for key, value in data["grossPremiums"].items()
            ],
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

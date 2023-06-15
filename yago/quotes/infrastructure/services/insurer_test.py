import pytest
from .insurer import GetQuoteCommand


def test_quote_command(subtests):
    with subtests.test("valid command"):
        cmd = GetQuoteCommand(1000, "123", "test", True, ["A", "B", "C"])

        assert cmd.annual_revenue == 1000
        assert cmd.enterprise_number == "123"
        assert cmd.legal_name == "test"
        assert cmd.natural_person
        assert cmd.nacebel_codes == ["A", "B", "C"]

    with subtests.test("invalid revenue"):
        with pytest.raises(AssertionError):
            GetQuoteCommand(-1000, "123", "test", True, ["A", "B", "C"])

    with subtests.test("invalid enterprise number"):
        with pytest.raises(AssertionError):
            GetQuoteCommand(1000, "", "test", True, ["A", "B", "C"])

    with subtests.test("invalid legal name"):
        with pytest.raises(AssertionError):
            GetQuoteCommand(1000, "123", "", True, ["A", "B", "C"])

    with subtests.test("invalid naecebel codes"):
        with pytest.raises(AssertionError):
            GetQuoteCommand(1000, "123", "", True, [])

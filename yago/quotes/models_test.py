from .models import NacebelCode, NacebelCodeAdvice, NacebelCodeCoverAdvice, QuoteAdvice


def test_quote_advice(
    db,
):  # This unused argument is for database instantiation by pytest-django
    # Prepare
    code1 = NacebelCode(
        level=5,
        code="12345",
        parent_code="1234",
        label_fr="test",
        label_nl="test",
        label_en="test",
        label_de="test",
    )
    code1.save()
    code2 = NacebelCode(
        level=5,
        code="22345",
        parent_code="2234",
        label_fr="test",
        label_nl="test",
        label_en="test",
        label_de="test",
    )
    code2.save()
    advice1 = NacebelCodeAdvice(
        nacebel_code=code1,
        deductibleFormula="S",
        coverageCeilingFormula="L",
    )
    advice1.save()
    advice2 = NacebelCodeAdvice(
        nacebel_code=code2,
        deductibleFormula="L",
        coverageCeilingFormula="S",
    )
    advice2.save()
    cover_advice1 = NacebelCodeCoverAdvice(nacebel_code_advice=advice1, cover="cover1")
    cover_advice1.save()
    cover_advice2 = NacebelCodeCoverAdvice(nacebel_code_advice=advice2, cover="cover2")
    cover_advice2.save()

    # Exercise
    advice = QuoteAdvice([advice1, advice2])

    # Test
    assert set(advice.covers) == {"cover1", "cover2"}
    assert advice.coverage_ceiling_formula == "L"
    assert advice.deductible_formula == "L"

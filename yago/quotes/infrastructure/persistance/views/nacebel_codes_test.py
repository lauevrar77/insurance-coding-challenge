from quotes.infrastructure.persistance.views.nacebel_codes import (
    NacebelCodeTree,
    NacebelCodeView,
)
from quotes.models import NacebelCode


def test_codes_as_tree(db):
    # Prepare
    code1 = NacebelCode(
        level=1,
        code="1",
        parent_code="",
        label_fr="test",
        label_nl="test",
        label_en="test",
        label_de="test",
    )
    code1.save()
    code11 = NacebelCode(
        level=2,
        code="11",
        parent_code="1",
        label_fr="test1",
        label_nl="test1",
        label_en="test1",
        label_de="test1",
    )
    code11.save()
    code12 = NacebelCode(
        level=2,
        code="12",
        parent_code="1",
        label_fr="test2",
        label_nl="test2",
        label_en="test2",
        label_de="test2",
    )
    code12.save()
    code111 = NacebelCode(
        level=3,
        code="111",
        parent_code="11",
        label_fr="test11",
        label_nl="test11",
        label_en="test11",
        label_de="test11",
    )
    code111.save()

    # Exercise
    tree = NacebelCodeView().all_as_tree()
    for node in tree:
        assert isinstance(node, NacebelCodeTree)
        check_node(node, None, 1)


def check_node(
    node: NacebelCodeTree, parent_code: NacebelCodeTree | None, level: int = 1
):
    assert node.level == level
    if parent_code:
        assert node.code.startswith(parent_code.code)
    for child in node.children:
        check_node(child, node, level + 1)

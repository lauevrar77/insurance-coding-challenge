from quotes.models import NacebelCode
from copy import deepcopy


class NacebelCodeTree:
    def __init__(self, code: NacebelCode):
        self.__code = code
        self.__childrens = []

    @property
    def code(self) -> str:
        return self.__code.code

    @property
    def label_fr(self) -> str:
        return self.__code.label_fr

    @property
    def label_nl(self) -> str:
        return self.__code.label_nl

    @property
    def label_en(self) -> str:
        return self.__code.label_en

    @property
    def label_de(self) -> str:
        return self.__code.label_de

    @property
    def children(self) -> list["NacebelCodeTree"]:
        return deepcopy(self.__childrens)

    def add_child(self, child: "NacebelCodeTree"):
        if child not in self.__childrens:
            self.__childrens.append(child)

    @property
    def level(self) -> int:
        return self.__code.level

    def __hash__(self) -> int:
        return hash((self.code,))

    def __eq__(self, value: object) -> bool:
        if isinstance(value, NacebelCodeTree):
            return self.code == value.code
        return False


class NacebelCodeView:
    def from_codes(self, codes: list[str]) -> list[NacebelCode]:
        return list(NacebelCode.objects.filter(code__in=codes).all())

    def all_as_tree(self) -> list[NacebelCodeTree]:
        level1_codes = []
        all_codes = {}
        codes = NacebelCode.objects.all().order_by("level", "code")
        for code in codes:
            code_tree = NacebelCodeTree(code)
            all_codes[code.code] = code_tree
            if code.level == 1:
                level1_codes.append(code_tree)
            else:
                all_codes[code.parent_code].add_child(code_tree)
        return level1_codes

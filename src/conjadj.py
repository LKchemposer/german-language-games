from abc import ABC, abstractmethod

from pattern import de


class ConjAdj(ABC):
    '''Methods inferring the gender of a noun, if not given.'''

    @abstractmethod
    def get_conjadj():
        pass


class Pattern_ConjAdj(ConjAdj):
    '''Uses pattern package.'''

    @staticmethod
    def get_conjadj(adj: str, gender: str, case: str, der_ein: str) -> str:
        conjadj = de.attributive(
            adj, gender=gender, role=case, article=der_ein)
        return conjadj

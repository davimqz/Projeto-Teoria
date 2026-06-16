"""Implementacao do problema Subconjunto Soma (Subset Sum) por backtracking.

Versao de decisao: retorna True se existir um subconjunto cuja soma seja igual ao alvo.
O algoritmo assume valores inteiros nao negativos quando a poda current_sum > target esta ativa.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SubsetSumResult:
    """Resultado da busca por backtracking."""

    exists: bool
    calls: int


def subset_sum_backtracking(values: Sequence[int], target: int, use_pruning: bool = True) -> SubsetSumResult:
    """Resolve Subset Sum usando backtracking recursivo.

    Args:
        values: Sequencia de inteiros positivos ou nao negativos.
        target: Valor-alvo W.
        use_pruning: Quando True, corta ramos em que a soma parcial ultrapassa o alvo.
            Essa poda e correta para entradas sem numeros negativos.

    Returns:
        SubsetSumResult com a resposta booleana e o numero de chamadas recursivas.
    """
    n = len(values)
    calls = 0

    def search(index: int, current_sum: int) -> bool:
        nonlocal calls
        calls += 1

        if current_sum == target:
            return True

        if index == n:
            return False

        if use_pruning and current_sum > target:
            return False

        # Ramo 1: inclui o elemento atual.
        if search(index + 1, current_sum + values[index]):
            return True

        # Ramo 2: ignora o elemento atual.
        return search(index + 1, current_sum)

    return SubsetSumResult(exists=search(0, 0), calls=calls)


if __name__ == "__main__":
    example_values = [3, 34, 4, 12, 5, 2]
    example_target = 9
    result = subset_sum_backtracking(example_values, example_target)
    print(f"Entrada: {example_values}")
    print(f"Alvo: {example_target}")
    print(f"Existe subconjunto? {result.exists}")
    print(f"Chamadas recursivas: {result.calls}")

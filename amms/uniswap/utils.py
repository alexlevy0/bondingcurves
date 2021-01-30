from typing import Any
from amms.logger import l

DIVIDER = "----"


class Token:
    def __init__(self, x_i: float = 1, x_i_qty: float = 0):
        if x_i not in [1, 2]:
            return Exception("1 or 2 allowed")

        if x_i_qty <= 0:
            return Exception("must be positive")

        self.name = f"x_{x_i}"
        self.qty = x_i_qty
        self.complement = f"x_{2 if x_i == 1 else 1}"

    def __repr__(self):
        return f"Token(x_i={self.name}, x_i_qty={self.qty})"


class LogHelper:
    @staticmethod
    def pool_created(o: Any):
        l.info(
            f"\nCREATED POOL.\n"
            f"x_1, x_2: {o.x_1:.8f}, {o.x_2:.8f}.\n"
            f"invariant {o.invariant}.\n"
            f"ex. rate x_1/x_2 = {o.x_2/o.x_1}.\n"
            f"{DIVIDER}\n"
        )

    @staticmethod
    def trade_executed(x_i: Token, x_j: float, o: Any):
        l.info(
            "\nEXECUTED TRADE.\n"
            f"swapped {x_i.qty} {x_i.name} for {x_j} {x_i.complement}\n"
            f"prev ex.rate x_1/x_2 = {o.prev_x_2/o.prev_x_1:.8f}.\n"
            f"prev x_1, prev x_2: {o.prev_x_1:.8f}, {o.prev_x_2:.8f}\n"
            f"prev invarinat {o.prev_invariant}\n"
            f"ex. rate x_1/x_2 = {o.x_2/o.x_1:.8f}.\n"
            f"x_1, x_2: {o.x_1:.8f}, {o.x_2:.8f}.\n"
            f"invariant {o.invariant}.\n"
            f"{DIVIDER}\n"
        )

    @staticmethod
    def added_liquidity(x_i: Token, x_j: float, o: Any):
        l.info(
            f"\nADDED LIQUIDITY.\n"
            f"added {x_i.qty} {x_i.name} and {x_j} {x_i.complement}\n"
            f"Δx_1, Δx_2: +{(o.x_1 - o.prev_x_1):.8f}, +{(o.x_2 - o.prev_x_2):.8f}.\n"
            f"x_1, x_2: {o.x_1:.8f}, {o.x_2:.8f}.\n"
            f"prev. invariant: {o.prev_invariant:.8f}.\n"
            f"invariant: {o.invariant:.8f}.\n"
            f"{DIVIDER}\n"
        )


# x_i_qty is the user sent delta
def quote(x_i_qty: float, x_i_reserve: float, x_j_reserve: float):
    x_j_per_x_i = x_j_reserve / x_i_reserve  # this is your ex rate: x_i / x_j
    x_j_qty = x_i_qty * x_j_per_x_i
    return x_j_qty


def get_amount_out(x_i: Token, x_i_reserve: float, x_j_reserve: float):
    x_i_with_fee = x_i.qty * 997
    x_j_out = (x_i_with_fee * x_j_reserve) / (x_i_with_fee + 1000 * x_i_reserve)
    return x_j_out
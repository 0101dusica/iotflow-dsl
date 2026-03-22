from dataclasses import field, dataclass
from typing import Optional

from .executor import RuleExecution


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"


@dataclass
class CycleResult:
    cycle_number: int
    readings: dict[str, float] = field(default_factory=dict)
    rule_executions: list[RuleExecution] = field(default_factory=list)
    actions_triggered: int = 0


@dataclass
class RunResult:
    model_name: str
    duration_seconds: float
    cycles: list[CycleResult] = field(default_factory=list)

    @property
    def total_rules_evaluated(self) -> int:
        return sum(len(c.rule_executions) for c in self.cycles)

    @property
    def total_actions_triggered(self) -> int:
        return sum(c.actions_triggered for c in self.cycles)

    @property
    def rules_passed(self) -> int:
        return sum(
            1 for c in self.cycles
            for r in c.rule_executions if r.condition_met
        )

    @property
    def rules_not_triggered(self) -> int:
        return self.total_rules_evaluated - self.rules_passed

    @staticmethod
    def _fmt_status(ok: bool) -> str:
        return f"{Color.GREEN}✔ TRIGGERED{Color.RESET}" if ok else f"{Color.YELLOW}— SKIPPED{Color.RESET}"

    def _render_header(self) -> str:
        return (
            f"{Color.BOLD}{Color.CYAN}IoTFlow Simulation Report{Color.RESET}\n"
            f"Model: {Color.BOLD}{self.model_name}{Color.RESET}\n"
            f"Duration: {self.duration_seconds:.3f}s\n"
        )

    def _render_cycle(self, cycle: CycleResult) -> list[str]:
        lines: list[str] = []
        lines.append(f"\n{Color.BOLD}Cycle {cycle.cycle_number}:{Color.RESET}")

        lines.append(f"  {Color.BOLD}Sensor Readings:{Color.RESET}")
        for name, value in cycle.readings.items():
            lines.append(f"    {name}: {value}")

        lines.append(f"  {Color.BOLD}Rules:{Color.RESET}")
        for r in cycle.rule_executions:
            status = self._fmt_status(r.condition_met)
            lines.append(f"    {status}  {r.rule_name}  ({r.sensor_name}={r.sensor_value})")
            if r.condition_met:
                lines.append(
                    f"      → {Color.GREEN}{r.actuator_name}.{r.action_name}{Color.RESET}"
                )

        return lines

    def _render_summary(self) -> str:
        return (
            f"\n{Color.BOLD}Summary:{Color.RESET}\n"
            f"  Cycles: {len(self.cycles)}\n"
            f"  Rules evaluated: {self.total_rules_evaluated} "
            f"({Color.GREEN}{self.rules_passed} triggered{Color.RESET}, "
            f"{Color.YELLOW}{self.rules_not_triggered} skipped{Color.RESET})\n"
            f"  Actions triggered: {self.total_actions_triggered}\n"
        )

    def __str__(self) -> str:
        lines: list[str] = [self._render_header()]

        for cycle in self.cycles:
            lines += self._render_cycle(cycle)

        summary_color = Color.GREEN if self.total_actions_triggered > 0 else Color.YELLOW
        lines.append(summary_color + self._render_summary() + Color.RESET)
        return "\n".join(lines)

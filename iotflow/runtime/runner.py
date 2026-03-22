from typing import Optional

from .context import build_context
from .sensor_sim import generate_readings
from .executor import execute_rules
from .run_result import RunResult, CycleResult
from .timing import timed
from ..model import Model


def _run_simulation_internal(
    model: Model,
    sensor_overrides: Optional[dict[str, float]] = None,
    cycles: int = 1,
) -> RunResult:
    ctx = build_context(model)
    cycle_results: list[CycleResult] = []

    for i in range(cycles):
        readings = generate_readings(ctx.sensors, sensor_overrides)
        rule_execs = execute_rules(ctx.rules, readings)
        actions_triggered = sum(1 for r in rule_execs if r.condition_met)

        cycle_results.append(CycleResult(
            cycle_number=i + 1,
            readings=readings,
            rule_executions=rule_execs,
            actions_triggered=actions_triggered,
        ))

    return RunResult(
        model_name=f"IoTFlow ({len(ctx.sensors)} sensors, {len(ctx.actuators)} actuators, {len(ctx.rules)} rules)",
        duration_seconds=0.0,
        cycles=cycle_results,
    )


@timed
def _run_simulation_timed(model, sensor_overrides=None, cycles=1):
    return _run_simulation_internal(model, sensor_overrides, cycles)


def run_simulation(
    model: Model,
    *,
    sensor_overrides: Optional[dict[str, float]] = None,
    cycles: int = 1,
) -> RunResult:
    result, duration = _run_simulation_timed(model, sensor_overrides, cycles)
    result.duration_seconds = duration
    return result

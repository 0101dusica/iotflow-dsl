from dataclasses import dataclass, field

from ..model import Model, Sensor, Actuator, Rule


@dataclass
class SimulationContext:
    sensors: dict[str, Sensor] = field(default_factory=dict)
    actuators: dict[str, Actuator] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=list)


def build_context(model: Model) -> SimulationContext:
    ctx = SimulationContext()
    for el in model.elements:
        if isinstance(el, Sensor):
            ctx.sensors[el.name] = el
        elif isinstance(el, Actuator):
            ctx.actuators[el.name] = el
        elif isinstance(el, Rule):
            ctx.rules.append(el)
    return ctx

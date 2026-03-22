from textx import language


@language('iotflow', '*.iot')
def iotflow_language():
    """
    Register IoTFlow DSL language with textX.
    """
    from .parser.metamodel import build_metamodel
    return build_metamodel()

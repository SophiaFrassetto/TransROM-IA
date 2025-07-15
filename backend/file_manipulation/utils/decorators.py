import logging
from functools import wraps
from ..core.enums import ProcessingStage

logger = logging.getLogger(__name__)


def stage_logger(stage: ProcessingStage):
    """
    Decorador para logging automático de estágios do pipeline.
    Loga início e fim do estágio.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Iniciando estágio: {stage.value}")
            result = func(*args, **kwargs)
            logger.info(f"Estágio {stage.value} concluído")
            return result

        return wrapper

    return decorator


def performance_monitor(func):
    """
    Decorador para monitoramento de performance.
    Loga o tempo de execução da função decorada.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        import time

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executado em {end_time - start_time:.4f}s")
        return result

    return wrapper

"""
Модуль, содержащий иерархию ошибок.
"""
class StreamStatsError(Exception):
    """
    Базовое исключение.
    """
    pass


class InvalidFormatError(StreamStatsError):
    """
    Ошибка неподдерживаемого формата.
    """
    pass


class InvalidEventError(StreamStatsError):
    """
    Ошибка неверного события.
    """
    pass


class InvalidTimestampError(InvalidEventError):
    """
    Неверная временная метка.
    """
    pass


class InvalidCLI(StreamStatsError):
    """
    Ошибка конфигурации CLI.
    """
    pass

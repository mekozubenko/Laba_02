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
import json

def report_to_dict(report):
    return {
        'Общее число событий': report.events_count,
        'Количество событий каждого уровня': report.levels,
        'Количество событий каждого источника': report.sources,
        'Топ-5 источников ошибок уровня ERROR/CRITICAL': report.top_5_error_sources,
        'Первая временная метка': report.first_timestamp,
        'Последняя временная метка': report.last_timestamp
    }

def report_to_json(report, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(report_to_dict(report), json_file, ensure_ascii=False, indent=4)

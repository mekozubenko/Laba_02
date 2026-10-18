"""
Модуль для анализа событий и сбора статистики.
"""
from streamstats.models import Event, Report

def analyzer(event):
    report = Report()
    for current_event in event:
        if isinstance(current_event, Event):
            report.events_count += 1

            if current_event.level in report.levels:
                report.levels[current_event.level] += 1
            else:
                report.levels[current_event.level] = 1

            if current_event.source in report.sources:
                report.sources[current_event.source] += 1
            else:
                report.sources[current_event.source] = 1

            if report.first_timestamp is None or current_event.timestamp < report.first_timestamp:
                report.first_timestamp = current_event.timestamp
            if report.last_timestamp is None or current_event.timestamp > report.last_timestamp:
                report.last_timestamp = current_event.timestamp

            if current_event.level in ('CRITICAL', 'ERROR'):
                if current_event.level in report.critical_sources:
                    report.critical_sources[current_event.level] += 1
                else:
                    report.critical_sources[current_event.level] = 1

    report.top_5_error_sources = [k for k, v in sorted(report.critical_sources.items(), key=lambda item: item[1], reverse=True)[:5]]

    return report

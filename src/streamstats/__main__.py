import argparse
import sys
import logging
from streamstats.errors import StreamStatsError,InvalidCLI
from streamstats.models import Report, Event
from streamstats.parsers import parser_csv, parser_json
from streamstats.report import report_to_json

logging.basicConfig(level=logging.WARNING, format = "%(levelname)s: %(message)s")

def parser_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices = ['analyze'])
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--format', choices = ['jsonl', 'csv'], required=True)
    parser.add_argument('--output', default = 'report.json')
    parser.add_argument('--skip-invalid', action = 'store_true')
    return parser.parse_args()

def update_report(report: Report, event: Event):
    report.events_count += 1

    report.levels[event.level] = report.levels.get(event.level, 0) + 1

    report.sources[event.source] = report.sources.get(event.source, 0) + 1

    if report.first_timestamp is None or event.timestamp < report.first_timestamp:
        report.first_timestamp = event.timestamp
    if report.last_timestamp is None or event.timestamp > report.last_timestamp:
        report.last_timestamp = event.timestamp

    if event.level in ('CRITICAL', 'ERROR'):
        report.critical_sources[event.source] = report.critical_sources.get(event.source, 0) + 1
def final_report(report: Report):
    sorted_sources = sorted(report.critical_sources, key=lambda x: x[1], reverse=True)
    report.top_5_error_sources = [k for k, v in sorted_sources[:5]]

def main():
    try:
        args = parser_command_line()
    except StreamStatsError:
        sys.exit(2)

    if args.format == 'jsonl':
        parse_file = parser_json
    else:
        parse_file = parser_csv

    main_report = Report()

    for file_number, filename in enumerate(args.inputs, start = 1):
        line_number = 0
        try:
            for event in parse_file(filename):
                line_number += 1
                update_report(main_report, event)
        except FileNotFoundError:
            print(f'Файл {filename} не найден', file=sys.stderr)
            sys.exit(2)
        except StreamStatsError as e:
            if args.skip_invalid:
                logging.warning(f'Пропущена строка номер {line_number + 1} в файле {filename}: {e}')
                main_report.skipped_lines += 1
            else:
                print(f'Ошибка в файле номер {file_number} ({filename}), строка номер {line_number + 1}: {e}', file=sys.stderr)
                sys.exit(2)

    final_report(main_report)

    report_to_json(main_report, args.output)

if __name__ == '__main__':
    main()
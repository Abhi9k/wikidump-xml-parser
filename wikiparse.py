import xml.etree.ElementTree as e_tree
from multiprocessing import Process, Pool
from datetime import datetime
import sys
import os


def parse_config(config_file_path):
    config_file = open(config_file_path, 'r')
    dump_file_path, edit_date_lower, edit_date_upper =\
                    config_file.readlines()
    edit_date_lower = datetime.strptime(edit_date_lower.strip(), "%Y-%m-%d")
    edit_date_upper = datetime.strptime(edit_date_upper.strip(), "%Y-%m-%d")
    return dump_file_path.strip(), edit_date_lower, edit_date_upper

def write_output_to_csv(file_obj, page_id, title, revision_count):
    file_obj.write('"{}","{}","{}"\n'.format(page_id, title, revision_count))


def is_valid_revision_timestamp(timestamp, timestamp_lower, timestamp_upper):
    if timestamp and (timestamp >= timestamp_lower) and (timestamp <= timestamp_upper):
        return True
    return False


def print_progress(current_byte_pos, start_byte_pos, end_byte_pos, last_progress):
    progress = ((float(current_byte_pos) - start_byte_pos)* 100)/ (start_byte_pos - end_byte_pos)
    progress = int(progress)
    if progress - last_progress > 2:
        print progress, 'percent completed'
        return progress
    return last_progress

def parse_chunk(
        start_byte_pos, end_byte_pos, dump_file_path,
        timestamp_lower, timestamp_upper):
    in_file = open(dump_file_path, 'r')
    start = start_byte_pos
    if end_byte_pos == -1:
        in_file.seek(0, 2)
        end = in_file.tell()
    else:
        end = end_byte_pos
    in_file.seek(start_byte_pos, 0)
    in_revision = False
    revision_count = 0
    page_id = -2
    timestamp = None
    title = ''
    max_id = -1
    max_count = 0
    max_title = ''
    progress = 0

    for line in in_file:
        if '<page' in line:
            page_id = -1
            revision_count = 0
            in_revision = False
            timestamp = None
            title = ''
        elif '<revision' in line:
            in_revision = True
            timestamp = None
        elif '</revision' in line:
            if (in_revision and page_id != -1 and page_id != -2 and\
                is_valid_revision_timestamp(
                    timestamp, timestamp_lower,timestamp_upper)):
                revision_count += 1
            in_revision = False
        elif '<id' in line and page_id == -1:
            line = line.strip()
            page_id = line[4: -5]
        elif '<title' in line:
            line = line.strip()
            title = line[len('<title>'): -1* len('</title>')]
        elif '</page' in line:
            if page_id != -1 and page_id != -2 and revision_count > 0:
                if revision_count > max_count:
                    max_count = revision_count
                    max_title = title
                    max_id = page_id
            progress = print_progress(in_file.tell(), start_byte_pos, end_byte_pos, progress)
            if in_file.tell() >= end_byte_pos:
                break
        elif '<timestamp' in line and timestamp is None and in_revision:
            line = line.strip()
            timestamp_str = line[len('<timestamp>'): -1* len('</timestamp>')]
            timestamp = datetime.strptime(timestamp_str.split('T')[0], "%Y-%m-%d")
    return max_id, max_title, max_count


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) < 3:
        print 'Usage: python wikiparse.py CONFIG_FILE_NAME START_BYTE_POSITION END_BYTE_POSITION'
        exit(1) 
    config_file_name = arguments[0]
    start = long(arguments[1])
    end = long(arguments[2])

    dump_file_path, edit_date_lower, edit_date_upper =\
                    parse_config(os.path.join(os.path.abspath('.'), config_file_name))
    f = open(dump_file_path, 'r')
    print parse_chunk(start, end, dump_file_path, edit_date_lower, edit_date_upper)

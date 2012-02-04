#!/usr/bin/env python
# -*- coding: utf-8 -*-
# authors: Dat Chu <dattanchu@gmail.com>
#          Dominik Mayer <dominik.mayer@gmail.com>
#          John Tyree
# Optional Dependency
#  - aplay to play a sound of your choice

import time
import os
import sys
import argparse
import subprocess

from datetime import timedelta
from math import ceil, floor

# ———————————————————————————— CONFIGURATIONS ————————————————————————————

# Files and Folders
pymodoro_directory_config = '~/.pymodoro'
session_file = '~/.pomodoro_session'

# Times
session_duration_in_seconds = 25 * 60 +1
break_duration_in_seconds = 5 * 60
update_interval_in_seconds = 1

# Progress Bar
total_number_of_marks = 10
session_full_mark_character = '#'
break_full_mark_character = '|'
empty_mark_character = '·'

# Sound
enable_sound = True
session_sound_file_config = 'ding.mp3'
break_sound_file_config = 'rimshot.wav'

# —————————————————————————— END CONFIGURATIONS ———————————————————————————

# constant inferred from configurations
pymodoro_directory = os.path.expanduser(pymodoro_directory_config)
session_sound_file = pymodoro_directory + '/' + session_sound_file_config
break_sound_file = pymodoro_directory + '/' + break_sound_file_config

# variables
last_start_time = 0

def set_configuration_from_arguments(args):
    global session_duration_in_seconds
    global break_duration_in_seconds
    global update_interval_in_seconds
    global total_number_of_marks
    global session_full_mark_character
    global break_full_mark_character
    global empty_mark_character
    global session_file
    global session_sound_file
    global break_sound_file
    global enable_sound
    if args.session_duration is not None:
        if args.durations_in_seconds == True:
            session_duration_in_seconds = args.session_duration
        else:
            session_duration_in_seconds = args.session_duration * 60
    if args.break_duration is not None:
        if args.durations_in_seconds == True:
            break_duration_in_seconds = args.break_duration
        else:
            break_duration_in_seconds = args.break_duration * 60
    if args.update_interval_in_seconds is not None:
        update_interval_in_seconds = args.update_interval_in_seconds
    if args.total_number_of_marks is not None:
        total_number_of_marks = args.total_number_of_marks
    if args.session_full_mark_character is not None:
        session_full_mark_character = args.session_full_mark_character
    if args.break_full_mark_character is not None:
        break_full_mark_character = args.break_full_mark_character
    if args.empty_mark_character is not None:
        empty_mark_character = args.empty_mark_character
    if args.session_file is not None:
        session_file = args.session_file
    if args.session_sound_file is not None:
        session_sound_file = args.session_sound_file
    if args.break_sound_file is not None:
        break_sound_file = args.break_sound_file
    if args.silent: # Always boolean
        enable_sound = False
    if args.no_break:
        break_duration_in_seconds = 0

def get_seconds_left():
    if os.path.exists(session_file):
        global last_start_time
        start_time = os.path.getmtime(session_file)
        if last_start_time != start_time:
            last_start_time = start_time
            setup_new_timer()
        return floor(session_duration_in_seconds - time.time() + start_time)
    else:
        return

def setup_new_timer():
    options = read_session_file()
    if len(options) > 0:
        set_session_duration(options[0])
    if len(options) > 1:
        set_break_duration(options[1])

def read_session_file():
    f = open(session_file)
    content = f.readline()
    f.close()
    return content.rsplit()

def set_session_duration(session_duration_as_string):
    global session_duration_in_seconds
    session_duration_as_integer = convert_string_to_int(session_duration_as_string)
    if session_duration_as_integer != -1:
        session_duration_in_seconds = session_duration_as_integer

def convert_string_to_int(string):
    if not string.isdigit():
        #print("Session File may only contain digits!")
        return -1
    else:
        return int(string)

def set_break_duration(break_duration_as_string):
    global break_duration_in_seconds
    break_duration_as_integer = convert_string_to_int(break_duration_as_string)
    if break_duration_as_integer != -1:
        break_duration_in_seconds = break_duration_as_integer * 60

def print_session_output(seconds_left):
    print_output("P", session_duration_in_seconds, seconds_left, session_full_mark_character)

def print_break_output(seconds_left):
    break_seconds_left = get_break_seconds_left(seconds_left)
    print_output("B", break_duration_in_seconds, break_seconds_left, break_full_mark_character)

def get_break_seconds_left(seconds):
    return break_duration_in_seconds + seconds

def print_output(description, duration_in_seconds, seconds, full_mark_character):
    minutes = get_minutes(seconds)
    output_seconds = get_output_seconds(seconds)
    progress_bar = print_progress_bar(duration_in_seconds, seconds, full_mark_character)
    output = description + "%s %02d:%02d" % (progress_bar, minutes, output_seconds)
    sys.stdout.write(wrap(output)+"\n")

def wrap(string, color = None):
    if color is not None:
        return "<fc=%s>%s</fc>" % (color, string)
    else:
        return string

def get_minutes(seconds):
    return int(seconds / 60)

def get_output_seconds(seconds):
    minutes = get_minutes(seconds)
    return int(seconds - minutes * 60)

def print_progress_bar(duration_in_seconds, seconds, full_mark_character):
    if total_number_of_marks != 0:
        seconds_per_mark = ceil(float(duration_in_seconds) / total_number_of_marks)
        number_of_full_marks = int(round(float(seconds) / seconds_per_mark))
        output = " " + print_full_marks(number_of_full_marks, full_mark_character) \
            + print_empty_marks(total_number_of_marks - number_of_full_marks)
    else:
        output = ""
    return output

def print_full_marks(number_of_full_marks, full_mark_character):
    return full_mark_character * number_of_full_marks

def print_empty_marks(number_of_empty_marks):
    return empty_mark_character * number_of_empty_marks

def print_break_output_hours(seconds):
    seconds = -seconds
    minutes = get_minutes(seconds)
    output_minutes = get_output_minutes(seconds)
    hours = get_hours(seconds)
    output_seconds = get_output_seconds(seconds)
    if break_duration_in_seconds < seconds:
        color = "red"
    else:
        color = None
    if minutes < 60:
        output = "B %02d:%02d min" % (minutes, output_seconds)
    elif hours < 24:
        output = "B %02d:%02d h" % (hours, output_minutes)
    else:
        days = int(hours/24)
        output_hours = hours - days * 24
        output = "B %02d d %02d h" % (days, output_hours)
    sys.stdout.write(wrap(output, color)+"\n")

def get_hours(seconds):
    return int(seconds / 3600)

def get_output_minutes(seconds):
    hours = get_hours(seconds)
    minutes = get_minutes(seconds)
    return int(minutes - hours * 60)

def play_sound(sound_file):
    if enable_sound:
        try:
            subprocess.Popen(['play', '-q', sound_file])
        except OSError as e:
            notify(["Error'd playing sound"])
            pass

def notify_end_of_session():
    play_sound(session_sound_file)
    notify(["Worked enough.", "Time for a break!"])

def notify_end_of_break():
    play_sound(break_sound_file)
    notify(["Break is over.", "Back to work!"])

def notify(strings):
    try:
        subprocess.Popen(['notify-send'] + strings)
    except OSError as e:
        pass

def main():
    # Parse command line arguments
    global session_file

    parser = argparse.ArgumentParser(description='Create a textual Pomodoro display.')

    parser.add_argument('-s', '--seconds', action='store_true', help='Changes format of input times from minutes to seconds.', dest='durations_in_seconds')
    parser.add_argument('-d', '--session', action='store', nargs='?', type=int, help='Pomodoro duration in minutes (default: 25).', metavar='POMODORO DURATION', dest="session_duration")
    parser.add_argument('break_duration', action='store', nargs='?', type=int, help='Break duration in minutes (default: 5).', metavar='BREAK DURATION')

    parser.add_argument('-f', '--file', action='store', help='Pomodoro session file (default: ~/.pomodoro_session).', metavar='PATH', dest='session_file')
    parser.add_argument('-n', '--no-break', action='store_true', help='No break sound.', dest='no_break')

    parser.add_argument('-i', '--interval', action='store', type=int, help='Update interval in seconds (default: 1).', metavar='DURATION', dest='update_interval_in_seconds')
    parser.add_argument('-l', '--length', action='store', type=int, help='Bar length in characters (default: 10).', metavar='INT', dest='total_number_of_marks')

    parser.add_argument('-p', '--pomodoro', action='store', help='Pomodoro full mark characters (default: #).', metavar='CHARACTER', dest='session_full_mark_character')
    parser.add_argument('-b', '--break', action='store', help='Break full mark characters (default: |).', metavar='CHARACTER', dest='break_full_mark_character')
    parser.add_argument('-e', '--empty', action='store', help='Empty mark characters (default: ·).', metavar='CHARACTER', dest='empty_mark_character')

    parser.add_argument('-sp', '--pomodoro-sound', action='store', help='Pomodoro end sound file (default: nokiaring.wav).', metavar='PATH', dest='session_sound_file')
    parser.add_argument('-sb', '--break-sound', action='store', help='Break end sound file (default: rimshot.wav).', metavar='PATH', dest='break_sound_file')
    parser.add_argument('-si', '--silent', action='store_true', help='Play no end sounds', dest='silent')

    args = parser.parse_args()
    set_configuration_from_arguments(args)
    session_file = os.path.expanduser(session_file)

# sanity check
    if not os.path.exists(session_sound_file):
        print("Error: Cannot find sound file %s" % session_sound_file)
    if not os.path.exists(break_sound_file):
        print("Error: Cannot find sound file %s" % break_sound_file)

# Repeat printing the status of our session
    seconds_left = get_seconds_left()
    while True:
        if seconds_left is None:
            sys.stdout.write("P —\n")
        else:
            if 0 < seconds_left:
                print_session_output(seconds_left)
            elif seconds_left == 0:
                notify_end_of_session()
            else:
                if -seconds_left < break_duration_in_seconds:
                    print_break_output(seconds_left)
                elif -seconds_left == break_duration_in_seconds:
                    print_break_output(seconds_left)
                    notify_end_of_break()
                else:
                    print_break_output_hours(seconds_left)

        sys.stdout.flush()

        time.sleep(update_interval_in_seconds)

        seconds_left = get_seconds_left()


if __name__ == "__main__": main()

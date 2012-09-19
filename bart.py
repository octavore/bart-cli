#!/usr/bin/env python
import sys, select, time, argparse
from urllib import urlopen
from xml.etree import ElementTree as ET
from string import rjust, ljust, join
from blessings import Terminal

INDENT = " " * 2
DIRECTION = {'s': 'south', 'n': 'north'}
WALKING = 3
WARNING = 10
BASE_URL = "http://api.bart.gov/api/"
term = Terminal('xterm-256color')

def api_url(endpoint, cmd, params={}):
  tail = join(["%s=%s" % (k,params[k]) for k in params], '&')
  tail += "&key=MW9S-E7SL-26DU-VV8V"
  return "%s%s.aspx?cmd=%s&%s" % (BASE_URL, endpoint, cmd, tail)

def get_stations():
  stns_url = api_url('stn', 'stns')
  xml_doc = ET.parse(urlopen(stns_url))
  root = xml_doc.getroot()
  for station in root.iter('station'):
    abbr = term.bright_green(station.find('abbr').text)
    name = station.find('name').text
    print '%s %s' % (abbr, name)

def get_time(orig, dir):
  powl_url = api_url('etd', 'etd', { 'ORIG': orig, 'dir': dir})

  xml_doc = ET.parse(urlopen(powl_url))
  root = xml_doc.getroot()

  output = "\n"
  output += INDENT
  output += term.bright_green_underline("Heading %s from %s"
                % (DIRECTION[dir], root.find('.//name').text))
  output += "\n"

  for etd in root.iter('etd'):
    estimates = [est.find("minutes").text for est in etd.iter("estimate")]
    estimates = [rjust(est, 2) for est in estimates]

    next_train = False
    for idx, est in enumerate(estimates):
      if not next_train and est.strip().isdigit() and int(est) > WALKING:
        next_train = int(est)
        estimates[idx] = term.bold_yellow(est)
        break

    output += INDENT
    output += ("[%s]" % etd.find('abbreviation').text) + "  "
    output += ljust(term.bright_white(etd.find('destination').text), 32)
    output += join(estimates, " <- ") + " minutes"

    if next_train < WARNING:
      output += " " + term.bright_white_on_red(" LEAVE NOW! ")

    output += "\n"

  output += "\n"
  output += INDENT
  output += "Page time: %s" % root.find('.//time').text
  output += "   Last fetch: %s" % time.strftime("%I:%M:%S%P", time.localtime())
  output += "\n"
  return output


def getch():
  import sys, tty, termios
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
  finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch


def magic_lines(s, width=term.width):
  for line in s.split("\n"):
    print term.on_bright_black_underline(" " * width)
    time.sleep(0.05)

    # print term.move_up + term.on_bright_black_underline(line)
    # time.sleep(0.2)
    print term.move_up + term.on_black(" " * width)
    print term.move_up + line
    time.sleep(0.05)


def draw(station, north=False, south=True):
  with term.location(y=0):
    if north:
      magic_lines(get_time(station, 'n'), term.width)

    if south:
      magic_lines(get_time(station, 's'), term.width)

    print '-' * term.width
    print "Press 'r' to refresh, any other key to quit"
  command = getch()
  if command != 'r':
    return
  draw(station, north, south)


def main():
  p = argparse.ArgumentParser()
  p.add_argument('station',
                  # metavar='STAT',
                  nargs='?',
                  type=str,
                  help='Station name',
                  default='POWL')
  p.add_argument('-n', action='store_true', help='Show northbound', default=False)
  p.add_argument('-s', action='store_true', help='Show southbound', default=False)
  p.add_argument('-p', action='store_true', help='Print station list', default=False)

  args = p.parse_args()

  if args.p:
    get_stations()
  else:
    with term.fullscreen():
      with term.hidden_cursor():
        # TODO: catch invalid station
        draw(args.station, args.n, args.s or not args.n)


if __name__ == '__main__':
  main()

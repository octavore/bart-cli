# BART Command-line tool

![Screenshot](https://raw.github.com/octavore/bart-cli/master/screenshot.png)

## Installation

1. Requires `blessings` module, either `easy_install blessings` or `pip install blessings`.
2. Clone this repo.

## Usage

From the downloaded repository folder, run `python bart.py` with options specified as below:

```sh
Usage: python bart.py [-h] [-n] [-s] [station]

  station     Station name

optional arguments:
  -h, --help  show this help message and exit
  -n          Show northbound
  -s          Show southbound
  -p          Print station list
```

e.g.

```sh
$ ./bart.py POWL -n
```

Default station is southbound trains from Powell.

Tip: symlink it into your `/usr/local/bin` folder so you can access it anywhere.

```sh
$ ln -s /path/to/bart.py /usr/local/bin/bart 
```

## Customization

'Leave now' messages appear when the time to departure is greater than `WALKING` and less than `WARNING`, which are constants specified in `bart.py`. 
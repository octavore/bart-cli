# BART Command-line tool

```sh
Usage: bart.py [-h] [-n] [-s] [station]

positional arguments:
  station     Station name

optional arguments:
  -h, --help  show this help message and exit
  -n          Show northbound
  -s          Show southbound
```

e.g.

```sh
$ ./bart.py POWL -n
```

Default station is Powell, default direction is southbound trains. Why? Because
I wrote this, and that's the train I take most often.
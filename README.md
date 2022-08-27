![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)

# [mif](./mif.py)
Converter to Altera [MIF](https://www.intel.com/content/www/us/en/programmable/quartushelp/17.0/reference/glossary/def_mif.htm) file format.


## Releases

| Version                                                   | Date       | Source                                                                                           | Change log     |
| --------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------ | -------------- |
| latest                                                    |            | <a id="raw-url" href="https://github.com/akaeba/mif/archive/refs/heads/main.zip">latest.zip</a>  |                |



## Features

* converts:
    * binary to mif
* selectable data width in byte granularity
* selectable size


## Command line interface

### Options

### Options

| Option                 | Description                            | Remarks                                   |
| ---------------------- | -------------------------------------- | ----------------------------------------- |
| -d, [--depth=1024]     | number of words                        | if input has less data, padding with 0xff |
| -w, [--width=1]        | word width in bytes                    |                                           |
| -e, [--endianness=big] | byte organization, low/high byte first |                                           |



### Run

```bash
python3 mif.py
```

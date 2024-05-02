# MicroFreshener-core

-------
[![PyPI version](https://badge.fury.io/py/microfreshener-core.svg)](https://badge.fury.io/py/microfreshener-core)
[![Build Status](https://travis-ci.org/di-unipi-socc/microFreshener-core.svg?branch=master)](https://travis-ci.org/di-unipi-socc/microFreshener-core)


`MicroFreshener-core` is the core python module of [microFreshener](https://github.com/di-unipi-socc/microFreshener) that permits to discover architecturl smells affectinng  microservices.


## Table of Contents
- [Architecture](#architecture)
- [Quick Guide](#quick-guide)
  * [Installation](#installation)
  * [Example of usage](#example-of-usage) -->
- [License](#license)

## Architecture
`microfreshener-core` has 3 stages: Importer, Analyser and Exporter. Each Stage should have well defined interface so it is easy to write new Importer, Analyser or Exporters and plug it in. Currently only Importer and Exporter interfaces are defined.


## Quick Guide
`MicroFreshener-core` is a python module distributed in PyPi.

## Installation
In order to use `MicroFreshener-core` install the python package

```
$ pip install microfreshener-core
```

## Example of usage
You can use `microfreshener-core` in your project by importing the class of the module.

In the following example, the YML file of the helloworld is imported and analysed.
The result of the analysis is a dictionary, where for each node are listed the smells and the refactorigns to be applied.

```
from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser import MicroToscaAnalyserBuilder

yml_importer = YMLImporter()

model = yml_importer.Import("helloworld.yml")
builder = MicroToscaAnalyserBuilder(model)
builder.add_all_sniffers()
analyser = builder.build()

res = analyser.run()
print(res)
```
# nake
nake is make for storing project scripts in nakefile, and running them in easy
and shell-compatible way

Problems with make from the point of view of person who wants to run shell scripts:
- need to repeat every command on top of file with .PHONY
- tab is required before every command, without it make won't work and error message
  will be cryptic
- every instruction is run in separate shell, which doesn't allow to set env 
  variables in one line and use in next
- by default doesn't use any shell extension (needs to be specifically instructed
  using `SHELL := /bin/bash`)
- syntax used by variables is different from shell, often impossible to use the same 
  command as in shell, adaptation is sometimes difficult and time consuming
- single targets can't have individual parameters
- focused on resolving dependencies in C/C++ and other compilled languages
- a lot of historic baggage, built originally in 70's and 80's which is visible


Aims of this project:
- to replace make for cases when resolving file dependencies doesn't matter, but user want
  to have scripts for running various project tasks
- allow perfect integration with shell variables and other utilities
- compatibility with all popular shells and platforms
- simple to use, flexible, modern feeling to it
- better autocompletion support (instead of only first words, also middle words ie.
  setup-api-server could be invoked by typing nake api<tab> and all commands with api would appear) 
- perhaps be make-compatible, in that nakefile can store make compatible syntax in case
  you need the dependency resolving and other magic. Then running it like `nake make stuff`
  would run it as `make stuff` (using make from system, with dynamically created makefile). 
  That way one file could store all building logic for using make, and in the same file have 
  handy nake scripts (need to think more on this if it makes sense).
- other reasons why Make is troublesome tool: https://github.com/SCons/scons/wiki/FromMakeToScons

Note: all below are louse design ramblings, and can change at any step. 

## Quick start:

`pip install nake`  - not yet there :)

`vim nakefile`

`nake`


## Examples:

```
setup:
	python3 -m venv foo_venv
 	source foo_venv/bin/activate
 	pip install -r requirements.txt
```
That's it, complete Nakefile which can be run as `nake setup`. Makefile would
need to have &\ at end of lines, for the changes made by source to not be lost. 
Nakefile by default checks if command in line returned 0, before proceeding to
next one. It can be changed to ignore errors by prefixing line with - (like in Makefile).

Indentation is up to you: you can use tab, 4 spaces, 1 space or no space at all. 
Nakefile is case sensitive.
Line comments are supported through `# line comment`, and multi line comments
through `/*` and `*/` (like in C++).

### Constants

```
FOOBAR_PORT='1337'
FOOBAR_ADDRESS='localhost:' + {FOOBAR_PORT}

api-add-some(baz: str):
  echo "Calling my amazing service"
  curl {FOOBAR_ADDRESS}/api/v1/baz/{baz} -X POST > results.txt 
_ cat results.txt | grep "top-secret"
```
Nakefile constants are using different syntax than shell variables, so it's harder to mix them and they're 
universal. Syntax is similiar to python. Constants are interpreted once before command is run.
Nakefile targets (api-add-some) can have parameters with types, and are automatically checked at runtime.
Forgetting to provide parameter shows friendly error:

```
$ nake api-add-some
Nake error: target 'api-add-some' called without param 'baz: str'

$ nake api-add-some "99_beers"
  Calling my amazing service
  curl localhost:1337/api/v1/baz/99_beers -X POST
  (here goes grep results)
```
Lines are echoed (except for `echo` command itself!). Echoing can be disabled by
prefixing line with `@` or `_` and space. 
Combining `_` and `-` gives `=` - line that is not echoed and return result is ignored
(will see if that makes sense :) )
Prefixing with + echoes line, if it was disabled for target.
Prefixing target with one of above modifiers applies this logic automatically to all lines.

### Targets

Nakefiles can also be simply included for composition (#1). 
Targets can call each other in any place (#2):
```Makefile
include foobar.nake   # 1

api-add-even-more(baz: str, buzz: int):    # 2
  api-add-some(baz)
  curl {FOOBAR_ADDRESS}/api/v1/buzz/{buzz} -X POST
```
Nake tries to detect target calls inside targets, but if it fails because ie. some
other symbol has the same name, it can be forced by prefixing with !

Nake doesn't support the dependencies syntax as in Make, ie. 

```Makefile
make-rule: dep1 dep2
	echo "doing sth here after dependencies"
```

### Default parameters:

```

build-api(tag: str = 'latest'):
	cd api/
	docker build -t api:{tag}

run-api(tag: str = 'latest'):
	echo "Running api:{tag}"
	docker run --rm -p 8080 api:{tag}

```
String parameters are "replaced" inplace without quotes, inside strings or commands.
Nake doesn't try interpret the context. No special rules to remember.

As usual in languages with default params, you need to provide default value to
all further params once one gets default param. And you can't 


### Default target and aliases

If nothing is passed - `nake` - a `all` target is run, if it's defined and has
all default variables.
Otherwise Nake just displays list of targets.

Note that you can provide aliases for commands by prepending them before:

```
all:
setup:
spam(what: str='):
	python3 -m spam {what}
```

So with above you can run `nake`, `nake setup` and `nake spam 'eggs'` and it 
will have the same effect.


### Envinroment variables

They can be declared in targets using :

```
some-rule:
	VARIABLE='foobar'
	echo $(VARIABLE)
```

You can also include env files with definitions, ie. `.env`:

```
FOOBAR_VER=1.0.2
export base_image=alpine:12
```

Notice that it supports both `export` and base variable definitions. Now after include in top level they will be
available to all targets:

```
include .env
```
Or you can include them in target:

```
some-rule:
	include .env
	echo $(FOOBAR_VER)
```
(Or maybe the include should create only nake constants, that are available like
`echo {FOOBAR_VER}` ? This avoids mixing envs and nake machinery).


Note, in many cases a typical bash `source` will work the same, and it might support more cases. 

### Configuration

Inside `nake` target:

```
nake:
  shell = sh  # by default is bash

```

Should nake support `nake.conf` file store in `~/.nake` for having user specific
settings?


## Alternatives:

* https://github.com/tj/robo - golang, modern, nice extensions

* https://github.com/ruby/rake - format of ruby

* frontend - https://medium.com/finn-no/makefiles-for-frontend-1779be46461b

* bash scripts :) just defining functions in .sh file. However you need additional layer of choosing which function should be run. 
Other method is to have functions in separate files, but it makes running them harder, code reuse is much harder, and 
maintaing lot of separate scripts is diffucult.



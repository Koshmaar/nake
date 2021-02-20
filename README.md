# nake
nake is make for storing project scripts in nakefile, and running them in easy and shell-compatible way


Problems with make from the point of view of person who wants to run shell scripts:
- need to repeat every command on top of file with .PHONY
- tab is required before every command, without it make won't work and error message will be cryptic
- every instruction is run in separate shell, which doesn't allow to set env variables in one line and use in next
- by default doesn't use any shell extension (needs to be specifically instructed using `SHELL := /bin/bash`)
- syntax used by variables is different from shell, often impossible to use the same command as in shell, adaptation
  is sometimes difficult and time consuming
- single targets can't have individual parameters
- focused on resolving dependencies in C/C++
- a lot of historic baggage, built originally in 80's and 90's which is visible


Aims of this project:
- to replace make for cases when resolving file dependencies doesn't matter, but user want to have scripts for 
  running various project tasks
- allow perfect integration with shell variables and other utilities
- compatibility with all popular shells and platforms
- simple to use, flexible, modern feeling to it
- better autocompletion support (instead of only first words, also middle words ie. setup-api-server could be 
  invoked by typing nake api<tab> and all commands with api would appear) 
- perhaps be make-compatible, in that nakefile can store make compatible syntax in case you need the dependency 
  resolving and other magic. Then running it like `nake make stuff` would run it as `make stuff` (using make 
  from system, with dynamically created makefile). That way one file could store all logic (need to think
  more on this if it makes sense).

Examples:

```
setup:
	python3 -m venv foo_venv
 	source foo_venv/bin/activate
 	pip install -r requirements.txt
```
That's it, complete Nakefile which can be run as `nake setup`. Makefile would need to have &\ at end of lines, 
for the changes made by source to not be lost. 
Nakefile by default checks if command in line returned 0, before proceeding to next one. It can be changed to
ignore errors by prefixing line with - (like in Makefile).


```
FOOBAR_PORT='1337'
FOOBAR_ADDRESS='localhost:' + {FOOBAR_PORT}

api-add-some(baz: str):
	curl {FOOBAR_ADDRESS}/api/v1/baz/{baz} -X POST
```
Nakefile constants are using different syntax than shell variables, so it's harder to mix them and they're 
universal. Syntax is similiar to python. Constants are interpreted once before command is run.
Nakefile targets (api-add-some) can have parameters with types, and are automatically checked at runtime.
Forgetting to provide parameter shows friendly error:

```
$ nake api-add-some
Nake error: target 'api-add-some' called without param 'baz: str'

$ nake api-add-some "99_beers"
  curl localhost:1337/api/v1/baz/99_beers -X POST

```
Lines are echoed. It can be disabled by prefixing line with `@` or `_`. 
Combining `_` and `-` gives `=` - line that is not echoed and return result is ignored (will see if that makes sense :) )
Prefixing with + echoes line, if it was disabled for target.
Prefixing target with one of above modifiers applies this logic automatically to all lines.

Targets can call each other in any place:
```
include foobar.nake

api-add-even-more(baz: str, buzz: int):
  api-add-some(baz)
	curl {FOOBAR_ADDRESS}/api/v1/buzz/{buzz} -X POST

```
Nake tries to detect target calls inside, but if it fails because ie. some other symbol has the same name, it can be 
forced by prefixing with !.

Nakefiles can also be simply included for composition.

WIP

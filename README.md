# nake
nake is make for storing project scripts in nakefile, and running them in easy and shell-compatible way


Problems with make from the point of view of person who wants to run shell scripts:
- need to repeat every command on top of file with .PHONY
- tab is required before every command, without it make won't work and error message will be cryptic
- every instruction is run in separate shell, which doesn't allow to set env variables in one line and use in next
- by default doesn't use any shell extension (needs to be specifically instructed using `SHELL := /bin/bash`)
- syntax used by variables is different from shell, impossible to use the same command as in shell, adaptation
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
- perhaps be make-compatible, in that nakefile can store make compatible syntax in case you need the dependency 
  resolving and other magic. Then running it like `nake make stuff` would run it as `make stuff` (using make 
  from system, with dynamically created makefile). That way one file could store all logic (need to think
  more on this if it makes sense).

Nake operates on Nakefiles which have structure: TBD

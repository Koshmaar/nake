# How to start

Run: `pip3 install -e .`

# Notes

Concatenating commands to single bash -c "" input makes env sharing easy, 
however then it's impossible to show step by step command name, and its output, ie.

```
spam:
    echo "spam"
    echo "spam spam"
```

Output:
```
> echo "spam"; echo "spam spam"; 
spam
spam spam
```

I would expect:
```
> echo "spam" 
spam
> echo "spam spam"
spam spam
```

# TODO

- experiment with creating process and running commands within it - perhaps
  that would make running commands individually and sharing shell session possible

- parse params like here:

```
>>> import shlex, subprocess
>>> command_line = input()
/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
>>> args = shlex.split(command_line)
>>> print(args)
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
>>> p = subprocess.Popen(args) # Success!
```

- more examples
- logging
- auto tests
- linter
- autocomplete

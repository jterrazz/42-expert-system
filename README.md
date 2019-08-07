#42-expert-system

## Presentation
Python implementation of a backward chaining inference engine.
The project receives an input file as the parameter.
This file describes the  set of rules, initial facts and queries.

For example:
```
# Example of input file

# Rules and symbols
C           => E        # C implies E
A + B + C   => D        # A and B and C implies D
A | B       => C        # A or B implies C
A + !B      => F        # A and not B implies F
C | !G      => H        # C or not G implies H
V ^ W       => X        # V xor W implies X
A + B       => Y + Z    # A and B implies Y and Z
C | D       => X | V    # C or D implies X or V
E + F       => !V       # E and F implies not V
A + B       <=> C       # A and B if and only if C
A + B       <=> !C      # A and B if and only if not C

# Initial facts
= ABG

# Queries
?GVX
```

## Implementation

### Project files structure

```
README.md
/src
    ... # Explain files here
```

### Data structure
![Tree structure](http://www.cse.unsw.edu.au/~billw/cs9414/notes/kr/rules/rules1.gif)

```buildoutcfg
class Node:
    
```

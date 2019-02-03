---
layout: post
title: "The Elements of Programming Style"
author: "tomrod"
use_math: true
tags: [coding, engineering, craft, software ]
---

## Context

Data science exists at the convergence of statistics, software crafting, engineering, and applied domain knowledge. Given the diversity of knowledge required, many embark with a solid background in a subset and let curiosity drive their knowledge in others. My own background is in the statistics and applied domain side (economics), so I often seek wisdom from practitioners across the spectrum.

In a recent [Hacker News discussion](https://news.ycombinator.com/item?id=19029713) *The Elements of Programming Style* was recommended.[^1] I gave it a read over the weekend and, in addition to being concise, listed its summary points near the end (that I will post here). Though the book elucidates its ideas uses Fortran as the focal point, the principles have wide applicability. Much of it can be found in the [Zen of Python](https://www.python.org/dev/peps/pep-0020/), though it takes a decidedly FORTRANic approach.

## Comments

Many of the principles are clear

- *Write clearly, don't be too clever.* Often hacks and workarounds gain wide respect for their creativity. But doing so increases the support required to understand, work with, and maintain the code. For example, in Python 2, division was `int` rather than `float`: `1/2 == 0`. If you baked this peculiarity into an application then the upgrade to Python 3 could have nerfed everything. Be explicit -- don't be too clever. **If there is any principle you learn from this post or the book, let this be the first.**
- *Let the machine do the dirty work.* Looking up log-, sin-, and standard normal-tables suffer from user-to-keyboard error. Make the machine do the hard work.
- *Make it (right\|clear\|fail-safe) before making it faster*. Preoptimization is the root of all evil. Make sure what you do works before focusing on runtime speed.
- *Make sure special cases are truly special*, *Take care to branch the right way on equality* and *Test programs at their boundary values.* For example, suppose you are using a `price` field in a dataset. Obviously `price` should never be zero or negative, since the item would sell at a loss. Yet -- you are assuming the upstream coder or data manager didn't do something clever. So instead of assuming it can never be zero, call it out as a special case.

Some of the principles are less clear or focused on `FORTRAN` idiomatic expression
- *Use `IF...ELSE IF....ELSE IF....ELSE...` to implement multi-way branches.* Today we would say use case statements.
- *Initialize contants with DATA statements or INITIAL attributes; initialize variables with executable code.* I don't actually know what an INITIAL attribute in `FORTRAN` is. I presume it has to do with initial assigned values.
- *Use `GOTO`s only to implement a fundamental structure.*
- *Avoid the `FORTRAN` arithmetic `IF`*


## The elements

1. Write clearly -- ***don't be too clever.***
2. Say what you mean, simply and directly.
3. Use library functions.
4. Avoid temporary variables.
5. Write clearly -- don't sacrifice clarity for "efficiency."
6. Let the machine do the dirty work.
7. Replace repetitive expressions by calls to a common function.
8. Parenthesize to avoid ambiguity.
9. Choose variable names that won't be confused.
10. Avoid the `FORTRAN` arithmetic `IF`
11. Avoid unnecessary branches.
12. Don't use conditional branches as a substitute for a logical expression.
13. If a logical expression is hard to understand, try transforming it.
14. Use data arrays to avoid repetitive control sequences
15. Choose a data representation that makes the program simple.
16. Write first in an eay-to-understand pseudo-language; then translate into whatever language you have to use.
17. Use `IF...ELSE IF....ELSE IF....ELSE...` to implement multi-way branches
18. Modularize. Use subroutines.
19. Use `GOTO`s only to implement a fundamental structure.
20. Avoid `GOTO`s completely if you can keep the program readable.
21. Don't patch bad code -- rewrite it.
22. Write and test a big program in small pieces.
23. Use recursive procedures for recursively-defined data structures.
24. Test input for plausibility and validity.
25. Terminate input by end-of-file or marker, not by count
26. Identify bad input; recover if possible.
27. Make input easy to proofread.
28. Use free-form input when possible.
29. Use self-identifying input. Allow defaults. Echo both on output.
30. Make sure all variables are initialized before use.
31. Don't stop at one bug.
32. Use debugging compilers.
33. Initialize constants with `DATA` statements or `INITIAL` attributes; initialize variables with executable code.
34. Watch out for off-by-one errors.
35. Take care to branch the right way on equality.
36. Be careful when a loop exits to the same place from side and bottom.
37. Make sure your code "does nothing" gracefully.
38. Test programs at their boundary values.
39. Check some answers by hand.
40. `10.0` times `0.1` is hardly ever `1.0`.
41. Don't compare floating point numbers solely for equality.
42. Make it right before you make it faster.
43. Make it fail-safe before you make it faster.
44. Make it clear before you make it faster.
45. Don't sacrifice clarity for small gains in "efficiency".
46. Let your compiler do the simple optimizations.
47. Don't strain to re-use code; reorganize instead.
48. Make sure special cases are truly special.
49. Keep it simple to make it faster. 
50. Don't diddle in code to make it faster -- find a better algorithm.
51. Instrument your programs. Measure before making "efficiency" changes
52. Make sure comments and code agree.
53. Don't just echo the code with comments -- make every comment count.
54. Don't comment bad code -- rewrite it.
55. Use variable names that mean something.
56. Use statement labels that mean something.
57. Format a program to help your reader understand it.
58. Document your data layouts.
59. Don't over-comment.



## Footnotes
[^1]: Kernighan, B. W., & Plauger, P. J. (1974). *The elements of programming style.* New York: Bell Telephone Laboratories, Incorporated.
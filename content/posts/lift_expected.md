---
title: "Lifting expected-valued functions for better chaining"
date: 2026-10-03
draft: false
tags: ["c++"]
---

{{< mathjax >}}

{{< lead >}}
Syntax sugar for error-handling using `std::expected`
{{< /lead >}}

Suppose you have some types `In`, `Out`, and that there is a natural way to compute `Out` from `In` in three steps,
as follows:

```cpp
struct A{};
struct B{};
struct In{};
struct Out{};

A computeA(In);
B computeB(A);

Out computeOut(A, B);

Out computeOut(In in)
{
    auto a = computeA(in);
    auto b = computeB(a);
    return computeOut(a, b);
}
```

Now suppose that each of `computeA(In)`, `computeB(In)`, `computeOut(A, B)` should rather return a `std::expected`, with the corresponding
output type as a value type, and some common `Error` type. Assuming that we want to return on the first error encountered, the code will then read:

```cpp
std::expected<A, Error> computeA(In);
std::expected<B, Error> computeB(In);

std::expected<Out, Error> computeOut(In)
{
    auto a = computeA(in);
    if (!a)
    {
        return a.error();
    }

    auto b = computeB(*a);
    if (!b)
    {
        return b.error();
    }

    return computeOut(*a, *b);
}
```
This is clean code, by my standards. But the original clarity of the way the computation flows is not that apparent anymore.

In particular, if you start introducing the propper words of your software's domain, a reader's mind
will have to bear that cognitive load. Some part of the subconcious will try to grasp in what cases some error will occur.
The picture of the computational graph wouldn't pop as easily as in the previous listing. 

One could also consider how this code might change. Maybe the computation will become more involved in the future,
possibly looking like this:
```cpp
std::expected<Out, Error> computeOut(In1 in1, In2 in1)
{
    auto a = computeA(In1);
    if (!a)
    {
        return a.error();
    }

    auto b = computeB(*a, in1);
    if (!b)
    {
        return b.error();
    }

    auto c = computeC(*a, *b, In1);
    if (!c)
    {
        return c.error();
    }

    return computeOut(*a, *b, *c);
}
```
Again, look at the code and imagine that instead of `a`, `b`, `c` you have `access_key`, `apfel_strudel` and `the_thing_we_named_after_the_meeting`.

Here's the version without error-handling:
```cpp
Out computeOut(In1 in1, In2 in2)
{
    auto a = computeA(in1);
    auto b = computeB(a);
    auto c = computeC(a, b, in1);
    return computeOut(a, b, c);
}
```

A solution I though of would be to 'lift' each `compute-` function to accept expected values as arguments,
and do the obvious thing if any of the arguments is in an erroneous state. I use the word 'to lift' in the sense that
the `computeB` function, taking arguments of type `A` and `In1`, is lifted to act on a larger domain that includes expected values
for each argument.

The code would then read:
```cpp
std::expected<Out, Error> computeOut(In1 in1, In2 in2)
{
    auto a = computeA(in1); // lifting here is not necessary
    auto b = lift(computeB)(a);
    auto c = lift(computeC)(a, b, in2);
    return lift(computeOut)(a, b, c);
}
```

The expression `lift(computeB)` should be a callable which accepts `std::expected<A, Error>` and returns `std::expected<B, Error>`, the usual return type of computeB. If the argument has a value, the return is just the value to which computeB is applied, otherwise the error is returned.

The term 'lift' is used in mathematics in the situation that one deals with a function, let's call it $f$, defined on some "small" space $U$,
and one can identify a mapping $h$ between $U$ and some larger space $V$, as well as a mapping $F$ with $V$ as a domain, such that
$f = F \circ h$. One can say that $F$ is a lifted version of $f$. Imagine for a moment that $U$ is just some subset of $V$, and that $h$ is just an identity mapping. The point then is that $F$ is a bit more general than $f$, while being the same as $f$ on $U$. One could say
that by going from $f$ to $F$, $f$ has been lifted to act on the larger space $V$. Note that usually the mapping $h$ is called the lift or lifting of $f$. In correspondence to our code, $f$ would correspond to `computeB` and $F$ would correspond to `lift(computeB)`.
The mapping $h$ would be the mapping that takes an `A a` and turns it into `std::expected<A, Error>{a}`.

Note also that the lifted function, for convenience, should also support receiving a plain type for any of its arguments, as is required by:
```cpp
    auto c = lift(computeC)(a, b, In1);
```

There are some caveats here, though. For one, each call that needs the value of `a` will check the corresponding expected.
Secondly, if we use this pattern in our first example,
```cpp
std::expected<Out, Error> computeOut(In in)
{
    auto a = lift(computeA)(in);
    auto b = lift(computeB)(in);
    return lift(computeOut)(a, b);
}
```
we see that even if the computation of a fails, `computeB` still is called. Or is it? I would bet the compiler can figure out that computeB is pure (if it is) and that there is an easy way to return from the function if a is missing, and so to effectively generate some version of the original error-handling code.

I would argue, however, that it might actually not be such a bad thing if lif(computeB)(in) is called. One could imagine,
for example, that before returning an error from computeB, a log is written, with all the details of what is causing the failure.
Now suppose that both computeA and computeB return errors, each having a different problem with the in argument. If we don't return immediately after finding that a has an error, we get to learn about the problem discovered by computeB. The program is more informative.
Now, of course we will still return the error we got from computeA. Depending on what we want, this program could be modified to actually
gather all the relevant errors from all the steps, and maybe list them all, or aggregate them in some way other than just picking the first error.

But, supposing it matters to us that the second step does not happen, we can do that by using a functionality baked into std::expected, namely `error_or`:
```cpp
std::expected<Out, Error> computeOut(In in)
{
    auto a = lift(computeA)(in);
    auto b = a ? lift(computeB)(in) : a.error();
    return lift(computeOut)(a, b);
}
```
Not quite right? We are suddenly a bit more interested in the error corresponding to `a`. And in a weird way: we are assinging it to `b`.
You know what?
That's just fine. We did not compute `b` because `a` had an error.

This lifting story can be applied to optionals as well.
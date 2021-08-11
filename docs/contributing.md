---
title: Contribution Guide
---

# Contributing for AdaptNLP

To contribute to the AdaptNLP library first make sure you are familiar with the [nbdev](https://nbdev.fast.ai) framework. 

The library is built by the notebooks available in the `nbs` folder, and tests can be run by using `nbdev_test_nbs`.

We follow a special documentation schema based on [docments](https://fastcore.fast.ai/docments) where each param is documented with a comment block next to it, such as below:

```python
def add(
    a:int, # The first number to add
    b:float # The second number to add
) -> (int, float): # The sum of `a` and `b`
  "Adds two numbers together"
  return a+b
```

Please include tests for your functionality in the notebook cells below each function declaration.
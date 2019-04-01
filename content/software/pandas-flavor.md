---
title: "Writing your own flavor of Pandas"
date: 2019-03-17T11:30:07-07:00
draft: true
tags: ["pandas"]
---

Pandas is Python's DataFrame library. If you don't know what a DataFrame is, check out this great [introduction](). If you're a graduate student, professor, data-scientist, or just a person using Python, you absolutely **need** to be using Pandas (one day I'll write that "why dataframes?" article I've been meaning to write).

Pandas is a powerful library. In our newly branded data-driven world, Pandas is foundational to the scientific and data-science Python stack. It seemlessly imports data from many file types, enables your to subset, slice, manipulate and plot your data, and does all of this efficiently. As a result, it has become the _de facto_ tool in various data science workflows across many of the world's biggest companies and research institutions.

Pandas is meant to be a core library. That means Pandas is a foundational package in many scientific and data science Python stacks. It is used in wildly different ways across many different domains--from financial institutions, research institutions, educational settings, machine learning pipelines, etc. As a result, Pandas must maintain a *general* purpose architecture. The Pandas core developers must guard against decisions that might inadvertently specialize its API. I would wager that they turned away many contributions from contributors who trieds to apply their special use-case. While these types of changes are great to see, they don't belong in the core Pandas API.

_So, where do they belong?_ 

Domain-specific additions to Pandas should be made into **Pandas extensions**. An extension is a separate piece of Python code, maybe an object or function, that when imported, _automatically_ hooks into the Pandas API. Let me give you a simple example.

_When should I write a Pandas Extension?_

If you're using Pandas already and find yourself doing *any* of the following actions (not an exhaustive list), you *should* write a Pandas extension. 
* You write the same code again and again.
* Other people could benefit from your code. 
* Your domain-specific plots for your data (something not already in Pandas' plot API).

I often see graduate students in the same lab writing code . -- Reinventing the wheel.

A great example of a domain-specific Pandas extension is [GeoPandas]()--a DataFrame extension for analysis geographic (map) data. This library includes special plotting functionality for visualizing maps.   

## The benefits. 

Standardize your team's Data. Data grammar. Everyone is on the same page.

## How do I write a Pandas Extension.

I recommend using `pandas-flavor`; full disclosure, I am the original creator of the project.

As I mentioned, Pandas released a new API that simplifies extension development. It introduced two class-wrappers (aka decorators): `register_dataframe_accessor` and `register_series_accessor`. To register a new accessor with Pandas, you simple decorate your accessor object with a `register_*` wrapper and pass it a `name`. 

Let's see an example. Let's try creating our own "plot" accessor. 

```python
import matplotlib.pyplot as plt
from pandas_flavor import register_dataframe_accessor

@register_dataframe_accessor("myplot")
class MyPlotAccessor:
    """A new plotting accessor"""
    
    def __init__(self, df):
        self._df = df # We use `_` prefix to hide this attribute.

    def scatter(self, x, y, **kwargs):
        """
        Args: 
            x: name of column for x-axis
            y: name of column for y-axis
        """
        x = self._df[x]
        y = self._df[y]
        return plt.scatter(x, y, **kwargs)
```

These decorators appeared in version 0.23 of Pandas and will not work with earlier versions. Before 0.23, you could patch-in your own accessor with some Python kung-foo; the new `register_*` decorators just simplify the syntax. _Pandas-flavor_ allows you to use the `register_*` syntax in earlier (<0.23) versions of Pandas by handling this Python kung-foo for you.

To write extensions that work with older version of Pandas, I recommend

Pandas is extendable. In fact, if your company, research field, or small team uses Pandas 

How do I write a Pandas Extension?

Pandas

]
Data scientists and software developers should build on it. 



```python
from pandas_flavor import register_dataframe_method

@register_dataframe_method
def my_method(df):
    print(df.shape())


for i in range(10)
    print(i)

class A(object):
    """This is a test"""
    
    def __init__(self, a):
        self.a
    
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>


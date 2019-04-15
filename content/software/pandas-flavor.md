---
title: "Writing your own flavor of Pandas"
date: 2019-04-14
authors: ["zsailer"]
tags: ["pandas", "software"]
---

Pandas is Python's DataFrame library. There are many reasons why should be using DataFrame's in your data science workflow, but I'll have to leave that for another post. Here, I'll show you how to tailor Pandas to your business, research, or personal workflow using Pandas' extension API.

In versions 0.24.x, Pandas introduced a new API for extending Pandas. This API handled the boilerplate code for registering custom **accessors** onto Pandas objects. (an _accessor_ is an object attached to a DataFrame/Series that can access and "mutate" that DataFrame/Series). Specifically, it included two Python decorators: 

1. `register_dataframe_accessor()`
2. `register_series_accessor()`.

[Pandas-flavor](https://github.com/Zsailer/pandas_flavor) is a library that backports this API to earlier versions of Pandas. I recommend using Pandas-flavor when writing custom accessors, since many users probably haven't upgraded to Pandas 0.24.x yet. (Full disclosure---I wrote Pandas-flavor)

## Custom Accessor

Here's how you write an accessor: 

1. Give your accessor a name. Pass this name as an argument to the `register_dataframe_accessor`.
2. Create an accessor class, a Python object. The name of the class doesn't matter. It must have an `__init__()` method and take the Pandas DataFrame/Series as an argument. 
3. Store the DataFrame/Series as a hidden attribute on the Accessor (prefix the attribute with an underscore); I suggest `self._df`.
4. Add your methods and attributes as members of the Accessor class. You can access and mutate the dataframe by affecting the `self._df` attribute.

As an example, here's a simple "finance" accessor that has a "get_losses" method:
```python
# pandas_finance.py module
from pandas_flavor import register_dataframe_accessor

@register_dataframe_accessor("finance")
class FinanceAccessor:
    """Extra methods for finance dataframes."""
    def __init__(self, df):
        self._df = df
        
    def get_losses(self):
        # Slice out values less than 1.
        df = self._df
        losses = df[df["gains_and_losses"] < 0]
        return losses
```
Here's what it would look like to use this accessor:
```python
# Import the pandas_finance module above
import pandas
import pandas_finance
 
df = pandas.DataFrame({
    "value": [5, -5, 45, 65, 30],
    "gains_and_losses": [5, -10, 50, 20, -35]
})

df.finance.get_losses()
```
```
   value  gains_and_losses
1     -5               -10
4     30               -35
```

## Custom Methods
Besides this backport, Pandas-flavor adds another way to extend Pandas:

* `register_dataframe_method()` 
* `register_series_method()`

These two decorators allow you to register custom methods _directly_ onto Pandas' DataFrame/Series. We could adjust the example above to attach the "get_losses" method directly to the DataFrame.
```python
# pandas_finance.py module
from pandas_flavor import register_dataframe_method

@register_dataframe_method
def get_losses(df):
    # Slice out values less than 1.
    losses = df[df["gains_and_losses"] < 0]
    return losses
```
To use this method:
```python
# Import the pandas_finance module above
import pandas
import pandas_finance

df = pandas.DataFrame({
    "value": [5, -5, 45, 65, 30],
    "gains_and_losses": [5, -10, 50, 20, -35]
})

df.get_losses()
```
```
   value  gains_and_losses
1     -5               -10
4     30               -35
```

(_It is likely that Pandas deliberately chose not implement "method registration". If everyone starts monkeypatching DataFrames with custom methods, it could lead to confusion in the Pandas community. The preferred Pandas approach is to namespace your methods by registering an accessor that contains your custom methods._)

## Installing Pandas-flavor

Try out Pandas-flavor and let me know what you think! 

You can install Pandas-flavor with `pip`:
```
pip install pandas-flavor
```
or `conda`:
```
conda install -c conda-forge pandas-flavor
```

## Extensions in the wild
Here is a non-exhaustive list of libraries that use Pandas' (and Pandas-flavor's) new extension API:

* [GeoPandas](http://geopandas.org/): Pandas for geographic data and information.
* [PhyloPandas](https://github.com/Zsailer/phylopandas): the Pandas DataFrame for phylogenetics.
* [Pdvega](https://altair-viz.github.io/pdvega/#): Vega-lite plots from Pandas DataFrames.
* [pyjanitor](https://github.com/ericmjl/pyjanitor): data "cleaning" API for Pandas DataFrames.
* [python-ctd](https://github.com/pyoceans/python-ctd): tools to load hydrographic data into Pandas DataFrames.
* [Pandas' plot API](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html): yes, this is part of Pandas' core library, but acts like an extension.

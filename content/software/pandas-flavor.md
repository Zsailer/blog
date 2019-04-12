---
title: "Writing your own flavor of Pandas"
date: 2019-04-05
authors: ["zsailer"]
draft: true
tags: ["pandas", "software"]
---

## The case for Pandas extensions
```python
>>> import pandas
>>> import myextension
>>> df = pandas.read_csv('my-data.csv')
>>> df.myextension.say_hello()
"Hello, world!"
```
Pandas is Python's DataFrame library. There are many reasons why should be using DataFrame's in your data science workflow, but I'll have to leave that for another article. In this article, I'll show you how to tailor Pandas to your business, research, or personal workflow using Pandas' extension API.

Pandas is a powerful library. You can read data from various file types and manipulate and plot that using a highly memory-efficient data structure and API. It has become a foundational library in various scientific Python stacks and the _de facto_ tool for data science in many companies and research institutions around the world.

Pandas is also a general library. You'll find Pandas at various financial institutions, research institutions, classrooms, etc. To meet the needs of these many different domains, the core Pandas development team has worked hard to keep the API fairly general.

Thus, Pandas does not (and should not) provide domain-specific functionality. I would wager that the core Pandas team has turned away many contributions from people who trieds to add functions for their special use-case. While these types of additions are great to see, they don't belong in the core Pandas API.

_So, where do my domain-specific additions belong?_ 

They belong in a **Pandas extension**. An extension is a separate piece of Python code, maybe an object or function, that _automatically_ hooks into the Pandas API when imported. 

Let's imagine, for example, you're a financial consultant, and you've developed a nice set of functions to analyze financial data into a Pandas DataFrame. This is a lot of work. You wrote your own  `read_portfolio` and `to_portfolio` functions to read/write your data, following Pandas' API design. You have code that sets each column to the correct data-type. You've formatted the date-time columns appropriately (I always have to look this up!). You have functions that slice out the capital gains for your clients. Maybe you even wrote some handy Matplotlib code to visualize your clients portfolio in a simple way.  

_How do you share this code with others?_ Clearly, this does not belong in the core Pandas library. A "finance DataFrame" only serves a small subset of Pandas users. However, your code follows Pandas' API design and directly affects Pandas' core objects. You want your users to treat this code like its "Pandas for finance" (or whatever domain you're in). 

That's when you should write a pandas extension. Here's what your Pandas extension might look like:

```python
import pandas                      					# Import pandas
import pandas_finance             					# Import your extension

df = pandas.DataFrame({            					# Create a DataFrame
    "value": [5, -5, 45, 65, 30]
    "gain_or_loss": [5, -10, 50, 20, -35]
})

# Get rows with negative numbers in 
# "gain_or_loss" column.
df.finance.get_losses()          					# That dataframe has a `finance` accessor.
```

By simply importing `pandas_finance` in the example above, the `pandas.DataFrame` has a `finance`  attribute (also called an "accessor") and an extra method, `get_losses`. The user acts directly on their DataFrame. They can all the "finance" attribute, hit _tab_, and see all the special functions you've added. 

Pandas extensions are meant to "feel" like Pandas code, even if they don't come from the core Pandas library. They live as separate Python packages that users can install and import. When they are imported, they automatically "patch" their custom functionality onto Pandas' objects.

There are many Pandas extensions that exist today. Here is a non-exhaustive list in case you're interested:

* [GeoPandas](http://geopandas.org/): Pandas for geographic data and information.
* [PhyloPandas](https://github.com/Zsailer/phylopandas): the Pandas DataFrame for phylogenetics.
* [Pdvega](https://altair-viz.github.io/pdvega/#): Vega-lite plots from Pandas DataFrames.
* [pyjanitor](https://github.com/ericmjl/pyjanitor): data "cleaning" API for Pandas DataFrames.
* [Pandas' `plot` API](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html): yes, this is part of Pandas' core library, but acts like an extension.

## How to write a Pandas Extension.

I recommend you use the Python library, [Pandas-flavor](https://github.com/Zsailer/pandas_flavor); I'll explain why in a minute. (Full disclosure: I am the original creator of this library.)

First, Pandas v0.24 introduced a new, simpler API for creating Pandas extensions. Essentially, it covered the boilerplate code for attaching extensions under the hood. It included two Python decorators: `register_dataframe_accessor` and `register_series_accessor`. Let me break down these magical functions. 

I'll start by showing an example. Let's create the "finance" extension from before. Put the following code inside a `pandas_finances.py` file:
```python
# Import pandas's extension API
from pandas.api.extensions import register_dataframe_accessor

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
This 
```python
import pandas
import pandas_finance

df = pandas.DataFrame({
    "value": [5, -5, 45, 65, 30]
    "gain_or_loss": [5, -10, 50, 20, -35]
})

df.finance.get_losses()
```


* The "`register`" part acknowledges that these functions "monkey-patch" or add functionality to Pandas DataFrame or Series objects after Pandas has been imported.  
* An "`accessor`" is an object that attaches to a Pandas object that can access and "mutate" (i.e. change) the object. In the example above, the `finance` attribute is an accessor.

As an example, let's create the finance extension above using  `register_dataframe_accessor`. We'll put this code inside a file named `pandas_finances.py`.


When we import `pandas_finances` (like in the example before), a `finance` accessor will appear on all Pandas DataFrames in this session.

To write such an extension, you'll need:

1. To give the accessor a name, i.e. the DataFrame's attribute you'll call. You'll pass this name as an argument to the `register_dataframe_accessor`.
2. To create an accessor class, a Python object. Name it whatever you like. It must have an `__init__` method whose only argument is the Pandas DataFrame (or Series, if using `register_series_accessor`). 
3. To store the Pandas object as a hidden attribute on the Accessor (prefix the attribute with an underscore); I suggest `self._df`.
4. To add your methods and attributes as members of the Accessor class. You can access and mutate the dataframe by affecting the `self._df` attribute.

That's it! You can start writing your own **Pandas extension** today!

## Extending Pandas with Pandas-flavor

As I mentioned, Pandas added this extension API in v0.24, which means this won't work with earlier versions of Pandas. That's one reason why I wrote [Pandas-flavor](https://github.com/Zsailer/pandas_flavor). 

Pandas-flavor backports this extension API to earlier versions of Pandas. You can import the same decorators, `register_dataframe_accessors` and `register_series_accessors` and it will work with most versions of Pandas. Just replace the the import statements above:

```python
from pandas_flavor import register_dataframe_accessor
```

Pandas-flavor also allows you to 

[WIP]




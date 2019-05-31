---
title: "NetworkX meets Altair"
date: 2019-05-31
draft: false
authors: ["zsailer"]
tags: ["jupyter"]
images:
- /path/to/picture
---

**NxAltair** is a small library I created last year to draw NetworkX graphs in Altair. [Altair](https://altair-viz.github.io/) is a declarative Python API for creating interactive visualizations powered by Vega. [NetworkX](https://networkx.github.io/) is a broadly used library for analyzing network data. 

NetworkX comes with a simple but powerful drawing API out-of-the-box. It's built on Matplotlib and allows you to customize the drawing of nodes, edges, and labels separately. One major downside of using Matplotlib here is that the figure is *static*. To explore the data further, we would need to re-render the figure in a different configuration.

## Interactivity for Free

NxAltair brings simple interactivity that is particularly useful for analyzing networks. I'll demonstrate this with examples. Here is a simple NetworkX example using the `draw_networkx` function: 
```python
import networkx as nx

# Generate a random graph
G = nx.fast_gnp_random_graph(n=20, p=0.25)

# Add store some random attributes on each node.
for n in G.nodes():
    G.nodes[n]['weight'] = np.random.randn()
    G.nodes[n]['name'] = np.random.randint(1000)
    G.nodes[n]['viable'] = np.random.choice(['yes', 'no'])

# Compute positions for viz.
pos = nx.spring_layout(G)

# Draw the graph using matplotlib
chart = nx.draw_networkx(G, pos=pos)
```
![](/software/nx_altair/data/networkx-mpl.png)


If we replace NetworkX's draw method with NxAltair's, we get an Altair chart. And calling `.interactive()` adds "pan and zoom". 
```python
# Import NxAltair
import nx_altair as nxa

# Swap nx with nxa.
chart = nxa.draw_networkx(G, pos=pos)

# Add pan and zoom!
chart.interactive()
```
<div id="vis"></div>

<script type="text/javascript">
  var spec = "data/chart1.json";
  vegaEmbed('#vis', spec).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
</script>

This is already useful for network figures that are crowded by many nodes and edges. We can zoom on regions of interest. But the interactivity doesn't stop there...

## Altair-level interactivity

Because NxAltair returns Altair charts, we can leverage most of the features inside of Altair. For example, we easily add tool-tips to label our nodes — hover over any node and quickly view its data:

```python
# Set the node_tooltip argument.
chart = nxa.draw_networkx(
    G, pos=pos,
    node_tooltip=["name", "weight", "viable"]
).interactive()
```
<div id="vis2"></div>

<script type="text/javascript">
  var spec = "data/chart2.json";
  vegaEmbed('#vis2', spec).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
</script>

NxAltair also has a feature not available in NetworkX. It can style the visualization using node and edge attributes. The values of those attributes are mapped onto properties of the visualization. For example, here we use the nodes "weight" attribute to color the nodes:

```python
chart = nxa.draw_networkx(
    G=G,
    pos=pos,
    node_size=200,
    node_color='weight',
    cmap='viridis',
    width='weight',
).interactive()
```
<div id="vis3"></div>

<script type="text/javascript">
  var spec = "data/chart3.json";
  vegaEmbed('#vis3', spec).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
</script>
This is particularly handy in XX.


```python
# Draw a basic chart
chart = nxa.draw_networkx(
    G, pos=pos,
)

# Get the node layer
edges = chart.layer[0]
nodes = chart.layer[1]

# Build a brush
brush = alt.selection_interval(encodings=['x', 'y'])
color = alt.Color('viable:N',  legend=None)

# Condition nodes based on brush
nodes = nodes.encode(
    fill=alt.condition(brush, color, alt.value('gray')),
).add_selection(
    brush
)

# Create a bar graph to show highlighted nodes.
bars = alt.Chart(nodes.data).mark_bar().encode(
    x=alt.X('count()', scale=alt.Scale(domain=(0,20))),
    y='viable',
    color='viable',
).transform_filter(
    brush
)

alt.vconcat(edges+nodes, bars)
```

<div id="vis4"></div>

<script type="text/javascript">
  var spec = "data/chart4.json";
  vegaEmbed('#vis4', spec).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
</script>



## API Design (may delete)

I followed three requirements when building NXAltair:

1. Build an API that's as close to NetworkX as possible
2. Return Altair `Chart`s that can be easily customized using Altair's API.
3. Allow users to declare attributes as visual features.

## Conclusion
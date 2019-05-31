import networkx as nx
import nx_altair as nxa
import altair as alt
import numpy as np
import matplotlib.pyplot as plt

# Generate a random graph
G = nx.fast_gnp_random_graph(n=30, p=0.25)

# Add attributes to each node.
for n in G.nodes():
    G.nodes[n]['weight'] = np.random.randn()
    G.nodes[n]['name'] = np.random.randint(1000)
    G.nodes[n]['viable'] = np.random.choice(['yes', 'no'])
    
# Add attributes to edge.    
for e in G.edges():
    G.edges[(e[0],e[1])]['weight'] = np.random.uniform(1, 10)

# Compute positions for viz.
pos = nx.spring_layout(G)

fig = plt.figure()
chart = nx.draw_networkx(
    G=G,
    pos=pos
)

fig.savefig('../data/networkx-mpl.png', format='png', dpi=80)

# Show it as an interactive plot!
chart = nxa.draw_networkx(
    G=G,
    pos=pos,
).interactive()

chart.save('../data/chart1.json')

chart = nxa.draw_networkx(
    G=G,
    pos=pos,
    node_tooltip=["name", "weight", "viable"]
).interactive()

chart.save('../data/chart2.json')

chart = nxa.draw_networkx(
    G=G,
    pos=pos,
    node_size=200,
    node_color='weight',
    cmap='viridis',
    width='weight',
).interactive()

chart.save('../data/chart3.json')

# Draw a basic chart
chart = nxa.draw_networkx(
    G=G,
    pos=pos,
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

chart = alt.vconcat(edges+nodes, bars)

chart.save('../data/chart4.json')
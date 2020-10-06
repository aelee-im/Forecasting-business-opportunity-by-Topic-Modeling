# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:20:14 2020

@author: aelee.im
"""
import numpy as np
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# convert distribution matrix(array) to standard adjacency matrix(array)
edit_lda_output = np.where(lda_output < np.mean(lda_output), 0, lda_output)
print(np.sum(edit_lda_output))
print(np.count_nonzero(edit_lda_output))
non_zero_avg = np.sum(edit_lda_output)/np.count_nonzero(edit_lda_output)
print(non_zero_avg)
cut_off_avg = non_zero_avg # use the average of non zero value of lda_output
standard_vsm = np.where(lda_output < cut_off_avg, 0, 1)

# creating pseudo adjacency matrix(array)
s_tot = []

# range of cut_off value : from 0 to 1 by interval of 0.01
# s means a simple match coefficient(i.d.(a+d)/(a+b+c+d)) between standard vsm and pseudo vsm
for i in np.arange(0, 1.001, 0.001):
    cut_off_pseudo = i
    pseudo_vsm = np.where(lda_output < cut_off_pseudo, 0, 1)
    a = ((standard_vsm == 1) & (pseudo_vsm == 1)).sum()
    b = ((standard_vsm == 1) & (pseudo_vsm == 0)).sum()
    c = ((standard_vsm == 0) & (pseudo_vsm == 1)).sum()
    d = ((standard_vsm == 0) & (pseudo_vsm == 0)).sum()
    s = (a+d)/(a+b+c+d)
    s_tot.append((i,s))
    print(i, s)

df_s = pd.DataFrame(s_tot, columns = ['cut_off_pseudo', 'match_coeff_s'])
print(df_s.head())

df_s.plot.line(x='cut_off_pseudo', y='match_coeff_s')   

# find out the maximum value of match coefficient 's' and their cut_off value 
print(df_s.loc[df_s['match_coeff_s'].idxmax()])

# create optimum adjacency matrix with best cut_off value(0.03)

cut_off_best = 0.884
best_vsm = np.where(lda_output < cut_off_best, 0, 1)

#topicnames = ["Topic" + str(i) for i in range(best_lda_model.n_components)]
topicnames = ["Topic" + str(i) for i in range(len(df_topic_keywords.index))]
docnames = full_text_list['patent_id'].values.tolist()
df_best = pd.DataFrame(np.round(best_vsm, 2), columns=topicnames, index=docnames)

df_best_asint = df_best.astype(int)
coocc = df_best_asint.T.dot(df_best_asint)
np.fill_diagonal(coocc.values, 0)



#add weights to edges
edge_list = [] #test networkx
for index, row in coocc.iterrows():
    i = 0
    for col in row:
        weight = col
        edge_list.append((index, coocc.columns[i], weight))
        i += 1

#Remove edge if 0.0
updated_edge_list = [x for x in edge_list if not x[2] == 0.0]

#create duple of char, occurance in novel
node_list = []
for i in topicnames:
    for e in updated_edge_list:
        if i == e[0] and i == e[1]:
           node_list.append((i, e[2]))
for i in node_list:
    if i[1] == 0.0:
        node_list.remove(i)

#remove self references
for i in updated_edge_list:
    if i[0] == i[1]:
        updated_edge_list.remove(i)
        
#set canvas size
plt.subplots(figsize=(14,14))

#networkx graph time!
G = nx.Graph()

for i in sorted(node_list):
    G.add_node(i[0], size = i[1])
    
G.add_weighted_edges_from(updated_edge_list)

node_order = topicnames
#reorder node list
updated_node_order = []
for i in node_order:
    for x in node_list:
        if x[0] == i:
            updated_node_order.append(x)
            
#reorder edge list - this was a pain
test = nx.get_edge_attributes(G, 'weight')
updated_again_edges = []
for i in nx.edges(G):
    for x in test.keys():
        if i[0] == x[0] and i[1] == x[1]:
            updated_again_edges.append(test[x])
#drawing custimization
node_scalar = 2
edge_scalar = 0.0001
sizes = [x[1]*node_scalar for x in updated_node_order]
widths = [x*edge_scalar for x in updated_again_edges]

#draw the graph
pos = nx.spring_layout(G, k=0.42, iterations=17)

nx.draw(G, pos, with_labels=True, font_size = 8, font_weight = 'bold', node_color = 'r', 
        node_size = sizes, width = widths)        

plt.axis('off')
plt.savefig("test_network.png") # save as png

## calculate degree centrality,
c = nx.closeness_centrality(G)
# convert to dataframe
closseness_centrality = pd.DataFrame(list(c.items()), columns=['topic', 'closeness_centrality'])

##############################################################################
# plotting bar chart for importance level
import random
import matplotlib.pyplot as plt
# Prepare Data
new_final_importance = closseness_centrality.sort_values('closeness_centrality',ascending=False)
n = new_final_importance['topic'].unique().__len__()+1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

# Plot Bars
plt.figure(figsize=(16,10), dpi= 80)
plt.bar(new_final_importance['topic'], new_final_importance['closeness_centrality'], color=c, width=.5)

# Decoration - rotation of x-label, adding title and y-label
plt.gca().set_xticklabels(new_final_satisfy['topic'], rotation=60, horizontalalignment= 'right')
plt.title("Score of importance level per each topic", fontsize=22)
plt.ylabel('Score of Closeness Centrality(importance level)')
#plt.ylim(0, 45)
plt.show()
plt.savefig("importance_level.png")


##### cf>
## set degree centrality metrics on each node,
nx.set_node_attributes(G, c, 'cc')

sorted(G.nodes(data=True), key = lambda x: x[1]['cc'], reverse=True)


# (optional) for calculating closeness centrality manually
sum(nx.shortest_path_length(G,32).values())
print((len(G.nodes())-1)/sum(nx.shortest_path_length(G, 'Topic1', method='dijkstra').values()))
nx.shortest_path_length(G, 'Topic1', method='dijkstra').values()


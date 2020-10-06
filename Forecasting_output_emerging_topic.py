# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:15:23 2020

@author: aelee.im
"""
topic_list = df_document_topic.loc[:, 'Topic0':'Topic29']
citation_list = df_citation_final['citation']
citation_list = citation_list.astype(float)

satisfy = []

# Yields a tuple of column name and series for each column in the dataframe
for (columnName, columnData) in topic_list.iteritems():
    sum=0
    citation_stock=0
    for i in range(len(columnData)):
        init_citation_stock = columnData[i]*citation_list[i]
        sum += init_citation_stock
    citation_stock = sum
    satisfy.append((columnName, citation_stock))
    
    print(columnName, citation_stock)

# convert list to data frame         
final_satisfy = pd.DataFrame(satisfy, columns = ['topic' , 'citation_stock'])

##############################################################################
# plotting bar chart for satisfaction level
import random
import matplotlib.pyplot as plt
# Prepare Data
new_final_satisfy = final_satisfy.sort_values('citation_stock',ascending=False)
n = new_final_satisfy['topic'].unique().__len__()+1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

# Plot Bars
plt.figure(figsize=(16,10), dpi= 80)
plt.bar(new_final_satisfy['topic'], new_final_satisfy['citation_stock'], color=c, width=.5)

# Decoration
plt.gca().set_xticklabels(new_final_satisfy['topic'], rotation=60, horizontalalignment= 'right')
plt.title("Score of satisfection level per each topic", fontsize=22)
plt.ylabel('Score of citation stock(satisfection level)')
plt.show()
plt.savefig("citation_stock.jpg")

##############################################################################

ofit_map = pd.merge(closseness_centrality, final_satisfy, how='left', on=['topic'])

# OFIT mapping : x-axis('closeness_centrality'), y-axis('citation_stock')
# scatter plot here..
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

# average of importance
avg_cent = closseness_centrality['closeness_centrality'].mean()
print(avg_cent) # => avg_cent = 0.7940293400835674

fig=plt.figure()
ax=fig.add_axes([0,0,1,1])
ax.scatter(ofit_map['closeness_centrality'], ofit_map['citation_stock'], color='r')
ax.set_xlabel('importance of topic (closeness_centrality)')
ax.set_ylabel('Satisfection of topic (citation_stock)')
ax.set_title('Opportunity-focused Innovation Topic(OFIT) map')
for i, txt in enumerate(ofit_map['topic']):
    ax.annotate(txt, (ofit_map['closeness_centrality'][i], ofit_map['citation_stock'][i]))

line = mlines.Line2D([0, 1], [0, 1], color='red')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)

# 0.618 = (avg_cent-0.45)/0.55 (* avg_cent = 0.7940293400835674)
line = mlines.Line2D([0.6232073678495466, 1], [0, 1], color='blue')
transform = ax.transAxes
line.set_transform(transform)
ax.add_line(line)
ax.fill_between(ofit_map['closeness_centrality'], line, color= 'skyblue')

plt.show()
plt.savefig("test_OFIT.png") # save as png

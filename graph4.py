import networkx as nx
import dill
import matplotlib.pyplot as plt
#import tkinter
import itertools
import operator

#nms = dill.load(open('nms1_list.pkd', 'rb'))
nmp1 = dill.load(open('nmp_new.pkd', 'rb'))
nmp2 = dill.load(open('nmp_new_td.pkd', 'rb'))



print('Size of nmp is:', len(nmp1))
print('Size of nmp is:', len(nmp2))
nmp = nmp1 + nmp2
print('Size of nmp is:', len(nmp))



#nmp = nmp[0:80000]
G=nx.Graph()


# for i in nmp:
#     #print(i)
#     if not 'Jr.' in i or 'M.D.' in i:
#         if G.has_edge(i[0],i[1]):
#             G.edges[i[0], i[1]]['weight'] += 1
#             #print(G.edges[i[0], i[1]]['weight'])
#         else:
#             G.add_edge(*i, weight = 1)

for i in nmp:
    #print(i)
    if G.has_edge(i[0],i[1]):
        G.edges[i[0], i[1]]['weight'] += 1
            #print(G.edges[i[0], i[1]]['weight'])
    else:
        G.add_edge(*i, weight = 1)


#nx.draw(G)
#plt.savefig("simple_path.png") # save as png

print('\n\n List of folks with large weight\n')

# Question 5
# ct = 0
# bf = []
# for (u,v,d) in G.edges(data='weight'):
#     if d >9:
#         #print(u, v, d)
#         bf.append(((u, v), d))
#         ct += 1
#
# sorted_bf = sorted(bf, key=operator.itemgetter(1))
# sorted_bf.reverse()
# print(sorted_bf[3:103])


#Degree of a person (question 3)
nd = G.degree
sorted_nd = sorted(nd, key=operator.itemgetter(1))
sorted_nd.reverse()
print(sorted_nd[0:100])

nd_50 = []
for i in sorted_nd:
    nd_50.append((i[0], int(i[1]*1.2)))
print(nd_50[0:100])



# #PageRank (Question 4)
# pr = nx.pagerank(G)
# sorted_pr = sorted(pr.items(), key=operator.itemgetter(1))
# sorted_pr.reverse()
# print(sorted_pr[0:100])
from graph_tool.all import *
import scipy
from pylab import *
root_user = "That_Colin"

g = Graph(directed = False)

#go through root list
def build_graph(graph):
    #root_list is the root_user's followers
    root_list = graph[root_user]
    #create the root_node
    root_node = g.add_vertex()
    graph_index = {}

    vprop = g.new_vertex_property("string")
    vprop[root_node] = str(root_user)
    g.vertex_properties["name"] = vprop
    i = 0

    #create root_user's node network with all 1st degree connections
    for user in root_list:
        graph_index[user] = []
        i += 1
        graph_index[user].append(i)

        user_vertex = g.add_vertex()

        print("user ", user, "'s place in index is", i)

        #vprop takes the user name as str
        vprop[user_vertex] = str(user)

        #connect vertex to root node
        e = g.add_edge(user_vertex, g.vertex(0))

    #traverse initial dictionary
    #which is the root_node's follower's
    for user in root_list:
        #don't need to create vertex for user
        #create a list for every follower's followers
        user_list = graph[user]

        user = graph_index[str(user)]
        print(user[0])
        user_vertex = g.vertex(user[0])

        #unk_user is a 2nd degree connection but it MIGHT be 1st degree too
        for unk_user in user_list:

            if unk_user in graph:

                #this means unk_user is a 1st degree connection
                #unk_user should already exist
                print(user," shares follower ", unk_user)

                #search dictionary for shared follower
                unk_user = graph_index[str(unk_user)]
                #get the index of the vertex for shared follower
                unk_vertex = g.vertex(unk_user[0])
                #print the vertex objects
                print(unk_vertex, user_vertex)

                #add a connection from user's 1st degree follower, to 1st degree user
                unk_e = g.add_edge(unk_vertex, user_vertex)

                #so unk_user should be an already existant node,
                #look up g.vertex(index) of node that coresponds to unk_user in root_list
                #add edge between user and other user.

            else:
                #if it's not in list, it's a random user 
                #it doesn't share a 1st degree connection with root
                #these don't deserve a name
                unk_vertex = g.add_vertex()
                unk_e = g.add_edge(unk_vertex, user_vertex)


    pos = sfdp_layout(g)

    print(g)
    #vertex_text = ug.vertex_properties["name"]
    graph_draw(g, pos=pos, vertex_text = g.vertex_properties["name"], vertex_font_size = 16, edge_pen_width = 20, output_size = (8000, 8000), bg_color=[0,0,0,0], output = "new_nodes2.png")

def parse():
    graph = {}

    file = open('organized_followers.csv')

    for line in file:
        split_line = line[:-2].split('|')
        user = split_line[0]
        graph[user] = []
        common_connection = 0

        for i in range(1, len(split_line)):
            follower = split_line[i]

            if split_line[i] in graph:
                vertex = graph[follower]
                common_connection += 1
            graph[user].append(split_line[i])
        # print(user, "has ", common_connection, "common connections.")
    # print(graph)
    return graph

graph = parse()
# for user in graph:
#     print('user %s has %d followers' % (user, len(graph[user])))

build_graph(graph)


# g = Graph(directed=True)
# print(g)
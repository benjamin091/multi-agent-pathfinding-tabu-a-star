#!/usr/bin/env python
# coding: utf-8

# In[1]:


import heapq

class Node:

    def __init__(self, parent=None, position=None, index_dict=0):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, index_dict=0):
   
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node

            while current is not None:
                path.append(current.position)
                current = current.parent

            #return path[::-1] # Return reversed path

            path_dict = {}
            for index, value in enumerate(path[::-1]):
                path_dict[index+index_dict] = value #index_dict ist eine Ergänzung für lokale Lösungen in Tabusearch
            return path_dict

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def evaluierung(liste_agents, lambda_collision = 100):
    total_length = 0
    collision_count = 0
    collision_swap_count = 0
    lambda_collision = 100

    for index, value in enumerate(liste_agents):
        total_length += len(value)

    #Liste nach Länge der Dict. sortieren
    liste_agents.sort(key = len, reverse=True)
    len_liste_agents = len(liste_agents)
    liste_agents_work = liste_agents


    for index_i, value_i in enumerate(liste_agents_work[1]):
        element_min = liste_agents_work[-1]

        if index_i > len(element_min)-1:
            liste_agents_work.pop()

        for index_j in range(len(liste_agents_work)):

            for index_k in range(index_j+1, len(liste_agents_work)):
                if index_i > 0:
                    if liste_agents[index_j][index_i] == liste_agents[index_k][index_i]: 
                        collision_count+=1

                    elif (liste_agents[index_j][index_i] == liste_agents[index_k][index_i-1] and liste_agents[index_j][index_i-1] == liste_agents[index_k][index_i]):
                        collision_swap_count+=1

    return total_length + lambda_collision * (collision_count+collision_swap_count)


# In[158]:


def suche_kollision(liste_agents):
    list_collision = []

    #Liste nach Länge der Dict. sortieren
    liste_agents.sort(key = len, reverse=True)
    len_liste_agents = len(liste_agents)
    liste_agents_work = liste_agents


    for index_i, value_i in enumerate(liste_agents_work[1]): #Index des zweitlängsten Agenten dient als Referenzindex
        element_min = liste_agents_work[-1] #Speichern der Länge des Agenten mit der geringsten Länge

        while index_i > len(element_min)-1: #wenn/solange Index größer als Agent mit der geringsten Länge, entferne diesen (Update der Indizes in der nächsten Runde)
            liste_agents_work.pop()
            element_min = liste_agents_work[-1]

        for index_j in range(len(liste_agents_work)):

            for index_k in range(index_j+1, len(liste_agents_work)):
                if index_i > 0:

                    if liste_agents[index_j][index_i] == liste_agents[index_k][index_i]: 
                        list_collision.append([index_j,index_i-1,liste_agents[index_j][index_i-1]])
                        list_collision.append([index_k,index_i-1,liste_agents[index_k][index_i-1]])
       
                        return list_collision
                        
                    elif (liste_agents[index_j][index_i] == liste_agents[index_k][index_i-1] and liste_agents[index_j][index_i-1] == liste_agents[index_k][index_i]):
                        list_collision.append([index_j,index_i-1,liste_agents[index_j][index_i-1]])
                        list_collision.append([index_k,index_i-1,liste_agents[index_k][index_i-1]])

                        return list_collision



def tabu_liste_suche(list_collision, liste_neighbours, tabu_liste, aspiration_crit_list, tabu_tenure):
    optimale_lsg = []
    if tabu_liste:
        position_tabu = []
        tabu_liste_1 = []
        tabu_liste_2 = []

        for _, value_tabu in enumerate(tabu_liste):
            tabu_liste_1.append(value_tabu[0][0])
            tabu_liste_2.append(value_tabu[1][0])

        if (list_collision[0][2] in tabu_liste_1 and list_collision[1][2] in tabu_liste_2) or (list_collision[0][2] in tabu_liste_2 and list_collision[1][2] in tabu_liste_1):
            optimale_lsg_tabutenure_list = heapq.nsmallest(tabu_tenure+1, liste_neighbours, key=lambda x: x[2])

            for index_tabu, value_tabu in enumerate(tabu_liste):
                if (list_collision[0][2] == value_tabu[0][0] and list_collision[1][2] == value_tabu[1][0]) or (list_collision[0][2] == value_tabu[1][0] and list_collision[1][2] == value_tabu[0][0]):
                    position_tabu.append(index_tabu)

                else:

                    continue

            for index_opt, value_opt in enumerate(optimale_lsg_tabutenure_list[:-1]):
                if index_opt >= len(tabu_liste):
                    continue

                if position_tabu:
                    for _, value_position in enumerate(position_tabu):
                        if (tabu_liste[value_position][0][1] == value_opt[0][list_collision[0][1]+1] and tabu_liste[value_position][1][1] == value_opt[1][list_collision[1][1]+1]) or (tabu_liste[value_position][0][1] == value_opt[1][list_collision[1][1]+1] and tabu_liste[value_position][1][1] == value_opt[0][list_collision[0][1]+1]):    
                            if value_opt[2] < min(aspiration_crit_list):
                                optimale_lsg = [value_opt[0], value_opt[1], value_opt[2]]
                                aspiration_crit_list.append(value_opt[2])
                                
                                return optimale_lsg, tabu_liste, aspiration_crit_list
                            continue
                        
                        else:
                            optimale_lsg = [value_opt[0], value_opt[1], value_opt[2]]
                            aspiration_crit_list.append(value_opt[2])
                            return optimale_lsg, tabu_liste, aspiration_crit_list

            if not optimale_lsg:
                optimale_lsg = optimale_lsg_tabutenure_list[-1]
                aspiration_crit_list.append(optimale_lsg[-1])
                
                return optimale_lsg, tabu_liste, aspiration_crit_list
        else:
            optimale_lsg = min(liste_neighbours, key=lambda x: x[2])
            aspiration_crit_list.append(optimale_lsg[-1])

            return optimale_lsg, tabu_liste, aspiration_crit_list
    else:
        optimale_lsg = min(liste_neighbours, key=lambda x: x[2])
        aspiration_crit_list.append(optimale_lsg[-1])

        return optimale_lsg, tabu_liste, aspiration_crit_list


def optimization_algorithm(maze, max_iterations, tabu_tenure, liste_agents):

    tabu_liste = []
    aspiration_crit_list = []
    goal_agents = []

    for i in range(max_iterations):
        liste_neighbours = []

        liste_collision_1 = []
        liste_collision_2 = []
        dict_collision_1 = {}
        dict_collision_2 = {}
        list_collision = suche_kollision(liste_agents)
        
        if list_collision == None:
            break

        #Anpassung der Reihenfolge der Zieltupel (Sortierung in suche_kollision)
        goal_agents = goal_agents[:0]
        for index_goal, _ in enumerate(liste_agents):
            goal_agents.append(list(liste_agents[index_goal].items())[-1][1])

        #Extrahieren der Tupel bis kurz vor der Kollision
        dict_collision_1 = {key: liste_agents[list_collision[0][0]][key] for key in list(range(0,list_collision[0][1]+1))}
        dict_collision_2 = {key: liste_agents[list_collision[1][0]][key] for key in list(range(0,list_collision[1][1]+1))}

        #Generierung neuer Lsgen
        for new_position in [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            dict_collision_1[list_collision[0][1]+1] = (dict_collision_1[list_collision[0][1]][0] + new_position[0], dict_collision_1[list_collision[0][1]][1] + new_position[1])
            dict_collision_2[list_collision[1][1]+1] = (dict_collision_2[list_collision[1][1]][0] + new_position[0], dict_collision_2[list_collision[1][1]][1] + new_position[1])

            if maze[dict_collision_1[list_collision[0][1]+1][0]][dict_collision_1[list_collision[0][1]+1][1]] != 0 or maze[dict_collision_2[list_collision[1][1]+1][0]][dict_collision_2[list_collision[1][1]+1][1]] != 0:
                continue

            liste_collision_1.append(dict_collision_1.copy()) #Hinzufügen er gewonnen Lsg
            dict_collision_1.pop(list_collision[0][1]+1) #Löschen der gewonnen Lsg, um für die nächste Platz zu machen

            liste_collision_2.append(dict_collision_2.copy())
            dict_collision_2.pop(list_collision[1][1]+1)

        liste_neighbours = [[a, b, None] for a in liste_collision_1 for b in liste_collision_2]

        #Suche nach Lsg mit A* auf Basis der Nachbarlsgen
        for index, value in enumerate(liste_neighbours):
            path_neighbour_1 = astar(maze, list(value[0].items())[-1][1], goal_agents[list_collision[0][0]], list(value[0].items())[-1][0])
            path_neighbour_2 = astar(maze, list(value[1].items())[-1][1], goal_agents[list_collision[1][0]], list(value[1].items())[-1][0])

            liste_neighbours[index][0] = liste_neighbours[index][0] | path_neighbour_1
            liste_neighbours[index][1] = liste_neighbours[index][1] | path_neighbour_2

        for index, value in enumerate(liste_neighbours):
            liste_neighbours[index][2] = evaluierung(value[:2])

        #Überprüfung Tabuliste
        optimale_lsg, tabu_liste, aspiration_crit_list = tabu_liste_suche(list_collision, liste_neighbours, tabu_liste, aspiration_crit_list, tabu_tenure)
        
        if len(tabu_liste) > tabu_tenure:
            tabu_liste.pop(0)

        #Tabu-Listen-Update: Speichern der Tupel unmittelbar vor der Kollision und der Nachbarlösung
        tabu_liste.append([[list_collision[0][2], optimale_lsg[0][list_collision[0][1]+1]], [list_collision[1][2], optimale_lsg[1][list_collision[1][1]+1]]])
        
        liste_agents.pop(list_collision[0][0])
        liste_agents.insert(list_collision[0][0], optimale_lsg[:2][0])
        liste_agents.pop(list_collision[1][0])
        liste_agents.insert(list_collision[1][0], optimale_lsg[:2][1])
 
    return i-1, liste_agents


if __name__ == "__main__":

    max_iterations = 60
    #Größen Tabuliste
    tabu_tenure = 8
    
    #Initiallösung
    #dynamisch ausbauen
    start_agent1 = (5, 0)
    end_agent1 = (5, 9)

    start_agent2 = (5, 9)
    #start_agent2 = (0, 0)
    end_agent2 = (5, 0)

    start_agent3 = (0, 5)
    end_agent3 = (9, 5)

    start_agent4 = (9, 5)
    end_agent4 = (0, 5)

    start_agent5 = (0, 2)
    end_agent5 = (9, 7)

    start_agent6 = (0, 7)
    end_agent6 = (9, 2)

    start_agent7 = (7, 0)
    end_agent7 = (4, 9)

    start_agent8 = (2, 4)
    end_agent8 = (7, 1)


    """maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]"""
    
    """maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]"""

    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    path_agent1 = astar(maze, start_agent1, end_agent1)
    path_agent2 = astar(maze, start_agent2, end_agent2)
    path_agent3 = astar(maze, start_agent3, end_agent3)
    path_agent4 = astar(maze, start_agent4, end_agent4)
    path_agent5 = astar(maze, start_agent5, end_agent5)
    path_agent6 = astar(maze, start_agent6, end_agent6)
    path_agent7 = astar(maze, start_agent7, end_agent7)
    path_agent8 = astar(maze, start_agent8, end_agent8)

    #print(path_agent1)
    #print(path_agent2)
    #print(path_agent3)
    #print(path_agent4)
    #print(path_agent5)
    #print(path_agent6)
    #print(path_agent7)
    #print(path_agent8)

    liste_agents = []
    liste_agents.append(path_agent1)
    liste_agents.append(path_agent2)
    liste_agents.append(path_agent3)
    liste_agents.append(path_agent4)
    liste_agents.append(path_agent5)
    liste_agents.append(path_agent6)
    liste_agents.append(path_agent7)
    liste_agents.append(path_agent8)
    
 
    #print(liste_agents)
    
    iterationen, liste_agents = optimization_algorithm(maze, max_iterations, tabu_tenure, liste_agents)
    
    print(liste_agents)
    
    print(iterationen)


# In[ ]:





        


# In[171]:




# In[156]:



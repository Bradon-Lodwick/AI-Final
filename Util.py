import numpy as np

#for this program this should only be run once, data will be a massive 2D array
def add_to_csv(data):

    # Puts all agent data into a list
    list_to_send = list()
    temp_list = list()
    for agent in data:
        temp_list = [agent['mode'], agent['run_no'], agent['agent'], agent['targets'], agent['steps'], agent['happiness'], agent['min'],
                     agent['max'], agent['avg'], agent['std'], agent['competitiveness']]
        list_to_send.append(temp_list)

    # takes in a 2D array of all data and write to csv file
    fmt_str = "%s," * (len(temp_list) - 1) + "%s"

    np_array = np.asarray(list_to_send)
    np.savetxt("G_24_1.csv", np_array , fmt=fmt_str)

#data is a list of 3 values, Gamemode, AvgHappiness, AvgCompetitiveness
def add_to_csv2(data):
    # Total happiness and competitiveness for each scenario given it's own list
    total_happiness = [list(), list(), list()]
    total_competitiveness = [list(), list(), list()]
    for agent in data:
        scenario_index = agent['mode']
        total_happiness[scenario_index - 1].append(agent['avg'])
        total_competitiveness[scenario_index - 1].append(agent['competitiveness'])

    # Calculate averages
    avg_happiness = [np.average(total_happiness[0]), np.average(total_happiness[1]), np.average(total_happiness[2])]
    avg_competitiveness = [np.average(total_competitiveness[0]), np.average(total_competitiveness[1]),
                           np.average(total_competitiveness[2])]

    temp_list = [1, avg_happiness[0],avg_competitiveness[0]], [2, avg_happiness[1],avg_competitiveness[1]], \
                [3, avg_happiness[2],avg_competitiveness[2]]

    fmt_str = "%s," * (len(temp_list) - 1) + "%s"

    np_array= np.array(temp_list)
    np.savetxt("G_24_2.csv", np_array, fmt=fmt_str)


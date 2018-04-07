# Introduction to Artificial Intelligence: SOFE 3720
## Term project: Design and implementation of a multi-agent system

## Setup
1. Clone the repository or download all of the files
2. To ensure that all dependencies are installed, run a pip  install with the requirements file in the venv_setup by running `pip install -r venv_setup/requirements.txt` from the root directory of the project
3. Run the Main.py file to begin the simulations

## Description
1. Environment: a 1 m x 1 m field.
2. Five agents (A,B,C,D,E) can move up and down and left and right, one centimeter in every step.
3. Assume the agents have unlimited power supply.
4. For each agent, there are five targets to collect. For example for agent A the targets are TA1 to
TA5.
5. Whenever a relevant target (for example TA3) is reachable by its related agent, the object is
considered as collected and will disappear from the field.
6. All targets and agents are randomly scattered all over the field. Agents do not have any
information about the location of none of the targets and other agents.
7. Agents have location sensor (x,y) to locate itself.
8. Agents have been given (x1,y1) and (x2,y2) so they can identify the border of the domain.
9. Agents never run out of fuel.
10. Every agent has a Radar to sense targets or other agents. The Radar can sense the type (which
agent belongs to) and locate every target or agent in 10 centimeter radius. Whenever an agent
locates a target (or an agent), it will receive the coordinates (x,y) of the target (or agent).
11. A target (or agent) is reachable by an agent if it falls into its Radar range (10cm).
12. Every agent has two communication channels: First is a public channel for broadcasting. In
broadcast mode, the message sent by an agent will be received by all other agents. Second, a
private channel to send private messages to a specific agent.
13. In both channels, agents can send any type of message but a mandatory message will be sent in
broadcast mode by an agent that collected its all targets.
14. Agents avoid colliding each other. They will never remain reachable by other agents. 
### Implement the following scenarios:
### Scenario 1: Competition
1. The game will be over as soon as one of the agents collects all its targets.
2. Only public communication channel is open for all agents. The private channels are closed.
Agents can broadcast anything including right or wrong information about the location of other
targets.
### Scenario 2: Collaboration
1. The game is not over until all agents collect their own targets.
2. Both public and private channels are open. Example of a private communication: Agent A
locates TB1. It may or may not notify the agent B the location of TB1.
### Scenario 3: Compassionate agents
1. The game will be over as soon as one of the agents collects all its targets.
2. Both public and private channels are open. Example of a private communication: Agent A
locates target TB1. It may or may not notify the agent B the location of TB1.

### Deliverables:
1. Your simulation generates a CSV file with the following columns. The name of this CSV is: G[your
group number]_1.csv
a. a= Scenario number (1,2 or 3)
b. b= Iteration number
c. c= Agent number
d. d= Number of collected targets by the agent
e. e= Number of steps taken by the agent at the end of iteration
f. Agent happiness: f=d/(e+1)
g. g= Maximum happiness in each iteration
h. h= Minimum happiness in each iteration
i. i= Average happiness in each iteration
j. j= Standard deviation of happiness in each iteration
k. Agent competitiveness: k=(f-h)/(g-h)
2. Your simulation generates another csv file from the previous CSV with the following columns.
The name of this CSV is: G[your group number]_2.csv
a. Scenario number (1,2 and 3)
b. Average of column “i” for the iterations of same scenario
c. Average of column “k” for the iterations of same scenario
3. A simple graphical interface is necessary for the simulation.
4. We expect your simulation is capable of many iterations (10 to 100 times) with random setup.
5. Deliverables: Two above mentioned CSV file in right format> since a script will read and process
the files, any other format will not be accepted and marks will be deducted. You has to send the
files before your demo via blackboard messaging.
6. You will present your simulation according to s schedule will be posted later. 

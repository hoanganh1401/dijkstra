import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pyamaze import maze, agent, COLOR

# Create title for the app
st.title("Maze Visualization with Dijkstra's Algorithm")
st.subheader("Mê cung từ file CSV và tìm đường đi ngắn nhất")

def dijkstra(m, *h, start=None):
    if start is None:
        start = (m.rows, m.cols)

    hurdles = [(i.position, i.cost) for i in h]

    unvisited = {n: float('inf') for n in m.grid}
    unvisited[start] = 0
    visited = {}
    revPath = {}
    while unvisited:
        currCell = min(unvisited, key=unvisited.get)
        visited[currCell] = unvisited[currCell]
        if currCell == m._goal:
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                if childCell in visited:
                    continue
                tempDist = unvisited[currCell] + 1
                for hurdle in hurdles:
                    if hurdle[0] == currCell:
                        tempDist += hurdle[1]

                if tempDist < unvisited[childCell]:
                    unvisited[childCell] = tempDist
                    revPath[childCell] = currCell
        unvisited.pop(currCell)

    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[revPath[cell]] = cell
        cell = revPath[cell]

    return fwdPath, visited[m._goal]

# Initialize the maze
myMaze = maze(10, 15)
myMaze.CreateMaze(1, 4, loopPercent=100)

# Create hurdles
hurdles = [agent(myMaze, 4, i, color=COLOR.red) for i in range(1, 6)]
for h in hurdles:
    h.cost = 100

# Select starting and ending points
start_options = [(i, j) for i in range(myMaze.rows) for j in range(myMaze.cols)]
start_point = st.selectbox("Select Start Point", start_options, format_func=lambda x: f"({x[0]}, {x[1]})")
end_point = st.selectbox("Select End Point", start_options, format_func=lambda x: f"({x[0]}, {x[1]})")

if st.button("Find Your Way") and start_point and end_point:
    # Set the goal for the maze
    myMaze._goal = end_point
    path, cost = dijkstra(myMaze, *hurdles, start=start_point)

    # Create a visualization using matplotlib
    plt.figure(figsize=(10, 6))
    
    # Draw the maze
    myMaze.drawMaze()  # Use the drawMaze method to visualize the maze
    
    # Highlight the path
    for cell in path:
        plt.plot(cell[1], cell[0], 'bo')  # Mark the path with blue circles
    
    plt.title(f'Total Cost: {cost}')
    plt.axis('off')  # Hide axes
    st.pyplot(plt)  # Display the plot in Streamlit
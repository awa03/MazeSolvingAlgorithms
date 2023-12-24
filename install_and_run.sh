#!/bin/bash

# Function to install Pygame
install_pygame() {
    echo "Installing Pygame..."
    pip install pygame
}

# Function to run Dijkstra's algorithm visualization
run_dijkstra() {
    python3 Dikstra.py
}

# Function to run Depth-First Search visualization
run_dfs() {
    python3 DFS.py
}

# Main script

# Install Pygame
install_pygame

# Prompt the user for visualization choice
echo "Choose visualization:"
echo "1: Dijkstra's Algorithm"
echo "2: Depth-First Search"

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo "Running Dijkstra's Algorithm Visualization..."
        run_dijkstra
        ;;
    2)
        echo "Running Depth-First Search Visualization..."
        run_dfs
        ;;
    *)
        echo "Invalid choice. Exiting..."
        ;;
esac

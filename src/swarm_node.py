import numpy as np
from typing import List, Tuple

class SwarmNode:
    def __init__(self, node_id: int, location: Tuple[float, float]):
        self.node_id = node_id
        self.location = location
        self.task_queue = []
        self.available_capacity = 100

    def add_task(self, task: dict):
        self.task_queue.append(task)
        self.available_capacity -= task['resource_requirement']

    def process_tasks(self):
        while self.task_queue:
            task = self.task_queue.pop(0)
            # Simulate processing the task
            print(f'Node {self.node_id} processing task: {task}')
            self.available_capacity += task['resource_requirement']

    def update_location(self, new_location: Tuple[float, float]):
        self.location = new_location

class AdaptiveSwarmIntelligence:
    def __init__(self, nodes: List[SwarmNode]):
        self.nodes = nodes

    def allocate_tasks(self, tasks: List[dict]):
        # Sort tasks by resource requirement in descending order
        tasks.sort(key=lambda x: x['resource_requirement'], reverse=True)

        # Allocate tasks to nodes
        for task in tasks:
            # Find the node with the most available capacity
            best_node = max(self.nodes, key=lambda x: x.available_capacity)
            if best_node.available_capacity >= task['resource_requirement']:
                best_node.add_task(task)
            else:
                # If no node has enough capacity, store the task in a queue
                print(f'Task {task} could not be allocated, added to queue.')

    def update_node_locations(self):
        # Update node locations based on some algorithm
        for node in self.nodes:
            new_location = (
                node.location[0] + np.random.uniform(-1, 1),
                node.location[1] + np.random.uniform(-1, 1)
            )
            node.update_location(new_location)

    def run(self):
        while True:
            # Receive new tasks
            new_tasks = [
                {'id': 1, 'resource_requirement': 20},
                {'id': 2, 'resource_requirement': 30},
                {'id': 3, 'resource_requirement': 40},
            ]

            self.allocate_tasks(new_tasks)

            # Process tasks on each node
            for node in self.nodes:
                node.process_tasks()

            self.update_node_locations()

if __name__ == '__main__':
    nodes = [
        SwarmNode(1, (0, 0)),
        SwarmNode(2, (10, 10)),
        SwarmNode(3, (20, 20)),
    ]

    swarm = AdaptiveSwarmIntelligence(nodes)
    swarm.run()
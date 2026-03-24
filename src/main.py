import random
import time

class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.state = 'IDLE'
        self.vote = None
        self.round = 0

    def connect(self, other_node):
        self.neighbors.append(other_node)
        other_node.neighbors.append(self)

    def start_election(self):
        self.state = 'CANDIDATE'
        self.vote = self.id
        self.round += 1
        for neighbor in self.neighbors:
            neighbor.receive_vote_request(self.id, self.round)

    def receive_vote_request(self, candidate_id, round):
        if round > self.round:
            self.round = round
            self.vote = candidate_id
            self.state = 'FOLLOWER'
            for neighbor in self.neighbors:
                neighbor.receive_vote_request(candidate_id, round)

    def receive_vote_response(self, voter_id):
        if self.state == 'CANDIDATE':
            self.vote_count += 1
            if self.vote_count > len(self.neighbors) // 2:
                self.state = 'LEADER'
                for neighbor in self.neighbors:
                    neighbor.receive_leader_notification(self.id)

    def receive_leader_notification(self, leader_id):
        self.state = 'FOLLOWER'
        self.vote = leader_id

def simulate_network():
    nodes = [Node(i) for i in range(10)]
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            nodes[i].connect(nodes[j])

    while True:
        time.sleep(random.uniform(0.5, 2))
        random.choice(nodes).start_election()

if __name__ == '__main__':
    simulate_network()
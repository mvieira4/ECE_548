import random

random.seed(25) 

# Class for default nodes
class wsn_node:  
  # Constructor for node
  def __init__(self, id: int, x: int , y: int, protocol: str = 'k'):
    self._id = id
    self._pos = (x, y)
    self._pub_key = 'Pb(0)'
    self._prv_key = f'Pv({self._id})'
    self._neighbors = {}
    self._neighbor_dists = {}
    self._connections = []
    self._recv_packs = []
    self._protocol = protocol
    
    if self._id == 0:
      self._hops = 0
      self.network = 0
    elif self._id == 1:
      self._hops = 0
      self.network = 1
    else:
      self._hops = None
      self.network = None
      
      
  def refresh(self):
    best = None
    
    while self._recv_packs:
      pack = self._recv_packs.pop().split(',')
      sndr_id = pack[0]
      sndr_hops = pack[1]
      sndr_prv_key = pack[2]
        
      if self._hops == None and sndr_hops != 'None':
        if (self._protocol == 'k' and sndr_prv_key == 'Pv(0)') or self._protocol == 'h' or int(sndr_hops) != 0:
            best = int(sndr_id)
            self._hops = int(sndr_hops) + 1
            self.network = self._neighbors[best].network
      elif sndr_hops != 'None':
        if int(sndr_hops) == 0:
          if (self._protocol == 'k' and sndr_prv_key == 'Pv(0)') or self._protocol == 'h':
            best = int(sndr_id)
            self._hops = int(sndr_hops) + 1
            self.network = self._neighbors[best].network
        elif int(sndr_hops) + 1 < self._hops and int(sndr_hops) != 0:
          best = int(sndr_id)
          self._hops = int(sndr_hops) + 1
          self.network = self._neighbors[best].network
        elif int(sndr_hops) == self._hops and best != None and int(sndr_hops) != 0:
          if self._neighbor_dists[best] > self._neighbor_dists[int(sndr_id)]:
            best = int(sndr_id)
            self._hops = int(sndr_hops) + 1
            self.network = self._neighbors[best].network
          
          
      if best != None:
        self.connections = [self.neighbors[best]]
        
    self.send_pack(list(self.neighbors.values()), self._hops)  
  
  
  def send_pack(self, targs, msg):
    for targ in targs:
      if targ._id != 0 and targ._id != 1:
        targ.append_recv_pack(f"{self._id},{msg},{self._prv_key}")
        #print(f"{self._id},{targ.id},{msg},{self._prv_key}")
    
      
  def append_recv_pack(self, new_pack):
    self._recv_packs.append(new_pack)
    
    
  @property
  def network(self):
    return self._network
  
  @network.setter
  def network(self, new_network):
    self._network = new_network
    
  @property
  def id(self):
    return self._id
  
  @property
  def pos(self):
    return self._pos
  
  @pos.setter
  def pos(self, new_pos):
    self._pos = new_pos
  
  @property
  def role(self):
    return self._role
  
  @role.setter
  def role(self, new_role):
    self._role = new_role 
  
  @property
  def neighbors(self):
    return self._neighbors
  
  @property
  def neighbor_dists(self):
    return self._neighbor_dists
  
  @property
  def connections(self):
    return self._connections
  
  @connections.setter
  def connections(self, new_connections):
    self._connections = new_connections
    
  @connections.deleter
  def connection(self):
    self.connections = []
    
  @property
  def hops(self):
    return self.hops
  
  @hops.setter
  def hops(self, new_hops):
    self._hops = new_hops
  
  @property
  def recv_packs(self):
    return self._recv_packs
  


# Contains all properties of wsn and interation of nodes
class wsn:
  # Needs to keep track of nodes
  # Should keep track of connections between nodes
  # Should be able to tell which nodes are in range for communication
  # Allow for connection between nodes 
  # Should have way to output elements
  # Constuctor for the wsn
  def __init__(self, base_num: int = 1, mal_num: int = 1, node_range: float = 1.5):
      self._base_num = base_num 
      self._mal_num = mal_num
      self._node_range = node_range
      self.nodes = {}
      self._next_id = 0
      self.max_nodes = 225

      # Create list of avaiable locations
      self._free_locs = []
      for i in range(15):
        for j in range(15):
          self._free_locs.append((i,j))
      
    
  def _add_node(self):
    # Get random location and find distances
    x, y = self._free_locs.pop(random.randint(0, len(self._free_locs) - 1))
    
    # Create node with generated info
    self.nodes[self._next_id] = wsn_node(self._next_id, x, y)
    
    # Increments id number
    self._next_id += 1
    
    
  def add_nodes(self, num):
    for i in range(num):
      self._add_node()
      
      
  def _set_neighbors(self):
    node_queue = list(self.nodes.values())
    
    while node_queue:
      current = node_queue.pop(0)
      
      for node in node_queue:
        current_x, current_y = current.pos
        node_x, node_y = node.pos
        dist = ((current_x - node_x) ** 2 + (current_y - node_y) ** 2) ** 0.5
        
        if dist <= self._node_range:
          node._neighbors[current.id] = current
          node._neighbor_dists[current.id] = dist
          
          current._neighbors[node.id] = node
          current._neighbor_dists[node.id] = dist
          
  def run(self):
    for i in range(8): 
      for node in self.nodes.values():
        node.refresh()
        
        
    # for node in self.nodes.values():
    #   print(f'id: {node.id}')
    #   print(f'role: {node.role}')
    #   if node.connected != None:
    #     print(f'connected: {node.connected.id}')
    #   else:
    #     print(f'connected: {node.connected}')
    #   print('neighbors:')
    #   for neighbor in node.neighbors:
    #     print(f'\t id: {neighbor.id} role: {neighbor.role} hops: {neighbor.hops}')
          
      
  def gen_elements(self):
    elements = []
    for node in self.nodes.values():
      node_x, node_y = node._pos
      role = 2
      
      if node.id == 0 or node.id ==1:
        role = node.id
      else:
        role = 2
        
      elements.append({'data': {'id': str(node._id), 'label': str(node._hops), 'network': node.network, 'role': role}, 'position': {'x': node_x * 100, 'y': node_y * 50},'locked': True})
      
    for node in self.nodes.values():
      if node.connections != []:
        for connection in node.connections:
          elements.append({'data': {'source': str(node.id), 'target': str(connection.id)}})
        
    return elements
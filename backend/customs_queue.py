class Shipment:
    def __init__(self, shipment_id, origin, destination, goods_type, base_priority):
        self.shipment_id = shipment_id
        self.origin = origin
        self.destination = destination
        self.goods_type = goods_type
        
        # Calculate final priority (Higher number = higher priority)
        # We boost priority for certain goods like medical supplies or perishables
        self.priority = base_priority
        if self.goods_type.lower() in ['medical', 'perishable']:
            self.priority += 50
        elif self.goods_type.lower() == 'hazardous':
            self.priority += 20
            
    def __repr__(self):
        return f"Shipment({self.shipment_id}, {self.goods_type}, Priority: {self.priority})"


class CustomsPriorityQueue:
    """
    A Max-Binary Heap implementation for the Customs Clearance Queue.
    Shipments with higher priority values are processed first.
    """
    def __init__(self):
        self.heap = []
        
    def _parent(self, index):
        return (index - 1) // 2
        
    def _left_child(self, index):
        return 2 * index + 1
        
    def _right_child(self, index):
        return 2 * index + 2
        
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        
    def insert(self, shipment):
        """Inserts a new shipment into the priority queue."""
        self.heap.append(shipment)
        self._heapify_up(len(self.heap) - 1)
        print(f"[ARRIVAL] {shipment} entered customs.")
        
    def _heapify_up(self, index):
        """Restores max-heap property by bubbling up."""
        parent_idx = self._parent(index)
        if index > 0 and self.heap[index].priority > self.heap[parent_idx].priority:
            self._swap(index, parent_idx)
            self._heapify_up(parent_idx)
            
    def extract_max(self):
        """Removes and returns the shipment with the highest priority for processing."""
        if not self.heap:
            print("[QUEUE EMPTY] No shipments waiting for clearance.")
            return None
            
        if len(self.heap) == 1:
            return self.heap.pop()
            
        # Swap root with last element, remove the max, and bubble down the new root
        max_shipment = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        print(f"[CLEARED] {max_shipment} has been processed and cleared.")
        return max_shipment
        
    def _heapify_down(self, index):
        """Restores max-heap property by bubbling down."""
        largest = index
        left = self._left_child(index)
        right = self._right_child(index)
        
        # Check if left child exists and is greater than current largest
        if left < len(self.heap) and self.heap[left].priority > self.heap[largest].priority:
            largest = left
            
        # Check if right child exists and is greater than current largest
        if right < len(self.heap) and self.heap[right].priority > self.heap[largest].priority:
            largest = right
            
        # If largest is not the current node, swap and continue bubbling down
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)
            
    def peek(self):
        """Returns the highest priority shipment without removing it."""
        if self.heap:
            return self.heap[0]
        return None
        
    def is_empty(self):
        return len(self.heap) == 0


# --- Demonstration of the Unit 1 Algorithm ---
if __name__ == "__main__":
    print("=== Smart International Trade Facilitation ===")
    print("--- Customs Priority Queue Subsystem ---\\n")
    
    queue = CustomsPriorityQueue()
    
    # Simulating arriving containers
    queue.insert(Shipment("CONT-001", "Shanghai", "Rotterdam", "Electronics", base_priority=10))
    queue.insert(Shipment("CONT-002", "New York", "Rotterdam", "Furniture", base_priority=5))
    queue.insert(Shipment("CONT-003", "Mumbai", "Rotterdam", "Medical", base_priority=15)) # Boosted!
    queue.insert(Shipment("CONT-004", "Dubai", "Rotterdam", "Perishable", base_priority=10)) # Boosted!
    queue.insert(Shipment("CONT-005", "Tokyo", "Rotterdam", "Automotive Parts", base_priority=30))
    
    print("\\n--- Commencing Customs Clearance Processing ---")
    while not queue.is_empty():
        cleared_item = queue.extract_max()

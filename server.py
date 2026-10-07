import http.server
import socketserver
import json
import heapq
import time
from urllib.parse import urlparse, parse_qs

PORT = 8000

# ==========================================
# Unit 1: Priority Queue (Max-Heap)
# ==========================================
class MaxHeapObj:
    def __init__(self, item, priority):
        self.item = item
        self.priority = priority
    def __lt__(self, other):
        return self.priority > other.priority # inverted for max-heap via heapq

customs_queue = []
heapq.heappush(customs_queue, MaxHeapObj({"id": "CONT-101", "type": "Electronics"}, 10))
heapq.heappush(customs_queue, MaxHeapObj({"id": "CONT-102", "type": "Medical"}, 80))
heapq.heappush(customs_queue, MaxHeapObj({"id": "CONT-103", "type": "Furniture"}, 5))
heapq.heappush(customs_queue, MaxHeapObj({"id": "CONT-104", "type": "Perishable"}, 60))

# ==========================================
# Unit 2: Graphs (Dijkstra)
# ==========================================
GRAPH = {
    'Shanghai': {'Singapore': 5, 'Tokyo': 3},
    'Tokyo': {'Shanghai': 3, 'Los Angeles': 12},
    'Singapore': {'Shanghai': 5, 'Rotterdam': 15, 'Dubai': 7},
    'Dubai': {'Singapore': 7, 'Rotterdam': 6},
    'Los Angeles': {'Tokyo': 12, 'Rotterdam': 18},
    'Rotterdam': {'Singapore': 15, 'Dubai': 6, 'Los Angeles': 18}
}

def dijkstra(start, end):
    distances = {node: float('inf') for node in GRAPH}
    distances[start] = 0
    prev = {node: None for node in GRAPH}
    unvisited = set(GRAPH.keys())
    
    while unvisited:
        curr = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(curr)
        if curr == end: break
        for neighbor, weight in GRAPH[curr].items():
            alt = distances[curr] + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                prev[neighbor] = curr
                
    path = []
    curr = end
    while curr:
        path.insert(0, curr)
        curr = prev[curr]
    return {"path": path, "time": distances[end]}

# ==========================================
# Unit 3: Dynamic Programming (0/1 Knapsack)
# ==========================================
ITEMS = [
    {"name": "Machinery", "weight": 10, "value": 50000},
    {"name": "Electronics", "weight": 5, "value": 40000},
    {"name": "Chemicals", "weight": 8, "value": 35000},
    {"name": "Textiles", "weight": 4, "value": 20000},
    {"name": "Auto Parts", "weight": 7, "value": 25000}
]

def optimize_load(capacity):
    n = len(ITEMS)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if ITEMS[i-1]["weight"] <= w:
                dp[i][w] = max(ITEMS[i-1]["value"] + dp[i-1][w - ITEMS[i-1]["weight"]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    
    w = capacity
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(ITEMS[i-1])
            w -= ITEMS[i-1]["weight"]
    return {"profit": dp[n][capacity], "items": selected}

# ==========================================
# Unit 4: Graph Coloring (Backtracking)
# ==========================================
MATERIALS = ["Explosives", "Flammable Gases", "Toxic Chemicals", "Oxidizers", "Corrosives"]
CONFLICTS = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0],
    [0, 1, 0, 0, 1],
    [1, 1, 0, 0, 1],
    [0, 0, 1, 1, 0]
]

def is_safe(v, color_arr, c):
    for i in range(len(MATERIALS)):
        if CONFLICTS[v][i] == 1 and color_arr[i] == c:
            return False
    return True

def graph_coloring_util(m, color_arr, v):
    if v == len(MATERIALS): return True
    for c in range(1, m + 1):
        if is_safe(v, color_arr, c):
            color_arr[v] = c
            if graph_coloring_util(m, color_arr, v + 1): return True
            color_arr[v] = 0
    return False

def allocate_storage():
    for m in range(1, len(MATERIALS) + 1):
        color_arr = [0] * len(MATERIALS)
        if graph_coloring_util(m, color_arr, 0):
            zones = {}
            for i, c in enumerate(color_arr):
                zone = f"Zone {chr(64+c)}" # Zone A, Zone B...
                if zone not in zones: zones[zone] = []
                zones[zone].append(MATERIALS[i])
            return {"zones_needed": m, "allocation": zones}
    return None

# ==========================================
# Server Handler
# ==========================================
class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        
        if parsed_path.path == '/api/customs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if customs_queue:
                cleared = heapq.heappop(customs_queue)
                response = {"status": "cleared", "shipment": cleared.item, "priority": cleared.priority}
            else:
                response = {"status": "empty"}
            self.wfile.write(json.dumps(response).encode())
            return
            
        elif parsed_path.path == '/api/customs/add':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            s_id = query.get('id', ['UNKNOWN'])[0]
            s_type = query.get('type', ['General'])[0]
            
            base_prio = 10
            if s_type == 'Medical': base_prio = 80
            elif s_type == 'Perishable': base_prio = 60
            elif s_type == 'Electronics': base_prio = 30
            
            heapq.heappush(customs_queue, MaxHeapObj({"id": s_id, "type": s_type}, base_prio))
            self.wfile.write(json.dumps({"status": "added", "id": s_id}).encode())
            return
            
        elif parsed_path.path == '/api/route':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            start = query.get('start', ['Shanghai'])[0]
            end = query.get('end', ['Rotterdam'])[0]
            
            # Simple check if valid
            if start not in GRAPH or end not in GRAPH:
                self.wfile.write(json.dumps({"path": [], "time": "Invalid route"}).encode())
                return
                
            route = dijkstra(start, end)
            self.wfile.write(json.dumps(route).encode())
            return
            
        elif parsed_path.path == '/api/optimize':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            cap_str = query.get('capacity', ['20'])[0]
            try: capacity = int(cap_str)
            except: capacity = 20
            
            load = optimize_load(capacity)
            self.wfile.write(json.dumps(load).encode())
            return
            
        elif parsed_path.path == '/api/storage':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            allocation = allocate_storage()
            self.wfile.write(json.dumps(allocation).encode())
            return
            
        return super().do_GET()

with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
    print(f"Serving UI and API at http://localhost:{PORT}")
    httpd.serve_forever()

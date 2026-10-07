# How the System Works

This project is separated into a clean Client-Server architecture, ensuring that the heavy algorithmic lifting is done on the backend.

## 1. The Backend (`server.py`)
The backend is written entirely in standard Python without external frameworks like Flask or Django. It utilizes the built-in `http.server` module to serve both static files and dynamic REST API endpoints.

### API Endpoints:
* `GET /api/route?start={origin}&end={destination}`: 
  Parses the query parameters, runs **Dijkstra's Algorithm** over the predefined port graph, and returns a JSON object containing the optimal path list and total transit time.
* `GET /api/optimize?capacity={tons}`:
  Runs the **0/1 Knapsack** DP algorithm to find the subset of cargo pallets that maximizes value without exceeding the specified `capacity`. Returns the items and total profit.
* `GET /api/customs/add?id={id}&type={type}`:
  Calculates a priority score based on the goods `type` and inserts it into a Python `heapq` (Binary Max-Heap).
* `GET /api/customs`:
  Pops and returns the highest priority shipment from the Max-Heap.
* `GET /api/storage`:
  Runs the **Graph Coloring (Backtracking)** algorithm on a predefined conflict matrix of hazardous materials and returns the optimal zone allocations.

## 2. The Frontend (`index.html`, `style.css`, `app.js`)
* **Styling**: The UI uses a modern "Glassmorphism" aesthetic with a massive container ship background. Dark themes, yellow accents, and CSS blur effects create a premium, production-ready feel.
* **Logic**: `app.js` listens to button clicks, reads values from the UI input elements (like dropdowns and number inputs), and asynchronously `fetch()`es data from the Python API. It then seamlessly injects the returned JSON data into the DOM, triggering CSS keyframe animations to reveal the results.

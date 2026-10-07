# Research & Theoretical Notes

## 1. Dijkstra's Algorithm in Logistics
**Topic**: Graphs (Unit 2)
Dijkstra's algorithm is a greedy algorithm used to find the shortest paths between nodes in a graph. In the context of maritime shipping, ports are nodes and shipping lanes are edges weighted by transit time (or fuel cost). 
* **Time Complexity**: $O(V^2)$ using an array, or $O(E + V \log V)$ using a Min-Priority Queue.
* **Why not Bellman-Ford?**: Since transit times cannot be negative, Dijkstra's is significantly faster and more appropriate for logistics graphs.

## 2. 0/1 Knapsack Problem for Container Packing
**Topic**: Dynamic Programming (Unit 3)
The 0/1 Knapsack problem is a combinatorial optimization problem. A shipping container has a fixed maximum weight limit $W$. We have $n$ pallets, each with a weight $w_i$ and a profit value $v_i$. 
* **Constraint**: We can either take an item completely or leave it (0/1 property).
* **State Equation**: $DP[i][w] = \max(v_i + DP[i-1][w - w_i], DP[i-1][w])$
* **Time Complexity**: $O(n \times W)$, where $n$ is the number of items and $W$ is the container capacity. This pseudo-polynomial time complexity is highly efficient for typical cargo capacities.

## 3. Priority Queues for Customs Clearance
**Topic**: Trees & Heaps (Unit 1)
A Priority Queue is an abstract data type where each element has a priority, and elements with higher priority are served before others. A Binary Max-Heap is a complete binary tree where the value of each node is greater than or equal to its children.
* **Insertion**: $O(\log N)$ - Add to bottom and "bubble up".
* **Extraction (Max)**: $O(\log N)$ - Remove root, swap with last element, and "bubble down".
* **Application**: Medical and perishable goods mathematically bypass regular goods, modeling real-world "Fast Lane" customs procedures.

## 4. Graph Coloring for Hazardous Materials
**Topic**: Backtracking (Unit 4)
Graph coloring involves assigning colors to certain elements of a graph subject to certain constraints. In logistics, no two adjacent vertices (conflicting hazardous materials) can share the same color (storage zone).
* **Algorithm**: Backtracking explores all potential color assignments and abandons a path (pruning) as soon as it determines the current assignment violates a safety conflict.
* **Time Complexity**: $O(m^V)$, where $m$ is the number of available zones and $V$ is the number of hazardous materials. While exponential, the number of dangerous goods classes (e.g., IMDG classes) is small (9 primary classes), making Backtracking perfectly viable.

## 5. References & Sources
To build the theoretical and practical foundations of this system, the following academic and engineering sources were utilized:

1. **Dijkstra's Routing**: 
   - Dijkstra, E. W. (1959). *"A Note on Two Problems in Connexion with Graphs"*. Numerische Mathematik. [Link to Paper](https://dl.acm.org/doi/10.1145/321156.321161)
   - GeeksForGeeks: [Dijkstra’s shortest path algorithm](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)
2. **Dynamic Programming (0/1 Knapsack)**:
   - Bellman, R. (1957). *"Dynamic Programming"*. Princeton University Press.
   - Introduction to Algorithms (CLRS) - Chapter 15: Dynamic Programming. [MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
3. **Binary Heaps & Priority Queues**:
   - Williams, J. W. J. (1964). *"Algorithm 232 - Heapsort"*. Communications of the ACM.
   - Python `heapq` standard library documentation: [docs.python.org/3/library/heapq.html](https://docs.python.org/3/library/heapq.html)
4. **Graph Coloring & Backtracking**:
   - International Maritime Dangerous Goods (IMDG) Code segregation tables (Real-world constraints used for mapping conflicts). [IMO IMDG Code](https://www.imo.org/en/OurWork/Safety/Pages/DangerousGoods.aspx)
   - Backtracking Algorithms: [Stanford CS Library](http://cslibrary.stanford.edu/114/)
5. **UI / Design Architecture**:
   - "Glassmorphism in UI Design" via CSS-Tricks: [css-tricks.com](https://css-tricks.com/glassmorphism-in-css/)
   - `http.server` — HTTP servers implementation in Python: [docs.python.org](https://docs.python.org/3/library/http.server.html)

class DigitsSolver:
    def __init__(self, target, nums):
        self.target = target
        self.root_node = self.Node(self, nums)
        self.degree = len(nums)
        self.nodes = {}
        self.vertices = []
        self.nodes[self.root_node.key] = self.root_node
        self.has_solution = False

    def solve(self, quit_early=False):
        for i in range(0, self.degree):
            keys = list(self.nodes.keys())
            for k in keys:
                self.nodes[k].spawn()
            if self.has_solution and quit_early:
                break
    
    def print_solutions(self, debug=False):
        output = [ '%d <--- [%s]' % (self.target, self.root_node.key) ]
        if debug:
            for k in self.nodes:
                output.append(str(self.nodes[k]))
        if self.has_solution:
            output.append('[%s] --->' % (self.root_node.key))
            solution_count = 0
            for k in self.nodes:
                if self.nodes[k].is_solution:
                    leftovers = self.nodes[k].leftovers
                    solution_output = []
                    iter_key = k
                    while k != self.root_node.key:
                        op = list(self.nodes[k].parent_vertices.keys())[0]
                        k = self.nodes[k].parent_vertices[op]["from"]
                        solution_output.append(op)
                    solution_output.reverse()
                    ops = ", ".join(solution_output)
                    leftoverstr = " WITH %s LEFT OVER" % (str(leftovers))
                    output.append("  %s ---> %d%s" % (ops, self.target, leftoverstr if len(leftovers) else ""))
                    solution_count += 1 
            output.append("%d SOLUTIONS" % solution_count)
        else:
            output.append("NO SOLUTION")
        return "\n".join(output)


    def __repr__(self):
        return self.print_solutions()

    def solutions(self):
        return [v for v in self.nodes if self.nodes[v].is_solution]
        #return self.nodes[lambda x: x.is_solution]
    
#    def test_add_node(self, parent, op, child):
#        if child.key in self.nodes:
#            self.nodes[node.key].child_vertices.append
#            return False
#        self.nodes[node.key] = node
#        return True
    
    class Node:
        def __init__(self, ds, nums):
            self.ds = ds
            self.nums = sorted(nums)
            self.ops = []
            is_solution = False
            self.leftovers = []
            for num in self.nums:
                if num == ds.target:
                    leftovers = nums.copy()
                    leftovers.remove(ds.target)
                    is_solution = True
                    for leftover in leftovers:
                        if not leftover in ds.root_node.nums:
                            is_solution = False
                    if is_solution:
                        ds.has_solution = True
                        self.leftovers = leftovers
            self.is_solution = is_solution
            self.key = ", ".join([str(x) for x in nums])
            self.child_vertices = {}
            self.parent_vertices = {}

        def spawn(self):
            def try_create_node(self, i1, i2, op):
                new_nums = self.nums.copy()
                n1 = self.nums[i2]
                n2 = self.nums[i1]
                res = 0
                if op == "+":
                    res = n1 + n2
                if op == "-":
                    res = n1 - n2
                if op == "x":
                    res = n1 * n2
                if op == "/" and not n1 % n2:
                    res = n1 // n2
                if res:
                    op = "%d %s %d = %d" % (n1, op, n2, res)
                    new_nums.remove(n1)
                    new_nums.remove(n2)
                    new_nums.append(res)
                    new_nums.sort()
                    new_node = self.ds.Node(self.ds, new_nums)
                    new_vertex = {
                        "from": self.key,
                        "to": new_node.key,
                        "op": op
                    }
                    self.ds.vertices.append(new_vertex)
                    self.child_vertices[op] = new_vertex
                    if new_node.key not in self.ds.nodes:
                        self.ds.nodes[new_node.key] = new_node
                    self.ds.nodes[new_node.key].parent_vertices[op] = new_vertex
            
            for i1 in range(0, len(self.nums)-1):
                for i2 in range(1, len(self.nums)):
                    if i1 < i2:
                        try_create_node(self, i1, i2, "+")
                        try_create_node(self, i1, i2, "-")
                        try_create_node(self, i1, i2, "x")
                        try_create_node(self, i1, i2, "/")

        def __repr__(self):
            output = [ "%s%s" % (str(self.nums), " -> " if len(self.child_vertices) else "") ]
            for k in self.child_vertices:
                child_key = self.child_vertices[k]["to"]
                output.append("  %s -> [%s]%s" % (k, child_key, " SOLUTION!!!" if self.ds.nodes[child_key].is_solution else ""))
            return "\n".join(output)
        


def solve_digits(target, digits, quit_early=False):
    ds = DigitsSolver(target, digits)
    ds.solve(quit_early)
    print(ds.print_solutions())

solve_digits(495, [3,5,7,13,20,25])
#solve_digits(118, [2,3,5,7,9,15])
#solve_digits(273, [5,6,7,8,11,20])
#solve_digits(335, [4,7,8,9,11,20])
#solve_digits(463, [9,11,13,19,20,25])



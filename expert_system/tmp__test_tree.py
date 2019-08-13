class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)

def print_tree_inorder(tree):
    if tree is None:
        return
    print_tree_inorder(tree.left)
    print(tree.cargo, end=" ")
    print_tree_inorder(tree.right)

# EXAMPLE: A | B + C => D
tree = Tree("=>", Tree('D'), Tree("|", Tree('A'), Tree('+', Tree('B'), Tree('C'))))

print_tree_inorder(tree)
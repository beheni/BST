"""
File: linkedbst.py
Author: Ken Lambert
"""
import tqdm
from sys import setrecursionlimit
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from random import choice, shuffle
from time import time

setrecursionlimit(10**6)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return list(iter(self))

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()
        nodes = LinkedStack()

        node = self._root
        while not nodes.isEmpty() or node is not None:
            if node is not None:
                nodes.push(node)
                node = node.left
            else:
                node = nodes.pop()
                lyst.append(node.data)
                # print(len(lyst))
                node = node.right

        return list(iter(lyst))

    def find_object(self, item):
        """Finds an item in a list and returns object"""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node)
                recurse(node.right)

        recurse(self._root)
        for elem in lyst:
            if elem.data == item:
                return elem

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)
        recurse(self._root)
        return list(iter(lyst))

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def find_iterative(self, item):
        root = self._root
        while root != None:
            if item > root.data:
                root = root.right
            elif item < root.data:
                root = root.left
            else:
                return root.data
        return False

    # Mutator methods

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def is_leaf(self, node):
        """Checks is the node is leaf"""
        if node.left or node.right:
            return False
        return True

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            if top.left is None and top.right is None:
                return 0
            left_sum = height1(top.left) if top.left is not None else -1
            right_sum = height1(top.right) if top.right is not None else -1
            return max(left_sum, right_sum)+1
        return height1(self._root)

    def num_nodes(self):
        """Num nodes"""
        return len(self.preorder())

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return: bool
        '''
        return self.height() < 2 * log(self.num_nodes() + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        traverse = self.inorder()
        return [i for i in traverse if i >= low and i <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recursive(elements):
            if len(elements) == 0:
                return None
            mid = len(elements)//2
            node = BSTNode(elements[mid])
            node.left = recursive(elements[:mid])
            node.right = recursive(elements[mid+1::])
            return node
        self._root = recursive(self.inorder())

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder():
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder()[::-1]:
            if elem < item:
                return elem
        return None

    def add_iter(self, item):
        #  Create a new node
        node = BSTNode(item)
        if (self._root == None):
            #  When adds a first node in bst
            self._root = node
        else:
            find = self._root
            #  Add new node to proper position
            while (find != None):
                if (find.data >= item):
                    if (find.left == None):
                        #  When left child empty
                        #  So add new node here
                        find.left = node
                        return
                    else:
                        #  Otherwise
                        #  Visit left sub-tree
                        find = find.left

                else:
                    if (find.right == None):
                        #  When right child empty
                        #  So add new node here
                        find.right = node
                        return
                    else:
                        #  Visit right sub-tree
                        find = find.right
        self._size += 1

    def add_recursive(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    @staticmethod
    def demo_bst(path):
        """
            Demonstration of efficiency binary search tree for the search tasks.
            :param path:
            :type path:
            :return:
            :rtype:
            """
        ITERATIONS = 10000
        with open(path, "r") as file:
            lst_words = []
            for word in file:
                lst_words.append(word.strip())
        print("Time searching in a list:")

        tm1 = time()
        for i in tqdm.tqdm(range(ITERATIONS)):
            random_item = choice(lst_words)
            lst_words.index(random_item)
        tm2 = time()
        print(tm2-tm1)
        print("")

        tree_not_random_add = LinkedBST(lst_words)
        print("Time searching in a not balanced binary tree with sequentially added nodes:")
        tm3 = time()
        for i in tqdm.tqdm(range(ITERATIONS)):
            random_item = choice(lst_words)
            tree_not_random_add.find_iterative(random_item)
        tm4 = time()
        print(tm4-tm3)
        print("")

        shuffle(lst_words)
        tree_random_add = LinkedBST(lst_words)
        print("Time searching in a not balanced binary tree with randomly added nodes:")
        tm5 = time()
        for i in tqdm.tqdm(range(ITERATIONS)):
            random_item = choice(lst_words)
            tree_random_add.find_iterative(random_item)
        tm6 = time()
        print(tm6-tm5)
        print("")

        tree_random_add.rebalance()
        print("Time searching in a balanced binary tree:")
        tm7 = time()
        for i in tqdm.tqdm(range(ITERATIONS)):
            random_item = choice(lst_words)
            tree_random_add.find_iterative(random_item)
        tm8 = time()
        print(tm8-tm7)
        print("")


LinkedBST.demo_bst("test.txt")

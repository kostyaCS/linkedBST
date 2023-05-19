"""
File: linkedbst.py
Author: Ken Lambert
"""
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
import time

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
            str_ = ""
            if node != None:
                str_ += recurse(node.right, level + 1)
                str_ += "| " * level
                str_ += str(node.data) + "\n"
                str_ += recurse(node.left, level + 1)
            return str_

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
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        current = self._root
        while current is not None:
            if item == current.data:
                return current
            elif item < current.data:
                current = current.left
            else:
                current = current.right
        return None

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        node = BSTNode(item)

        if self.isEmpty():
            self._root = node
            self._size += 1
            return

        current_tree = self._root

        while True:
            if item < current_tree.data:
                if current_tree.left is None:
                    current_tree.left = node
                    self._size += 1
                    return
                else:
                    current_tree = current_tree.left
            else:
                if current_tree.right is None:
                    current_tree.right = node
                    self._size += 1
                    return
                else:
                    current_tree = current_tree.right

        # # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left == None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right == None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_MaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_Node = top.left
            while not current_Node.right == None:
                parent = current_Node
                current_Node = current_Node.right
            top.data = current_Node.data
            if parent == top:
                top.left = current_Node.left
            else:
                parent.right = current_Node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
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
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_MaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_Child = current_node.right

                # Case 3: The node has no right child
            else:
                new_Child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_Child
            else:
                parent.right = new_Child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return item_removed

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def get_children(self, node):
        """
        This method gets node's children.
        """
        if node.left is not None:
            yield node.left
        if node.right is not None:
            yield node.right

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        root = self._root

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None or (top.right is None and top.left is None):
                return 0
            return 1 + max(height1(child) for child in self.get_children(top))
        return height1(root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < (2 * log(self._size + 1) - 1)

    def symmetric_traversal(self):
        """This method represent a symmetric traversal"""
        list_of_linkedbst = []

        def recurse(node):
            if node is not None:
                if node.left is not None:
                    recurse(node.left)
                list_of_linkedbst.append(node.data)
                if node.right is not None:
                    recurse(node.right)
        recurse(self._root)
        return list_of_linkedbst

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [x for x in self.inorder() if low <= x <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        list_ = self.symmetric_traversal()
        self._root = None
        def build_balanced_tree(start, end):
            if start > end:
                return None
            middle = (start + end) // 2
            node = BSTNode(list_[middle])
            node.left = build_balanced_tree(start, middle - 1)
            node.right = build_balanced_tree(middle + 1, end)
            return node
        self._root = build_balanced_tree(0, len(list_) - 1)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result_list = self.inorder()
        min_greater = float('inf')
        for num in result_list:
            if num > item and num < min_greater:
                min_greater = num
        return min_greater if min_greater != float('inf') else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result_list = self.inorder()
        max_smaller = 0
        for num in result_list:
            if num < item and num > max_smaller:
                max_smaller = num
        return max_smaller if max_smaller != 0 else None

    def demo_bst(self, path: str):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # перший спосіб
        with open(path, mode='r', encoding='utf-8') as file_dict:
            res = [x.strip() for x in file_dict.readlines()[:50000]]
            random_words = [random.choice(res) for _ in range(10000)]
            indexes = []
            start_time_list = time.time()
            for i in random_words:
                indexes.append(res.index(i))
            end_time_list = time.time()
            result_of_1 = end_time_list - start_time_list
            print(f'Time when we search for 10000 words in list: {result_of_1} s')

        #другий спосіб
        with open(path, mode='r', encoding='utf-8') as file_dict:
            tree = self
            res = [x.strip() for x in file_dict.readlines()[:50000]]
            for i in res:
                tree.add(i)
            random_words = [random.choice(res) for _ in range(10000)]
            start_time_list = time.time()
            for i in random_words:
                tree.find(i)
            end_time_list = time.time()
            result_of_2 = end_time_list - start_time_list
            print(f'Time for searching 10000 words in a binary tree search\
 with 50000 elements: {result_of_2} s')

        # третій спосіб
        with open(path, mode='r', encoding='utf-8') as file_dict:
            tree = self
            res = random.sample(file_dict.readlines(), 10000)
            linked_tree = LinkedBST(res)
            start_time_list = time.time()
            for i in res:
                linked_tree.find(i)
            end_time_list = time.time()
            result_of_3 = end_time_list - start_time_list
            print(f'Time for searching 10000 words in a binary tree search\
 that added random: {result_of_3} s')

        # четвертий спосіб
            linked_tree.rebalance()
            start_time_list = time.time()
            for i in res:
                linked_tree.find(i)
            end_time_list = time.time()
            result_of_4 = end_time_list - start_time_list
            print(f'Time for searching 10000 words in a binary tree search\
 that added random, but already balanced: {result_of_4} s')


a = LinkedBST()
print(a.demo_bst('words.txt'))

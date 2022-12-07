#!/usr/bin/env python3
# https://adventofcode.com/2022/day/7

import os


# class for managing our directory tree
class Directory:
    def __init__(self, name):
        self.name     = name
        self.size     = 0
        self.children = []
        self.files    = []

    def get_all_size(self):
        if self.children is None:
            return self.size
        else:
            total_size = self.size
            for child in self.children:
                total_size += child.get_all_size()
            return total_size

    def add_file(self, name, size):
        self.files.append({name: size})
        self.size += size

    def add_children(self, child):
        self.children.append(child)


# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# disk metadata
disk_size = 70000000
needed_space = 30000000

# tracking our structure and state
tree = {
    '/': Directory('/')
}
cwd   = []

# process the commands
for line in lines:
    # noop for ls instructions
    if "$ ls" in line:
        continue

    # track directory changes
    if "$ cd" in line:
        target = line.split(' ')[-1]
        if target == '/':
            cwd = []
        elif target == '..':
            cwd.pop()
        else:
            cwd.append(target)
        continue

    # split the output of ls command
    ls_out = line.split(' ')

    # handle subdirectories
    if ls_out[0] == 'dir':
        # grab the subdir name
        dir_name = ls_out[1]

        # derive full path string for cwd
        parent_path = '/' + '/'.join(cwd)

        # derive full path string for subdir
        subdir = cwd.copy()
        subdir.append(dir_name)
        subdir_path = '/' + '/'.join(subdir)

        # add as a child to parent dir
        tree[subdir_path] = Directory(subdir_path)
        tree[parent_path].add_children(tree[subdir_path])

        continue

    # handle files
    size = int(ls_out[0])
    file = ls_out[1]
    path = '/' + '/'.join(cwd)

    tree[path].add_file(file, size)

# sum up folders less than 100000
total = 0
for dir, data in tree.items():
    size = data.get_all_size()
    if size <= 100000:
        total += size
print('part 1:', total)

# determine free spack
free_space = disk_size - tree['/'].get_all_size()

# determine space needed
to_delete = needed_space - free_space

# build a dir: size array
dir_sizes = [[dir, data.get_all_size()] for dir, data in tree.items()]

# sort by smallest to largest
dir_sizes.sort(key=lambda s: (s[1]))

# find the smallest dir we can delete to reach our target free space
for dir in dir_sizes:
    if dir[1] >= to_delete:
        print('part 2:', dir[1])
        break

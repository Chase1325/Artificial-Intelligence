import sys
import re
from copy import deepcopy

class Variable:

	def __init__(self, list_args):
		self.name = list_args[0]
		self.args = list_args[1:]

	def __repr__(self):
		return "Variable({0},{1})".format(self.name, self.args)

	def assignedTo(self, assignment):
		isAssigned = False
		for assignedVariable in assignment:
			if assignedVariable[0] == self:
				isAssigned = assignedVariable[1]
				break
		return isAssigned


class Value:

	def __init__(self, n):
		self.name = n
		self.arguments = []

	def __repr__(self):
		string = "Value({0}".format(self.name)
		for argument in self.arguments:
			string += ", {0}".format(argument)
		return string + ")"


class Constraint:

	# types of constraints:
	#	0: deadline, universal
	#	11: Unary inclusive --- the task can only be assigned this subset of the domain
	#	12: Unary exclusive --- the task cannot be assigned this subset of the domain
	#	21: Binary equals --- the tasks need to be assigned the same value
	#	22: Binary not equals --- the tasks cannot be assigned the same value
	#	23: Binary not simultaneous --- the tasks cannot be assigned simultaneously the two values

	# Cosntraint is only called in Graph initialization method. The variables and the values are already created

	def __init__(self, graph, type_of_constraint, list_variables = [], list_values = []):
		self.type = type_of_constraint
		self.variables = list_variables

		if self.type == 0:
			self.values = list_values
			return

		if self.type == 11:
			self.values = [0]*len(graph.values)
			for val_index, possible_val in enumerate(graph.values):
				for constraint_val in list_values:
					if possible_val == constraint_val:
						self.values[val_index] = 1

		elif self.type == 12:
			self.values = [1]*len(graph.values)
			for val_index, possible_val in enumerate(graph.values):
				for constraint_val in list_values:
					if possible_val == constraint_val:
						self.values[val_index] = 0

		elif self.type == 21:
			self.values = [[0 for x in range(len(graph.values))] for y in range(len(graph.values))]
			for i in range(0,len(graph.values)):
				self.values[i][i] = 1

		elif self.type == 22:
			self.values = [[1 for x in range(len(graph.values))] for y in range(len(graph.values))]
			for i in range(0,len(graph.values)):
				self.values[i][i] = 0


		elif self.type == 23:
			self.values = [[1 for x in range(len(graph.values))] for y in range(len(graph.values))]
			for val_index_1, possible_val_1 in enumerate(graph.values):
				for val_index_2, possible_val_2 in enumerate(graph.values):
					if ((possible_val_1 == list_values[0] and possible_val_2 == list_values[1]) or
					(possible_val_1 == list_values[1] and possible_val_2 == list_values[0])):
						self.values[val_index_1][val_index_2] = 0

		else:
			assert False, "Constraint init: type of constraint not known"

	def __repr__(self):
		return "Constraint({0}, {1}, {2})".format(self.type, self.variables, self.values)

	def __str__(self):
		string = "\nCosntraint:\n"
		string += "Type:\n{0}\n".format(self.type)
		string += "Variables:\n{0}\n".format(self.variables)
		string += "Values:\n"
		if self.type/10 == 2:
			for j in range(len(self.values)):
				string += str(self.values[j])
				string += "\n"
		else:
			string += str(self.values)
			string += "\n"
		return "{0}, {1}, {2}".format(self.type, self.variables, self.values)



	def updateBinaryConstraint(self, graph, unaryConstraint):
		assert self.type in [21, 22, 23], "Constraint updateBinaryConstraint: constraint type not in whitelist"


		if len(unaryConstraint.variables) == 0:
			return

		if unaryConstraint.variables[0] == self.variables[0]:
			for i in range(len(graph.values)):
				for j in range(len(graph.values)):
					self.values[i][j] = (self.values[i][j] and unaryConstraint.values[i])

		elif unaryConstraint.variables[0] == self.variables[1]:
			for i in range(len(graph.values)):
				for j in range(len(graph.values)):
					self.values[i][j] = (self.values[i][j] and unaryConstraint.values[j])


	def updateRemainingValues(self, graph, variable, remainingValues, assignment):
		#input: graph, Variable, [1, 1, ...], asssignment([Variable, Value])
		#output: modify remainingValues to be consistent with self constraint and assignment

		if variable not in self.variables:
			return

		assign = variable.assignedTo(assignment)
		if assign:
			return

		if self.type < 10:
			return
		elif self.type < 20:
			for i in range(len(remainingValues)):
				remainingValues[i] = remainingValues[i] and self.values[i]
		else:
			otherVariableIsAssigned = False
			if variable == self.variables[0]:
				currentVar = self.variables[0]
				otherVar = self.variables[1]
			else:
				currentVar = self.variables[1]
				otherVar = self.variables[0]
			otherVal = otherVar.assignedTo(assignment)
			if otherVal != False:
				otherVariableIsAssigned = True

			if not otherVariableIsAssigned:
				if currentVar == self.variables[0]:
					for i in range(len(self.values)):
						remain = 0
						for j in range(len(self.values[0])):
							if self.values[i][j] == 1:
								remain = 1
								break
						remainingValues[i] = remainingValues[i] and remain
				else:
					for i in range(len(self.values)):
						remain = 0
						for j in range(len(self.values[0])):
							if self.values[j][i] == 1:
								remain = 1
								break
						remainingValues[i] = remainingValues[i] and remain
			else:
				if currentVar == self.variables[0]:
					for i in range(len(self.values)):
						remainingValues[i] = remainingValues[i] and self.values[i][graph.values.index(otherVal)]
				else:
					for i in range(len(self.values)):
						remainingValues[i] = remainingValues[i] and self.values[graph.values.index(otherVal)][i]


		#print "updated remaining values"
		#print remainingValues


class Graph:

	variables = []
	values = []

	uniform = []
	unaryInclusive = []
	unaryExclusive = []
	binaryEqual = []
	binaryNotEqual = []
	binaryNotSimultaneous = []

	possibleAssignments = []

	constraints = [uniform, unaryInclusive, unaryExclusive, binaryEqual, binaryNotEqual, binaryNotSimultaneous]

	def __str__(self):
		string = "List of variables:\n"
		for var in self.variables:
			string += "{0}\n".format(var.name)

		string += "\nList of values:\n"
		for val in self.values:
			string += "{0}\n".format(val.name)

		string += "\nList of constraints:\n"
		for const in self.constraints:
			string += "{0}\n".format(const)

		return string


	# list_variables = [[var1arg1, var1arg2, ...], [var2arg1,...], ...]
	# list_values = [value1, value2, ...]
	def __init__(self, list_variables, list_values, constraints_deadline = [],
					constraints_unary_inclusive = [], constraints_unary_exclusive = [], constraints_binary_equal = [],
					constraints_binary_not_equal = [], constraints_binary_not_simultaneous = []):

		for var_args in list_variables:
			self.variables.append(Variable(var_args))
		for val in list_values:
			self.values.append(Value(val))
		for var in self.variables:
			self.possibleAssignments.append([var, []])
			for val in self.values:
				self.possibleAssignments[-1][1].append(val)


		self.uniform.append(Constraint(self, 0, self.variables, constraints_deadline))

		self.addUnaryConstraint(0, constraints_unary_inclusive)
		self.addUnaryConstraint(1, constraints_unary_exclusive)

		self.addBinaryConstraint(0, constraints_binary_equal)
		self.addBinaryConstraint(1, constraints_binary_not_equal)
		self.addBinaryConstraint(2, constraints_binary_not_simultaneous)

		for binary_constraint in self.binaryEqual + self.binaryNotEqual + self.binaryNotSimultaneous:
			for unary_constraint in self.unaryInclusive + self.unaryExclusive:
				if unary_constraint.variables[0] in binary_constraint.variables:
					binary_constraint.updateBinaryConstraint(self, unary_constraint)

		self.initializePossibleAssignments()

		#print "initial possible assignments: {0}".format(self.possibleAssignments)


	def addArgumentsToValues(self, list_arguments):
	# input: [[argument1, argument2,...], [...]]
	# assume the arguments are stored in the right order directly

		assert len(list_arguments) == len(self.values)

		for value, args in zip(self.values, list_arguments):
			for arg in args:
				value.arguments.append(arg)



	def addUnaryConstraint(self,type_of_constraint, list_constraints):
		for constraint in list_constraints:
			constraintVar = -1
			for var in self.variables:
				if var.name == constraint[0]:
					constraintVar = [var]
					break
			assert constraintVar != -1

			constraintValues = []
			for constraint_val in constraint.split( )[1:]:
				for val in self.values:
					if constraint_val == val.name:
						constraintValues.append(val)
						break
			assert len(constraintValues) == len(constraint.split( ))-1

			if type_of_constraint == 0:
				self.unaryInclusive.append(Constraint(self, 11, constraintVar, constraintValues))
			if type_of_constraint == 1:
				self.unaryExclusive.append(Constraint(self, 12, constraintVar, constraintValues))

	def addBinaryConstraint(self, type_of_constraint, list_constraints):
		for constraint in list_constraints:
			constraintVar = []
			for var in self.variables:
				if var.name == constraint.split()[0] or var.name == constraint.split()[1]:
					constraintVar.append(var)
			assert len(constraintVar) == 2

			constraintValues = []
			for constraint_val in constraint.split( )[2:]:
				for val in self.values:
					if constraint_val == val.name:
						constraintValues.append(val)
						break

			assert len(constraintVar) == 2
			assert len(constraintValues) == 0 or len(constraintValues) == 2

			if type_of_constraint == 0:
				self.binaryEqual.append(Constraint(self, 21, constraintVar))
			if type_of_constraint == 1:
				self.binaryNotEqual.append(Constraint(self, 22, constraintVar))
			if type_of_constraint == 2:
				self.binaryNotSimultaneous.append(Constraint(self, 23, constraintVar, constraintValues))

	def initializePossibleAssignments(self):
		# initialize the possible assignment with the initial constraints
		# constraints = [list_constraints_1, list_constraints_2, ...]
		for [var, assignments] in self.possibleAssignments:
			for constraint_list in self.constraints[1:]: #TODO: increment if unary constraints start not at constraints[1]
				for constraint in constraint_list:
					if var not in constraint.variables:
						continue
					elif constraint.type > 9 and constraint.type < 20:
						for i, isPossible in enumerate(constraint.values):
							if not isPossible and self.values[i] in assignments:
								assignments.remove(self.values[i])
					elif constraint.type > 19:
						if var == constraint.variables[0]:
							for i in range(len(constraint.values)):
								isPossible = False
								for j in range(len(constraint.values[0])):
									if constraint.values[i][j] == 1:
										isPossible = True
										break
								if not isPossible and self.values[i] in assignments:
									assignments.remove(self.values[i])
						elif var == constraint.variables[1]:
							for i in range(len(constraint.values[0])):
								isPossible = False
								for j in range(len(constraint.values)):
									if constraint.values[j][i] == 1:
										isPossible = True
										break
								if not isPossible and self.values[i] in assignments:
									assignments.remove(self.values[i])
						else:
							assert False


	def selectVariable(self, assignment):
		# input: assignment
		# output: [ [var, number of remaining values, number of binary constraints] ]
		# output is sorted by [1], tie break with [2]
		# only containts var not assigned
		minRemainingValues = self.countRemainingValues(self.selectRemainingValues(assignment), assignment)

		self.maxConstraintedValues(minRemainingValues, assignment)

		variableQueue = sorted(sorted(minRemainingValues, key = lambda x: x[2], reverse = True), key = lambda y: y[1])
		return variableQueue

	def maxConstraintedValues(self, setVariables, assignment):
		# input: setVariables([ [var, number of remaining values] ])
		# input: assignment([Variable, Value])
		# output: [ [var, number of remaining values, number of binary constraints with var] ]

		for i in range(len(setVariables)):
			setVariables[i].append(-1)
		for i, [var, minRemVal, init] in enumerate(setVariables):
			numberOfConstraints = 0
			for list_constraint in self.constraints:
				for constraint in list_constraint:
					if constraint.type < 20:
						break
					if var in constraint.variables:
						for [otherVar, assignedVal] in assignment:
							if otherVar in constraint.variables:
								break
						numberOfConstraints += 1
			setVariables[i][2] = numberOfConstraints
		return setVariables


	def countRemainingValues(self, remainingValues, assignment):
		# input: remainingValues([ [var, [1,0,...]] ]) for var not assigned
		# input: assignment([Variable, Value])
		# output: [ [var, number of remaining values] ]
		numberRemainingValues = []
		for [var, rV] in remainingValues:
			numberRemainingValues.append([var, sum(rV)])
		return numberRemainingValues

	def selectRemainingValues(self, assignment):
		# input: assignment([Variable, Value])
		# output: [ [var, [1,0,...]] ] for variable not assigned.

		remainingValues = []
		for var in self.variables:
			if not var.assignedTo(assignment):
				remainingValues.append([var, [1]*len(self.values)])

		for list_const in self.constraints:
			if len(list_const) == 0 or list_const[0].type < 10:
				continue

			for const in list_const:
				for [var, currentRemainingValues] in remainingValues:
					const.updateRemainingValues(self, var, currentRemainingValues, assignment)


		return remainingValues

	def selectValue(self, variable, assignment,):
		# input: Variable, assignment([Variable, Value])
		# output: [Valeur, Valeur, ...] in the right order

		# least constraining value heuristic:
		# sort the values in order of increment constraints

		# for each value possible:
		#	assume variable is assigned to value
		#	for all other variable not assigned:
		#		count the number of values the other variable can still have
		#		take the min between the other variables
		#	take the value so that the min is the highest


		valueQueue = []

		possibleValues = self.possibleAssignments[self.variables.index(variable)][1]

		# if it is the last variable to test, add all values, order not important
		if len(assignment) == len(self.variables)-1:
			for value in possibleValues:
				valueQueue.append([value, len(self.values)+1])
			return valueQueue


		for value in possibleValues:
			assignment.append([variable, value])
			valueAssignmentEffect = []
			#for this value, compute the number of remaining values and store the min
			for [var, nbRemainningVal] in self.countRemainingValues(self.selectRemainingValues(assignment), assignment):
				if var.assignedTo(assignment) or var == variable:
					continue
				else:
					valueAssignmentEffect.append([var, nbRemainningVal])

			valueQueue.append([value, sorted(valueAssignmentEffect, key = lambda x: x[1])[0][1]])
			assignment.remove([variable, value])

		assert not variable.assignedTo(assignment)
		return sorted(valueQueue, key = lambda x: x[1], reverse = True)



	def consistentAssignment(self, variable, value, assignment):

		varIndex = self.variables.index(variable)
		valIndex = self.values.index(value)


		for list_const in self.constraints :
			if len(list_const) == 0:
				continue

			for const in list_const:

				#print const

				if variable not in const.variables:
					continue
				if const.type == 0:
					length = 0
					for assign in assignment:
						if assign[1] == value:
							length += int(assign[0].args) 						#TODO change if there is no deadline constraint!!
					if not int(const.values[0]) >= length + int(variable.args):
						#print "Non consistency", variable, value, assignment, const
						return False
				elif const.type < 20:
					if const.values[valIndex] != 1:
						#print "Non consistency", variable, value, assignment, const
						return False

				else:
					otherVariableIsAssigned = False
					if variable == const.variables[0]:
						currentVar = const.variables[0]
						otherVar = const.variables[1]
					else:
						currentVar = const.variables[1]
						otherVar = const.variables[0]
					otherVal = otherVar.assignedTo(assignment)
					if otherVal != False:
						otherVariableIsAssigned = True


					if not otherVariableIsAssigned:
						consistent = False
						if variable == self.variables[0]:
							for i in range(len(const.values)):
								if const.values[valIndex][i] == 1:
									consistent = True
						else:
							for j in range(len(const.values)):
								if const.values[j][valIndex] == 1:
									consistent = True
						#if not consistent:
							#print "Non consistency", variable, value, assignment, const, otherVal
						return consistent
					else:
						if variable == self.variables[0]:
							consistent = const.values[valIndex][self.values.index(otherVal)] == 1
							#if not consistent:
								#print "Non consistency", variable, value, assignment, const
							return consistent
						else:
							consistent = const.values[self.values.index(otherVal)][valIndex] == 1
							#if not consistent:
								#print "Non consistency", variable, value, assignment, const
							return consistent
		return True




def removeInconsistentValue(graph, arc, assignment):
	# input: arc = [value assigned, value linked, binary constraint]

	removedAssignments = []
	removed = False
	if arc[0].assignedTo(assignment):
		domain1 = [arc[0].assignedTo(assignment)]
	else:
		for possibleAssignment in graph.possibleAssignments:
			if arc[0] == possibleAssignment[0]:
				domain1 = possibleAssignment[1]
				break
	for possibleAssignment in graph.possibleAssignments:
		if arc[1] == possibleAssignment[0]:
			domain2 = possibleAssignment[1]
			break

	"""
	print "arguments of removeInconsistentValue: "
	print arc, assignment
	print "possible assignments: "
	print domain1, domain2
	"""
	for possibleValue2 in domain2:
		#print "can var {0} have value {1}?".format(arc[1], possibleValue2)
		satisfied = False
		for possibleValue1 in domain1:
			if arc[1] == arc[2].variables[1]:
				if arc[2].values[graph.values.index(possibleValue1)][graph.values.index(possibleValue2)] == 1:
					satisfied = True
					break
			else:
				if arc[2].values[graph.values.index(possibleValue2)][graph.values.index(possibleValue1)] == 1:
					satisfied = True
					break


		if not satisfied:
			removedAssignments.append([arc[1], possibleValue2])
			print("---because the only possible value(s) for {0} are {1}, then {2} can not have the value {3}".format(
															arc[0].name, domain1, arc[1].name, possibleValue2.name))
			removed = True
	for [variable, removedVal] in removedAssignments:
		domain2.remove(removedVal)
	return removedAssignments


def constraintPropagation(graph, variableAssigned, assignment):
	# output: return the possible assignments removed by removeInconsistentValue
	removedPossibleAssignments = []
	# create the queue of arcs, corresponding to the binary constraints
	queue = []

	for constraint_list in graph.constraints:
		if len(constraint_list) == 0:
			continue
		if constraint_list[0].type > 20:
			for constraint in constraint_list:
				if variableAssigned == constraint.variables[0] and not constraint.variables[1].assignedTo(assignment):
					queue.append([variableAssigned, constraint.variables[1], constraint])
				elif variableAssigned == constraint.variables[1] and not constraint.variables[0].assignedTo(assignment):
					queue.append([variableAssigned, constraint.variables[0], constraint])



	while len(queue) > 0:
		#print "queue ", queue
		arc = queue[0]
		del queue[0]
		removedAssignments = removeInconsistentValue(graph, arc, assignment)
		if len(removedAssignments) != 0:
			for assign in removedAssignments:
				removedPossibleAssignments.append(assign)
			for constraint_list in graph.constraints:
				if len(constraint_list) == 0:
					continue
				if constraint_list[0].type > 20:
					for constraint in constraint_list:
						if arc[1] == constraint.variables[0] and not constraint.variables[1].assignedTo(assignment):
							queue.append([arc[1], constraint.variables[1], constraint])
						elif arc[1] == constraint.variables[1] and not constraint.variables[0].assignedTo(assignment):
							queue.append([arc[1], constraint.variables[0], constraint])

	return removedPossibleAssignments


def backtrackingSearch(graph):
	return recursiveBacktracking([], graph)

def printVarValList(varValList):
	string = "-"
	for varVal in varValList:
		string += "{0} ".format(varVal[0].name)
	print(string)

def recursiveBacktracking(assignment, graph):
	if len(assignment) == len(graph.variables):
		return assignment

	variablesInOrder = graph.selectVariable(assignment)
	print("\nVariables are ordered like this:")
	printVarValList(variablesInOrder)
	for [var, numRemainVal, numConstr] in variablesInOrder:
		print("\n-Variable selected: {0}".format(var))
		#print "possible assignments: {0}".format(graph.possibleAssignments)
		valuesInOrder = graph.selectValue(var, assignment)
		print("-Values are ordered like this:")
		printVarValList(valuesInOrder)
		for [val, minRemVal] in valuesInOrder:
			print("--test with value {0}".format(val))
			if graph.consistentAssignment(var, val, assignment):
				print("---{0} assigned {1} is consistent, test the children".format(var, val))
				assignment.append([var, val])
				removedAssignments = constraintPropagation(graph, var, assignment)
				result = recursiveBacktracking(assignment, graph)
				if result != False:
					return result
				for [variableRemoved, valueRemoved] in removedAssignments:
					for possibleAssign in graph.possibleAssignments:
						if variableRemoved == possibleAssign[0]:
							possibleAssign[1].append(valueRemoved)
				assignment.remove([var, val])
				print("\n---no solution with {0} assigned to {1}".format(var, val))
			print("--{0} assigned {1} is not consistent, test next variable".format(var, val))
		return False

def main():
	if len(sys.argv) != 2 and len(sys.argv) != 3:
		print("Usage: python CSP.py {input file} [optimization input file 2]")
		return

	try:
		f1 = open(sys.argv[1], "r")

	except Exception:
		pass

	lines = []
	for line in f1.readlines():
		lines.append(line[:-1])

	f1.close()

	# input list in order [variables, values, deadline constraints, unary inclusive, unary exclusive, binary equals,
	#						binary not equals, binary not simultaneous]
	input_list = []
	for line in lines:
		if re.match("#####*", line):
			input_list.append([])
		else:
			input_list[-1].append(line)

	print(input_list)

	graph = Graph(input_list[0], input_list[1], input_list[2], input_list[3], input_list[4], input_list[5],
					input_list[6], input_list[7])

	# add the optimization data if present
	# /!\ assume that the variable are sorted the same way in both documents and values are second category in input1
	if len(sys.argv) == 3:
		try:
			f2 = open(sys.argv[2], "r")

		except Exception:
			pass

		linesOptimizationFile = []
		for line in f2.readlines():
			print(line)
			linesOptimizationFile.append([line.split(" ")[1][:-1]])

		f2.close()

		graph.addArgumentsToValues(linesOptimizationFile)


	solution =  backtrackingSearch(graph)
	if solution:
		print("\n\nThe algorithm found a solution:\n")
		lengthPerValue = [0]*len(graph.values)
		for assignment in solution:
			print("Variable {0}, length {2} assigned value is {1}".format(assignment[0].name,
																			assignment[1].name, assignment[0].args))
			lengthPerValue[graph.values.index(assignment[1])] += int(assignment[0].args)
		for valueIndex, value in enumerate(graph.values):
			print("Length of task assigned to processor {0} is {1}".format(value.name, lengthPerValue[valueIndex]))
	else:
		print("No solution found")


if __name__ == '__main__':
	main()

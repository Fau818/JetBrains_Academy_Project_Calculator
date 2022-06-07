from collections import deque


INVALID_IDENTIFIER = "Invalid identifier"
INVALID_ASSIGNMENT = "Invalid assignment"
UNKNOWN_VARIABLE = "Unknown variable"
INVALID_EXPRESSION = "Invalid expression"


def is_num(op): return op.lstrip('-').isdigit() or op.lstrip('+').isdigit()
def calc_sign(op): return -1 if op.count('-') & 1 else 1


def is_oper(op): return op in ('+', '-', '*', '/', '^')

mp: dict[str, int] = dict()  # save variable
oper_level: dict[str, int] = {
	'+': 1, '-': 1,
	'*': 2, '/': 2,
	'^': 3
}


def calc_val(a, b, op):
	if op == '+': return a + b
	elif op == '-': return a - b
	elif op == '*': return a * b
	elif op == '/': return a // b
	return a ** b


def calc(st1: deque, st2: deque):  # if legal return RES else return ERROR
	if len(st1) < 2 or not st2: return False
	b, a = st1.pop(), st1.pop()
	op = st2.pop()

	if not is_oper(op): return False
	st1.append(calc_val(a, b, op))
	return True

	# print("(a, op, b, res)", a, op, b, st1[-1])


def calculate():
	st1: deque = deque()  # save variable order
	st2: deque = deque()  # save operation order

	global user_input
	val: str = ""  # current number
	for now in user_input:
		if now == ' ': continue

		# deal with digit
		if now.isdigit():
			val = val + now
			continue
		elif val: st1.append(int(val)); val = ""


		# deal with ( and )
		if now == '(': st2.append(now); continue
		elif now == ')':
			while st2 and st2[-1] != '(':
				if not calc(st1, st2): return INVALID_ASSIGNMENT

			if len(st2): st2.pop()
			else: return INVALID_EXPRESSION
			continue


		# deal with operation
		if is_oper(now):
			while st2 and st2[-1] != '(' and oper_level[st2[-1]] >= oper_level[now]:
				if not calc(st1, st2): return INVALID_ASSIGNMENT
			st2.append(now)
			continue


		# deal with variable
		if now in mp: st1.append(mp[now])
		else: return UNKNOWN_VARIABLE



	else:  # if while end, but the last char is digit.
		if val: st1.append(int(val))

	while st2 and st2[-1] != '(': calc(st1, st2)

	if len(st1) != 1 or st2: return INVALID_EXPRESSION
	return st1.pop()



while True:
	user_input = input()
	if not user_input: continue  # white line

	# commands
	if user_input.startswith('/'):
		if user_input == '/exit': break
		elif user_input == '/help': print("Please enjoy it!")
		else: print("Unknown command")  # error

		continue


	# assignment
	if '=' in user_input:
		if user_input.count('=') > 1:
			print(INVALID_ASSIGNMENT)
			continue

		var, val = [op.strip() for op in user_input.split('=')]
		var: str; val: str  # hints
		if not var.isalpha(): print(INVALID_IDENTIFIER)
		else:  # legal var
			if val.isdigit(): mp[var] = int(val)
			elif val in mp: mp[var] = mp[val]
			elif val.isalpha(): print(UNKNOWN_VARIABLE)
			else: print(INVALID_ASSIGNMENT)

		continue

	# calculate
	print(calculate())



print("Bye!")  # END


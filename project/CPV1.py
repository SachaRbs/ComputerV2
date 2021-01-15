import argparse
import sys
import re
import matplotlib.pyplot as plt
import numpy as np


def parsing(equation):
	if check_equation(equation) is False:
		exit()
	equation = equation.split('=')
	if len(equation) != 2:
		print("ERROR: Equation is not well formatted, it has to be an equality with only one ('=')")
		exit()
	if equation[0] == "" or equation[1] == "":
		print("ERROR: Missing one side of the equality")
		exit()
	if (equation[0] != "0") or (equation[1] != "0"):
		equation = poly_zero(equation[0], equation[1])
		if equation == False:
			print("ERROR: Equation is not well formatted")
			exit()
	elif equation[0] == "0":
		equation = equation[1]
	elif equation[1] == "0":
		equation = equation[0]
	if equation:
		polynome = reduce_form(equation)
	else:
		print("ERROR: Equation does not exist")
		exit()
	if polynome is False:
		print("The polynomial degree is stricly greater than 2, I can't solve.")
		exit()
	return polynome

def natural(equation):
	equation = equation.upper()
	therms = re.split(r"(\+|\-|\=)", equation)
	therms = list(filter(None, therms))
	get = '+'
	new = ""
	for i in range(len(therms)):
		if therms[i] == '-' or therms[i] =='+' or therms[i] == '=':
			if therms[i] == '=':
				new = new + '='
			if therms[i] == '-':
				get = '-'
			continue
		if therms[i] == 'X':
			therms[i] = '1*X^1'
		if re.match(r"X\^[.?\d]+$", therms[i]) is not None:
			therms[i] = '1*' + therms[i]
		if 'X' not in therms[i]:
			therms[i] = therms[i] + '*X^0'
		if 'X' == therms[i][-1]:
			therms[i] = therms[i] + '^1'
		if '*' not in therms[i]:
			idx = therms[i].find('X')
			therms[i] = therms[i][:idx] + '*' + therms[i][idx:]
		new = new + get + therms[i]
		get = '+'
	return new

def _sqrt(num):
  	return num**0.5

def solve_first_poly(polynome):
	x = - polynome[0] / polynome[1]
	print("The solution is:")
	print("{}".format(x))

def solve_second_poly(a, b, c):
	delta = (b**2) - (4 * a * c)
	if delta < 0:
		print("Discriminant is strictly negative, there is two complex solutions:")
		print("z1: {} - (i * √{})/{}".format(-b / (2 * a), -delta, 2 * a))
		print("z2: {} + (i * √{})/{}".format(-b / (2 * a), -delta, 2 * a))

	elif delta == 0:
		print("Discriminant is equal to zero the only solution is:")
		x = -b / (2 * a)
		print("x: {}".format(x))
	else:
		print("Discriminant is strictly positive, the two solutions are:")
		x1 = (- b - _sqrt(delta)) / (2 * a)
		x2 = (-b + _sqrt(delta)) / (2 * a)
		print("x1 :  {}".format(x1))
		print("x2 :  {}".format(x2))


def calculus(polynome):
	if not polynome[0] and not polynome[1] and not polynome[2]:
		# print("Reduced form: X = X")
		print("all the numbers are solution of the equation")
		exit()
	elif not polynome[1] and not polynome[2]:
		print("There is no solution to the equation")
		exit()
	elif polynome[2] == 0:
		solve_first_poly(polynome)
	else:
		solve_second_poly(polynome[2], polynome[1], polynome[0])
	
def check_equation(equation):
	equation = equation.replace(' ', '')
	therms = re.split(r"\+|\-|\=", equation)
	therms = list(filter(None, therms))
	for therm in therms:
		if (re.search(r"[.?\d]+\*X\^[.?\d]+$", therm)) is None and therm != "0":
			print("ERROR: equation is not well formated, term [{}] is not formatted like [a * X^p]".format(therm))
			return False
	return True


def poly_zero(left, right):
	res = re.split(r"(\+|\-)", right)
	res = list(filter(None, res))
	get = '+'
	inverse = {'-': '+', '+': '-'}
	multi = 0
	for item in res:
		if item == '-' or item =='+':
			if item == '-':
				get = '-'
			multi = multi + 1
			if multi == 2:
				return False
			continue
		multi = 0
		left = left + inverse[get] + item
		get = '+'
	return left


def int_or_float(s):
	try:
		return int(s)
	except:
		return float(s)


def get_reduce(polynome):
	reduce_ = ""
	sign = ""
	maxPol = 0
	for i in polynome:
		if polynome[i] != 0:
			maxPol = i
			if polynome[i] < 0:
				sign = ' - '
				reduce_ = reduce_ + sign + '{} * X^{}'.format((polynome[i] * -1), i)
			elif polynome[i] == 0:
				reduce_ = reduce_ + sign + 'X^{}'.format(i)
			else:
				reduce_ = reduce_ + sign + '{} * X^{}'.format(polynome[i], i)
			sign = ' + '
	if reduce_ != "":
		reduce_ = (reduce_ + ' = 0').strip()
		print("Reduced form: {}".format(reduce_))
		# print("Polynomial degree: {}".format(maxPol))
	return maxPol


def reduce_form(equation):
	if equation[0] != '+':
		equation = '+' + equation
	res = re.findall(r"[\+\-][.?\d]+\*X\^[.?\d]+", equation)
	polynome = {0: 0,
				1: 0,
				2: 0}
	for item in res:
		tmp = item.split('*')
		try:
			polynome[int(tmp[1][2:])] = polynome[int(tmp[1][2:])] + int_or_float(tmp[0])
		except:
			polynome[int(tmp[1][2:])] = int_or_float(tmp[0])
	maxPol = get_reduce(polynome)
	if maxPol > 2:
		return False
	return(polynome)

def compute_poly(equation):
	equation = natural(equation)
	polynome = parsing(equation)
	if polynome is not False:
		calculus(polynome)
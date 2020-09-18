import signal
import equations as eq
import random # noqa
import time
import ctypes
import pathlib
import itertools

init = time.perf_counter()

game = eq.Game()
rolls = game.roll()

nums = list(filter(lambda x: isinstance(x, int), rolls))
ops = list(filter(lambda x: isinstance(x, str), rolls))
nums = [1, 2, 2, 3, 4, 5, 8, 9]
ops = ['+', '-', '-', '*', '^', 'v']
goal = nums[random.randint(0, len(nums) - 1)]
nums.remove(goal)
# nums = sorted([1, 1, 0, 2, 2])
# ops = ['-', '*', '+', '-']
# goal = 0
print('Numbers: %s\nOperators: %s\nGoal: %d' % (nums, ops, goal))

max_length = min(2*len(nums) - 1, 2*len(ops) + 1)
print('Max Length of Equations: ', max_length)

number_of_equations = 0


def generate_pairs(state, nums, ops):
    """Generates operator + digit pairs and the new
    states that come from them.

    :state: state to extend
    :nums: list of digits
    :ops: list of operators
    :returns: new states

    """
    temp_states = []
    for op in range(len(ops)):
        if op in state['ops_used']:
            continue
        ops_used = state['ops_used'] + [op]
        for nu in range(len(nums)):
            if nu in state['nums_used']:
                continue
            nums_used = state['nums_used'] + [nu]
            eval_expr = state['eval'] + [ops[op], str(nums[nu])]
            repr = state['repr'] + [ops[op], str(nums[nu])]
            temp_states += [{'eval': eval_expr, 'repr': repr,
                             'nums_used': nums_used, 'ops_used': ops_used}]
    return temp_states


unique_times = []
eval_times = []
total_check_times = []

libname = pathlib.Path().absolute() / 'eval.so'
clib = ctypes.CDLL(libname)


class RESULT(ctypes.Structure):
    _fields_ = [("ret", ctypes.c_int),
                ("val", ctypes.c_longdouble),
                ("msg", ctypes.c_char_p)]


clib.parse.restype = RESULT
clib.unique.restype = ctypes.c_bool


def check_states(states, equations, reprs, checked, invalid):
    """Checks the states and adds unique ones that
    evaluate to the goal

    :states: list of states
    :equations: list of eval-ready equations
    :reprs: list of representations of the equations,
        lists of digits and operators.

    """
    finished_eval = True

    def handler(signum, frame):
        if not finished_eval:
            raise Exception('timeout')
    signal.signal(signal.SIGALRM, handler)

    def is_unique(new, old):
        start_t = time.perf_counter()
        StringArray = ctypes.c_char_p * len(old)
        clib.unique.argtypes = [
            ctypes.c_char_p,
            StringArray,
            ctypes.c_int]
        new_byte_array = ''.join(new).encode('utf-8')
        unique = clib.unique(
            new_byte_array, StringArray(
                *old), len(old))
        unique_times.append(time.perf_counter() - start_t)
        return unique
    for s in states:
        expr = ''.join(s['eval'])
        if expr not in equations and is_unique(s['repr'], reprs):
            if expr not in invalid:
                too_big = False
                for c in invalid:
                    if c == expr or c in expr:
                        too_big = True
                if too_big:
                    invalid.add(expr)
                elif expr not in checked:
                    signal.alarm(1)
                    try:
                        finished_eval = False
                        start_t = time.perf_counter()
                        result = clib.parse(expr.encode('utf-8'))
                        if result.ret != 0:
                            raise Exception(result.msg.decode())
                        result = result.val
                    except Exception as e:
                        if str(e) != 'float division by zero':
                            pass
                        invalid.add(expr)
                    eval_times.append(time.perf_counter() - start_t)
                    finished_eval = True
                    if result is not None and result == goal \
                            and round(result) == result:
                        equations.add(expr)
                        reprs.append(''.join(s['repr']).encode('utf-8'))
                    else:
                        checked.add(expr)


parens_time = []


def generate_parens(state, positions):
    """TODO: Docstring for generate_parens.

    :state: TODO
    :open_pos: TODO
    :close_pos: TODO
    :returns: TODO

    """
    temp_states = []
    for p in parens:
        new_state = {}
        count = 0
        temp = state
        for i in sorted(p):
            if p[i]['val'] == '(':
                new_state['eval'] = temp['eval'][0:i + count] + \
                    ['('] * p[i]['count'] + temp['eval'][i + count:]
                new_state['repr'] = temp['repr'][0:i + count] + \
                    ['('] * p[i]['count'] + temp['repr'][i + count:]
            else:
                if i + count == len(new_state['eval']):
                    new_state['eval'] += [')'] * p[i]['count']
                    new_state['repr'] += [')'] * p[i]['count']
                else:
                    new_state['eval'] = temp['eval'][0:i + count + 1] + \
                        [')'] * p[i]['count'] + \
                        temp['eval'][i + count + 1:]
                    new_state['repr'] = temp['repr'][0:i + count + 1] + \
                        [')'] * p[i]['count'] + \
                        temp['repr'][i + count + 1:]
            count += p[i]['count']
            temp = new_state
        temp_states.append(new_state)

    return temp_states


equations = set()
reprs = []
invalid = set()
for i in range(1, max_length+1, 2):
    length = 0
    states = []
    i_length_reprs = []
    i_length_checked = set()
    i_length_states = []
    i_length_parens = []
    open_pos = list(range(0, i, 2))
    close_pos = list(range(2, i, 2))
    positions = itertools.product(open_pos, close_pos)
    positions = list(filter(lambda p: p[0] < p[1], positions))
    positions = [p for i in range(0, len(positions))
                 for p in itertools.combinations(positions, i + 1)]
    parens = []
    for ps in positions:
        new_state = {}
        (opens, closes) = zip(*ps)
        if len(set(opens) & set(closes)) > 0:
            continue
        if(0 in opens and i-1 in closes):
            continue
        new_parens = {}
        for o in opens:
            if o in new_parens:
                new_parens[o]['count'] += 1
            else:
                new_parens[o] = {'val': '(', 'count': 1}
        for o in closes:
            if o in new_parens:
                new_parens[o]['count'] += 1
            else:
                new_parens[o] = {'val': ')', 'count': 1}
        parens.append(new_parens)
    for n in range(len(nums)):
        temp_nums = nums
        temp_ops = ops
        equation = str(nums[n])
        length = 1
        states = [{'eval': [equation], 'repr': [
            equation], 'nums_used': [n], 'ops_used': []}]
        paren_states = []
        while length < i:
            temp_states = []
            for s in states:
                temp_states += generate_pairs(s, nums, ops)
            states = temp_states
            length += 2
        start_t = time.perf_counter()
        for s in states:
            paren_states += generate_parens(s, parens)
        parens_time.append(time.perf_counter() - start_t)
        i_length_states += states
        i_length_parens += paren_states
        eqs = set()
    print('Generated all %d-resource length equations' % (i))
    i_length_states += i_length_parens
    number_of_equations += len(i_length_states)
    start_check = time.perf_counter()
    check_states(
        i_length_states,
        equations,
        i_length_reprs,
        i_length_checked,
        invalid)
    total_check_times.append(time.perf_counter() - start_check)
    reprs += i_length_reprs
    print('Checked all %d-resource length equations' % (i))

total_time = time.perf_counter() - init
print(list(equations))
print("Checked %d equations in %f seconds" %
      (number_of_equations, total_time))
print("Percent of check spent on eval: %f%%" %
      (sum(eval_times) / sum(total_check_times) * 100))
print("Percent of check spent on unique: %f%%" %
      (sum(unique_times) / sum(total_check_times) * 100))
print("Percent of time spent on check: %f%%" %
      (sum(total_check_times) / (total_time) * 100))
print("Percent of time spent on parens: %f%%" %
      (sum(parens_time) / (total_time) * 100))

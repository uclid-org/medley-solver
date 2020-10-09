from collections import OrderedDict, namedtuple

SOLVERS = OrderedDict({
    "Z3"   : "z3",
    "CVC4" : "~/tools/cvc4",
    "BOOLECTOR" : "~/tools/boolector/boolector/bin/boolector",
    "YICES": "~/bin/yices-smt2",
    "MathSAT": "~/tools/mathsat/bin/mathsat",
#    "Vampire": "~/tools/vampire --input_syntax smtlib2 ",
    "Bitwuzla": "~/tools/Bitwuzla/bin/bitwuzla",
})

SAT_RESULT     = 'sat'
UNSAT_RESULT   = 'unsat'
UNKNOWN_RESULT = 'unknown'
TIMEOUT_RESULT = 'timeout (%.1f s)' #% TIMEOUT
ERROR_RESULT   = 'error'

Result = namedtuple('Result', (
    'problem', 
    'result', 
    'elapsed'
))

Solved_Problem = namedtuple('Solved_Problem', (
    'problem',
    'datapoint',
    'solve_method',
    'time',
    'result',
    'order',
    'time_spent'
))

keyword_list = [
    ##SMT-LIB
    'as',
    'assert',
    'check-sat',
    'check-sat-assuming',
    'declare-const',
    'declare-datatype',
    'declare-datatypes',
    'declare-fun',
    'declare-sort',
    'define-fun',
    'define-fun-rec',
    'define-funs-rec',
    'define-sort',
    'echo',
    'exit',
    'get-assertions',
    'get-assignment',
    'get-assignment',
    'get-info',
    'get-info',
    'get-model',
    'get-option',
    'get-option',
    'get-proof',
    'get-unsat-assumptions',
    'get-unsat-core',
    'get-value',
    'pop',
    'push',
    'reset',
    'reset-assertions',
    'set-info',
    'set-logic',
    'set-option',

    ##BINDERS
    'exists',
    'forall',
    'let',

    ##CORE
    'true',
    'false',
    'not',
    '=>',
    'and',
    'or',
    'xor',
    '=',
    'distinct',
    'ite',
    'Bool',

    ##ARRAYS
    'Array',
    'select',
    'store',

    ##BV
    'BitVec',
    'concat',
    'extract',
    'bvnot',
    'bvand',
    'bvor',
    'bvneg',
    'bvadd',
    'bvmul',
    'bvudiv',
    'bvurem',
    'bvshl',
    'bvlshr',
    'bvult',
    'bvnand',
    'bvnor',
    'bvxor',
    'bvxnor',
    'bvcomp',
    'bvsub',
    'bvsdiv',
    'bvsrem',
    'bvsmod',
    'bvashr',
    'repeat',
    'zero_extend',
    'sign_extend',
    'rotate_left',
    'rotate_right',
    'bvule',
    'bvugt',
    'bvuge',
    'bvslt',
    'bvsle',
    'bvsgt',
    'bvsge',

    ##FP
    'RoundingMode',
    'Real',
    'FloatingPoint',
    'Float16',
    'Float32',
    'Float64',
    'Float128',
    'fp',

    'roundNearestTiesToEven',
    'roundNearestTiesToAway',
    'roundTowardPositive',
    'roundTowardNegative',
    'roundTowardZero',

    'RNE',
    'RNA',
    'RTP',
    'RTN',
    'RTZ',

    'fp.abs',
    'fp.neg',
    'fp.add',
    'fp.sub',
    'fp.mul',
    'fp.div',
    'fp.fma',
    'fp.sqrt',
    'fp.rem',
    'fp.roundToIntegral',
    'fp.min',
    'fp.max',
    'fp.leq',
    'fp.lt',
    'fp.geq',
    'fp.gt',
    'fp.eq',
    'fp.isNormal',
    'fp.isSubnormal',
    'fp.isZero',
    'fp.isInfinite',
    'fp.isNaN',
    'fp.isNegative',
    'fp.isPositive',
    'to_fp',
    'to_fp_unsigned',
    'fp.to_ubv',
    'fp.to_sbv',
    'fp.to_real',


    ##INTS+REAL
    'Int',
    '-',
    '+',
    '*',
    'div',
    'mod',
    'abs',
    '<=',
    '<',
    '>=',
    '>',
    'to_real',
    'to_int',
    'is_int',

]

def is_solved(foo):
    return foo == SAT_RESULT or foo == UNSAT_RESULT


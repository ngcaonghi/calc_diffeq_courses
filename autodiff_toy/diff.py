import numpy as np

# INTERFACE ====================================================================

class NodeFunction(object):
    def f(self):
        pass
    def df(self):
        pass

# BASIC TYPES ==================================================================

class Var(NodeFunction):
    _name = 'var'
    _max_in = 1
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return self.x.__repr__()
    def f(self):
        return self.x
    def df(self):
        return np.sign(self.x)

class Const(NodeFunction):
    _name = 'const'
    _max_in = 1
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return self.x
    def f(self):
        return self.x
    def df(self):
        return 0

# SIMPLE FUNCTIONS =============================================================

class Pow(NodeFunction):
    _name = '^'
    _max_in = 1
    def __init__(self, x, n):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.n = n
        self.__name = '^{}'.format(n)
        self.max_in = 1
    def __repr__(self):
        return '{}^{}'.format(self.x.__repr__(), self.n)
    def f(self):
        return self.x.f() ** self.n
    def df(self):
        return self.n * (self.x.f() ** (self.n - 1)) * self.x.df()

class Sum(NodeFunction):
    _name = '+'
    _max_in = np.inf
    def __init__(self, *args):
        self.args = args
        for x in agrs:
            assert issubclass(x.__class__, NodeFunction)
    def __repr__(self):
        rep = '(' + self.args[0]
        for x in self.args[1:]:
            rep += '+' + str(x.__repr__())
        rep += ')'
        return rep
    def f(self):
        return  np.sum([x.f() for x in self.args])
    def df(self):
        return np.sum([x.df() for x in self.args])

class Prod(NodeFunction):
    _name = '*'
    _max_in = np.inf
    def __init__(self, *args):
        assert len(args) > 1
        self.args = args
        for x in agrs:
            assert issubclass(x.__class__, NodeFunction)
    def __repr__(self):
        rep = self.args[0]
        for x in self.args[1:]:
            rep += '*' + str(x.__repr__())
        return rep
    def f(self):
        return  np.prod([x.f() for x in self.args])
    def df(self):
        template = np.array(self.args)
        template_f = np.array([x.f() for x in template])
        matrix = np.vstack([template_f for i in range(len(template))])
        for i in range(len(template)):
            matrix[i][i] = template[i].df()
        return np.sum(np.prod(matrix, axis=1))

class Div(NodeFunction):
    '''
    CAUTION: THINK OF HOW TO IMPLEMENT DENOM AND NUM INPUTS IN GUI
    '''
    _name = '/'
    _max_in = 2
    def __init__(self, denom, num=Const(1)):
        assert issubclass(denom.__class__, NodeFunction) \
            & issubclass(num.__class__, NodeFunction)
        self.denom = denom
        self.num = num
    def __repr__(self):
        return '[({}) / ({})]'.format(self.num.__repr__(), self.denom.__repr__())
    def f(self):
        return self.num.f() / self.denom.f()
    def df(self):
        return (self.num.df()*self.denom.f() - self.denom.df()*self.num.f())\
            / (self.denom.f() ** 2)

class Log(NodeFunction):
    _name = 'log'
    _max_in = 2
    def __init__(self, x, base=Const(np.e)):
        assert issubclass(x.__class__, NodeFunction) \
            & issubclass(base.__class__, NodeFunction)
        self.x = x
        self.base = base
        self.__name = 'log{}'.format(base)
    def __repr__(self):
        return 'log_({})({})'.format(self.base.__repr__(), self.x.__repr__())
    def f(self):
        return np.log(self.x.f()) / np.log(self.base.f())
    def df(self):
        if (isinstance(self.base, Const)):
            return 1/(self.x.f()*np.log(self.base.f())) * self.x.df()
        else:
            assert (isinstance(self.base, Var))
            return Div(denom=Log(self.base), num=Log(self.x)).df()

class Exp(NodeFunction):
    _name = 'exp'
    _max_in = 2
    def __init__(self, x, base=Const(np.e)):
        assert issubclass(x.__class__, NodeFunction) \
            & issubclass(base.__class__, NodeFunction)
        if base.f() == np.e:
            self.x = x
            self.base = base
        else:
            self.base = Const(np.e)
            self.x = Prod(self.x, Log(self.base))
    def __repr__(self):
        return 'e^({})'.format(self.x.__repr__())
    def f(self):
        return self.base.f() ** self.x.f()
    def df(self):
        return self.f() * self.x.df()

# TRIGONOMETRIC FUNCTIONS ======================================================

class Sin(NodeFunction): 
    _name = 'sin'
    _max_in = 1
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
    def __repr__(self):
        return 'sin({})'.format(self.x.__repr__())
    def f(self):
        return np.sin(self.x.f())
    def df(self):
        return np.cos(self.x.f()) * self.x.df()

class Cos(NodeFunction): 
    _name = 'cos'
    _max_in = 1
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
    def __repr__(self):
        return 'cos({})'.format(self.x.__repr__())
    def f(self):
        return np.cos(self.x.f())
    def df(self):
        return -np.sin(self.x.f()) * self.x.df()

class Tan(NodeFunction): 
    _name = 'tan'
    _max_in = 1
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
    def __repr__(self):
        return 'tan({})'.format(self.x.__repr__())
    def f(self):
        return np.tan(self.x.f())
    def df(self):
        return 1/(np.cos(self.x.f())**2) * self.x.df()

class Cot(NodeFunction): 
    _name = 'cot'
    _max_in = 1
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
    def __repr__(self):
        return 'cot({})'.format(self.x.__repr__())
    def f(self):
        return 1/np.tan(self.x.f())
    def df(self):
        return -1/(np.sin(self.x.f())**2) * self.x.df()

class Arcsin(NodeFunction): 
    _name = 'arcsiwickedn'
    _max_in = 1
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arcsin'
    def __repr__(self):
        return 'arcsin({})'.format(self.x.__repr__())
    def f(self):
        return np.arcsin(self.x.f())
    def df(self):
        return (1/np.sqrt(1 - self.x.f()**2)) * self.x.df()

class Arccos(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arccos'
    def __repr__(self):
        return 'arccos({})'.format(self.x.__repr__())
    def f(self):
        return np.arccos(self.x.f())
    def df(self):
        return -(1/np.sqrt(1 - self.x.f()**2)) * self.x.df()

class Arctan(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arctan'
    def __repr__(self):
        return 'arctan({})'.format(self.x.__repr__())
    def f(self):
        return np.arctan(self.x.f())
    def df(self):
        return (1/(1 + self.x.f()**2)) * self.x.df()

class Arccot(NodeFunction):
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arccot'
    def __repr__(self):
        return 'arctan({})'.format(self.x.__repr__())
    def f(self):
        return np.arctan(1/self.x.f())
    def df(self):
        return (-1/(1 + self.x.f()**2)) * self.x.df()

# HYPERBOLIC FUNCTIONS =========================================================
class Sinh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'sinh'
    def __repr__(self):
        return 'sinh({})'.format(self.x.__repr__())
    def f(self):
        return np.sinh(self.x.f())
    def df(self):
        return np.cosh(self.x.f()) * self.x.df()

class Cosh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'cosh'
    def __repr__(self):
        return 'cosh({})'.format(self.x.__repr__())
    def f(self):
        return np.cosh(self.x.f())
    def df(self):
        return -np.sinh(self.x.f()) * self.x.df()

class Tanh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'tanh'
    def __repr__(self):
        return 'tanh({})'.format(self.x.__repr__())
    def f(self):
        return np.tanh(self.x.f())
    def df(self):
        return 1/(np.cosh(self.x.f())**2) * self.x.df()

class Coth(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'coth'
    def __repr__(self):
        return 'coth({})'.format(self.x.__repr__())
    def f(self):
        return 1/np.tanh(self.x.f())
    def df(self):
        return -1/(np.sinh(self.x.f())**2) * self.x.df()

class Arcsinh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arcsinh'
    def __repr__(self):
        return 'arcsinh({})'.format(self.x.__repr__())
    def f(self):
        return np.arcsinh(self.x.f())
    def df(self):
        return (1/np.sqrt(1 + self.x.f()**2)) * self.x.df()

class Arccosh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arccosh'
    def __repr__(self):
        return 'arccosh({})'.format(self.x.__repr__())
    def f(self):
        return np.arccosh(self.x.f())
    def df(self):
        return (1/np.sqrt(self.x.f()**2 - 1)) * self.x.df()

class Arctanh(NodeFunction): 
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arctanh'
    def __repr__(self):
        return 'arctanh({})'.format(self.x.__repr__())
    def f(self):
        return np.arctanh(self.x.f())
    def df(self):
        return (1/(1 - self.x.f()**2)) * self.x.df()

class Arccoth(NodeFunction):
    def __init__(self, x):
        assert issubclass(x.__class__, NodeFunction)
        self.x = x
        self.__name = 'arccoth'
    def __repr__(self):
        return 'arctan({})'.format(self.x.__repr__())
    def f(self):
        return np.arctan(1/self.x.f())
    def df(self):
        return (1/(1 - self.x.f()**2)) * self.x.df()


if __name__ == '__main__':
    x = Var(1)
    print(Prod(Pow(x, 5), Div(Sum(Prod(x, Const(3)), Const(9)))))
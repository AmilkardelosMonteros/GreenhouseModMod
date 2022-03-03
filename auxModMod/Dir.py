#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:02:17 2019

@author: jac

ModMod, an environment for coding Modular models:
Define, debug and Run dynamic models on many modules with several variables

To do list:
    
    - Inconsisntencis with saves variables etc.
    - List of variables
    - 

"""
from sys import exc_info

from numpy import zeros, arange, diff, mean, array, arange, append
from pylab import plot, xlabel, ylabel, title
from sympy import latex, symbols, simplify

from pandas import read_excel

from numpy import format_float_scientific
def str_ScientificNotation( x, precision=4):
    """Wrapper for format_float_scientific with fixed str size depending on precision."""
    return ("{:>%d}" % (8+precision,)).format(\
           format_float_scientific( x, precision=precision, trim='0', exp_digits=3))

# Butcher Tableau of RK methods, as described in
# https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
#       { 'Method':3, 'Ord':3, 'name':"Not yet implemented."},\
RKcoef = ( \
       { 'Method':0, 'Ord':1, 'name':"Euler RK1", 's':1, 'ErrorEst':False,\
                'c':array([0.0]), 'b':array([1.0]), 'a':[array([])]},\
       { 'Method':1, 'Ord':1, 'name':"Euler-Heun RK12", 's':2, 'ErrorEst':True,\
               'c':array([0.0, 1.0]), 'b':array([ 0.5, 0.5]),\
               'a':[array([]), array([1.0])],\
               'E':array([ 1.0, 0.0])},\
       { 'Method':2, 'Ord':2, 'name':"Midpoint RK2", 's':2, 'ErrorEst':False,\
               'c':array([0.0, 0.5]), 'b':array([ 0.0, 1.0]),\
               'a':[array([]), array([0.5])]},\
       { 'Method':3, 'Ord':4, 'name':"Classic Runge-Kutta 3/8 Rule RK4", 's':4, 'ErrorEst':False,\
               'c':array([ 0.0, 1.0/3, 2.0/3, 1.0]),\
               'b':array([ 1.0/8.0, 3.0/8.0, 3.0/8.0, 1.0/8.0]),\
               'a':[ array([]), array([1.0/3]), array([-1.0/3, 1.0]), array([ 1.0, -1.0, 1.0])] },\
       { 'Method':4, 'Ord':4, 'name':"Runge-Kutta Cash-Karp RK45",'s':6, 'ErrorEst':True,\
               'c':array([ 0.0, 1.0/5, 3.0/10, 3.0/5, 1.0, 7.0/8]),\
               'b4':array([2825.0/27648, 0.0, 18575.0/48384, 13525.0/55296, 277.0/14336, 1.0/4]),\
               'b':array([ 37.0/378, 0.0, 250.0/621, 125.0/594, 0.0, 512.0/1771]),\
               'a':[ array([]), array([1.0/5]), array([ 3.0/40, 9.0/40]),\
                   array([ 3.0/10, -9.0/10, 6.0/5]),\
                   array([-11.0/54, 5.0/2, -70.0/27, 35.0/27]),\
                   array([ 1631.0/55296, 175.0/512, 575.0/13824, 44275.0/110592, 253.0/4096])],\
               'E':array([-0.00429377, 0.0, 0.01866859, -0.03415503, -0.01932199,0.0391022 ])})

def TranslateArgNames(func):
    """From a regular function, translate its var names to be called
       using self.V ... ie. from h(key) return h( key=self.V('key') ).
       You just need to add manually self.Vk if state variable.
       See example in ExamplePVT/Both/Auxiliars.py
    """

    rt = func.__code__.co_name + "( "
    for key in func.__code__.co_varnames:
        rt += key + "=self.V('%s'), " % (key,)
    rt += "\nCopy-paste the func call to your code."
    rt += "\nAdd k's to self.V to state variables, remove the comma and add ) at the end." 
    return print(rt)



class Var:
    def __init__(self, typ, varid, desc, units, val, units_symb=True, rec=1, prn=None, prnpres=4):
        """Class to hold, record and return value of a variable:
            typ = Type of variable, eg. 'State', 'Control', if 'Cnts'
                  then the Set method is disabled.
            name = Short description of variable.
            desc = Name and description of variable.
            units = Units of variable.  If units_symb=True, use sympy symbols to enter units.
            val = current value of variable
            rec = 1, no recording, >0 number of calls to record.
            
            prn = Print version of Var name, default to varid,
                  Use prn=r"..." with Latex, without the $ $.
            prnpres = Number of significant digits to print the value of val with.
        """
        self.typ = typ
        if self.typ == 'Cnts':
            self.Set = self.Set_Cnts # Will trigger an error if attemped to be used.
        self.varid = varid
        self.desc = desc #Description
        if units_symb:
            self.symb_units = units # symbolic espresion for units, see examples.
            #self.units = latex( units, mode='inline') #Units of the variable, in latex script, translated with sympy
            self.units = '$'+latex(units)+'$' #Units of the variable, in latex script, translated with sympy
            self.aux_symbol = symbols('a_' + varid)
        else:
            self.symb_units = None
            self.units = units
        self.val = val #Current value
        self.ncalls = 0 #NUmber of actualizations
        self.rec = rec
        self.rec_val = zeros(self.rec)
        self.rec_val[0] = self.val
        
        if prn == None:
            self.prn = self.varid
        else:
            self.prn = prn
        self.prnpres = prnpres
    
    def Set( self, val):
        """Set value of variable equal to val, and record."""
        self.val = val
        self.ncalls += 1
        i = (self.ncalls % self.rec) #Index to use, record is circular
        self.rec_val[i] = val

    def Set_Cnts( self, val):
        """Will trigger an error if attempting to change a Cnts variable."""
        raise Exception("Var.Set: Attempting to change a 'Cnts' constant Var!") 

    def GetVal(self):
        return self.val
    
    def EqualDef( self, var, warn=True):
        """Compare self with another Var instance.
           We want computer equality: two Var's are compared with
           EqualDef to check if their definition is the same, and their initial
           values are calculated equal, leading to equal val values.
           One would use fcomp on their GetVal to compare thier values.
        """
        for ky in self.__dict__.keys():
            if ky in ['rec_val', 'Set']:
                continue
            if self.__dict__[ky] != var.__dict__[ky]:
                if warn:
                    print("\nWARNING: Var.EqualDef: '%s' not equal:" % (ky,),\
                          self.__dict__[ky], "not equal to", var.__dict__[ky])
                return False
        return True
                
    def __str__(self):
        return str_ScientificNotation( self.val, precision=self.prnpres)

    def GetRecord(self):
        """Return record."""
        i = (self.ncalls % self.rec) #Current index to use, record is circular
        indx = arange( i - self.rec + 1, i + 1, step=1)
        return self.rec_val[indx]
    
    def Integral( self, n=0, t=0):
        """Return integral removing the first n recorded values."""
        val = self.GetRecord()
        if t == 0:
            return sum(val[(n+1):]) ## Simple sum
        else:
            return sum(val[(n+1):]*diff(t)[n:]) ## Integral with t
    
    def Mean( self, n=0):
        """Return the mean of the recorded values."""
        val = self.GetRecord()
        return mean(val)



class Dummy():
    def __init__(self, director=False):
        """Very dum class used by StateRHS to be able to define
           self.mod.k and self.D.Vars and self.symb_time_unit to use temporary
           for testing.
        """
        if director:
            self.Vars = {}
            self.symb_time_unit = None
        else:
            self.k = {}
            self.D = Dummy(director=True)
            
    
class StateRHS():
    def __init__(self):
        """Defines the RHS in a system of ODE's for one state variable.
           The state variable id is varid. The line is defined as
           \kappa_1 \frac{dX_1}{dt} = F_1( t, X), and then the rhs is
           \kappa_1^{-1} F_1( t, X), were the state variable is X_1.
           The evaluation of the RHS method is as this:
           RHS( Dt, k) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is a simple dictionary { 'v1':k1, 'v2':k2 ... etc}
           A Module has a list of RHS's, so that \frac{dX}{dt} = F( t, X) may be evaluated,
           the SetModule method is called so that StateRHS has access to all
           variables.
        """
        # This will be the parent Module when added
        # Meanwhile we use local self.mod.k (all equal 0) and self.D.Vars
        self.mod = Dummy()
        ### List of global and local Vars
        self.mod.D.glob_list = []
        self.mod.D.local_list = []
        self.mod.D.VarClas = {'Cnts':[]} # Variable classification, use the special names 'Cnts' only
        self.aux_symb_time_unit = symbols('modmod_rhs_a_time')
        
        self.TU_look_up_func = []
        
    def AddVar( self, typ, varid, desc, units, val, rec=1, prn=None, prnpres=4):
        """Adds a variable:
           It will create the object Var, the rest of pars are passed to Var to create the Var instance.
        """
        if varid in self.mod.D.Vars.keys():
            raise ValueError("StateRHS: Var '%s' previously defined." % (varid,))
        self.mod.D.Vars[varid] = Var( typ, varid, desc, units, val, rec=rec, prn=prn, prnpres=prnpres)
        self.mod.k[varid] = 0.0
        self.mod.D.glob_list += [varid]
        if typ == 'Cnts':
            self.mod.D.VarClas['Cnts'] += [varid]
        
    def AddVarLocal( self, typ, varid, desc, units, val, rec=1, prn=None, prnpres=4):
        """Adds a variable:
           It will create the object Var, the rest of pars are passed to Var to create the Var instance.
        """
        if varid in self.mod.D.Vars.keys():
            raise ValueError("StateRHS: Var '%s' previously defined." % (varid,))
        self.mod.D.Vars[varid] = Var( typ, varid, desc, units, val, rec=rec, prn=prn, prnpres=prnpres)
        self.mod.k[varid] = 0.0
        self.mod.D.local_list += [varid]
        if typ == 'Cnts':
            self.mod.D.VarClas['Cnts'] += [varid]
        
    def GetDirector(self):
        """Access the dummy Director, to merge Variables."""
        return self.mod.D
    
    def SetSymbTimeUnits( self, symb_time_unit):
        """Add a SymPy symbol representing the time units."""
        self.mod.D.symb_time_unit = symb_time_unit
    
    def CheckSymbTimeUnits( self, staterhs):
        """"Check that the SymbTimeUnits of another RHS are the same,
            return the symb_time_unit.
            Raise error if not.
        """
        if self.mod.D.symb_time_unit != staterhs.mod.D.symb_time_unit:
            raise Exception('VarNotEqual')
            return False
        else:
            return self.mod.D.symb_time_unit

    def GetTimeUnits(self):
        """Units for \frac{dX}{dt} for varid."""
        if self.mod.D.symb_time_unit == None:
            raise Exception('RHS.GetTimeUnits: Symbolic time unit not defined yet!')
        else:
            return self.mod.D.symb_time_unit
        
    def DerivativeUnits( self, varid):
        """Units for \frac{dX}{dt} for varid."""
        return self.mod.D.Vars[varid].symb_units / self.GetTimeUnits()
    
    def SetModule( self, mod):
        self.mod = mod    

    def V( self, varid):
        """Get value of variable.  Short for:"""
        return self.mod.D.Vars[varid].val

    def V_Mean( self, varid):
        """Get mean value of variable.  Short for:"""
        return self.mod.D.Vars[varid].Mean()

    def Vk( self, varid):
        """Get value of variable + k, k is established in mod.  Short for:"""
        return self.mod.D.Vars[varid].val + self.mod.k[varid]
    
    def V_TU( self, varid):
        """Get value of variable.  Short for:"""
        if varid in ['t', 'Dt']: # varid is time, return the time units:
            if self.aux_symb_only: ## This might happen when called from GetFuncUnits
                return self.aux_symb_time_unit
            else:
                return self.GetTimeUnits() * self.aux_symb_time_unit
        if self.aux_symb_only:
            return self.mod.D.Vars[varid].aux_symbol
        else:
            return self.mod.D.Vars[varid].aux_symbol * self.mod.D.Vars[varid].symb_units

    def Vk_TU( self, varid):
        """Get value of variable, k is ignored here:"""
        if self.mod.D.Vars[varid].typ != 'State':
            print("ModMod.StateRHS.Vk_TU: Warning, Vk used on non-State var '%s'" % (varid,))
        return self.V_TU(varid)
    
    def GetUnits( self ):
        """Run RHS with symbolically to test all units.  Note that k is not used,
           as if all = to 0.0.
           NOTE: This should be called with the sympy version of math/numpy
           functions like exp, log etc. ie, call first:
           from sympy import exp, log, ... etc
        """
        # Save the numeric versions
        tmp1 = self.V
        tmp2 = self.Vk
        
        ## Change to the sympy units versions:
        self.V = self.V_TU
        self.Vk = self.V_TU

        self.aux_symb_only = False
        # Evaluate symbolocally RHS with V_TU and Vk_TU with aux_symbol * symb_time_unit
        rt1 = self.RHS( self.aux_symb_time_unit * self.mod.D.symb_time_unit )
        self.aux_symb_only = True
        # Now evaluate symbolically RHS with V_TU and Vk_TU with aux_symbol only
        rt2 = self.RHS( self.aux_symb_time_unit * self.mod.D.symb_time_unit )

        # Return to the numeric versions:
        self.V = tmp1
        self.Vk = tmp2
        
        ### If simplify works, this should have the units
        return simplify(rt1/rt2)
    
    def GetFuncUnits( self, func):
        """Try to evaluate function func and obtain its units.
           NOTE: 't' or 'Dt' are taken as time variables, with the value of 1.
        """

        call = {}
        self.aux_symb_only = False
        for key in func.__code__.co_varnames:
            call[key] = self.V_TU(key)
        rt1 = func(**call)

        self.aux_symb_only = True
        for key in func.__code__.co_varnames:
            call[key] = self.V_TU(key)
        rt2 = func(**call)
        aux_symbols = set([call[key] for key in call.keys()])
                
        self.aux_symb_only = True
        for key in func.__code__.co_varnames:
            if key in [ 't', 'Dt']:
                call[key] = 1.0
            else:
                call[key] = self.V(key)
        
        ### Evaluate sympy functions
        ### If there are no sympy functions, func(**call) is a number
        ### This will also return the number:
        rt3 = simplify(func(**call)).evalf() 
                
        units = simplify(rt1/rt2)
        ### If there are free aux simbols then:
        print( "Function %s:" % (func.__name__,))
        if aux_symbols.intersection(units.free_symbols) != set():
            print("WARNING: seemingly inconmensurable units !")
        print( "Value:", str_ScientificNotation(rt3), " Units:", units, "\n")

    def TU_IA_test( self, func_names=[]):
        """DOES NOT WORK
        Interactively try to obtain the units of expressions for
           already defined Vars.
           NOTE: 't' or 'Dt' are taken as time variables, with the value of 1.
           NOTE: This should be called with the sympy version of math/numpy
           functions like exp, log etc. ie, call first:
           from sympy import exp, log, ... etc
        """
        expr = "expr"
        self.aux_symb_only = False
        aux_and_symb = ""
        for key in list(self.mod.D.Vars.keys()) + ['t','Dt']:
            aux_and_symb += key + "=" + self.V_TU(key).__str__() + ","
        aux_and_symb = aux_and_symb[:-1] ## Remove the last comma
        self.aux_symb_only = True
        aux_symb = ""
        aux_symbols = set() ## aux symbols, start with empty set
        for key in list(self.mod.D.Vars.keys()) + ['t','Dt']:
            aux_symb += key + "=" + self.V_TU(key).__str__() + ","
            aux_symbols.add(self.V_TU(key)) ## To make a set of all aux symbols
        aux_symb  = aux_symb[:-1] ## Remove the last comma
        numbers = ""
        for key in self.mod.D.Vars.keys():
            numbers += key + "=" + self.V(key).__str__() + ","
        ### Add the time
        numbers += " t=1.0, Dt=1.0"
        
        print("(lambda %s: %s )" % ( aux_and_symb, expr))
        print("(lambda %s: %s )" % ( aux_symb, expr))
        print("(lambda %s: %s )" % ( numbers, expr))

        globals()['ModMod_rt'] = [0,1,2]
        print("Type 'exit' to finish.\nType TU: import func")
        print("to import a function from sympy and numpy.")
        print("NOTE: 't' or 'Dt' are taken as time variables, with the value of 1.")
        expr = ' '
        while True:
            expr = input('TU: ')
            if expr == 'exit':
                break
            try: ### Here we only form the expresions for functions to evaluate
                exec( "ModMod_rt[0] = (lambda %s: %s )" % ( aux_and_symb, expr))
                exec( "ModMod_rt[1] = (lambda %s: %s )" % ( aux_symb, expr))
                exec( "ModMod_rt[2] = (lambda %s: %s )" % ( numbers, expr))
                f1, f2, f3 = globals()['ModMod_rt'] ##Retrive the expressions
                rt1 = f1() ### An then evaluate them
                rt2 = f2()
                rt3 = f3()
            except:
                print("Error:", exc_info()[0])
                continue
            units = simplify(rt1/rt2)
            ### Evaluate sympy functions
            ### If there are no sympy functions, rt3 is a number
            ### This will also return the number:
            value = simplify(rt3).evalf()
            ### If there are free aux simbols then:
            if aux_symbols.intersection(units.free_symbols) != set():
                print("WARNING: seemingly inconmensurable units !")
            print( "Value:", str_ScientificNotation(value), " Units:", units)

    
    def TU_IA( self, func_names=[]):
        """Interactively try to obtain the units of expressions for
           already defined Vars.
           NOTE: 't' or 'Dt' are taken as time variables, with the value of 1.
           NOTE: This should be called with the sympy version of math/numpy
           functions like exp, log etc. ie, call first:
           from sympy import exp, log, ... etc
        """
        self.aux_symb_only = False
        locs_aux_and_symb = {}
        for key in list(self.mod.D.Vars.keys()) + ['t','Dt']:
            locs_aux_and_symb[key] = self.V_TU(key)
        self.aux_symb_only = True
        locs_symb = {}
        for key in list(self.mod.D.Vars.keys()) + ['t','Dt']:
            locs_symb[key] = self.V_TU(key)
        aux_symbols = set([locs_symb[key] for key in locs_symb.keys()])

        locs_numbers = {}
        for key in self.mod.D.Vars.keys():
            locs_numbers[key] = self.V(key)
        for key in ['t','Dt']: ### Add the time
            locs_numbers[key] = 1.0
        
        globals()['ModMod_rt'] = [0,1,2]
        print("Type 'exit' to finish.\nType TU: import func")
        print("to import a function from sympy and numpy.")
        print("NOTE: 't' or 'Dt' are taken as time variables, with the value of 1.")
        expr = ' '
        while True:
            expr = input('TU: ')
            if expr == 'exit':
                break
            try:
                exec( 'ModMod_rt[0] = %s' % expr, globals(), locs_aux_and_symb)
                exec( 'ModMod_rt[1] = %s' % expr, globals(), locs_symb)
                exec( 'ModMod_rt[2] = %s' % expr, globals(), locs_numbers)
                rt1, rt2, rt3 = globals()['ModMod_rt']
            except:
                print("Error:", exc_info()[0])
                continue
            units = simplify(rt1/rt2)
            ### Evaluate sympy functions
            ### If there are no sympy functions, rt3 is a number
            ### This will also return the number:
            value = simplify(rt3).evalf()
            ### If there are free aux simbols then:
            if aux_symbols.intersection(units.free_symbols) != set():
                print("WARNING: seemingly inconmensurable units !")
            print( "Value:", str_ScientificNotation(value), " Units:", units)

    def TestUnits( self, lhs, assigm=False):
        """Test the units of this RHS, with repsect to the lhs, either if ODE or assigment."""
        if assigm:
            lhs_units = self.mod.D.Vars[lhs].symb_units
            lhs_prn = self.mod.D.Vars[lhs].prn
            tp = "assigment"
        else:
            lhs_units = self.DerivativeUnits(lhs)
            lhs_prn = r"$\frac{d%s}{dt}$" % self.mod.D.Vars[lhs].prn
            tp = "ODE"
        rhs_units = self.GetUnits()
        print( "Units of %s:" % (lhs_prn,), lhs_units, ". Units for rhs:", rhs_units,\
              "(%s).  Equal:" % (tp,), lhs_units == rhs_units)
        kappa = simplify(rhs_units/lhs_units)
        if lhs_units != rhs_units:
            if kappa.free_symbols == set(): ## Empty set, no free symbols, the difference is a constant
                print("Conmensurable units, kappa= ", kappa)
            else:
                print("Inconmensurable units!!!!")
        return lhs_units, rhs_units, lhs_units == rhs_units, kappa

    def RHS( self, Dt):
        """RHS( Dt, k) = \kappa_1^{-1} F_1( t+Dt, X+k) where X is the current value of
           all state variables.  k is set in the module class.
           To access a state variable one **MOST** use self.Sk(varid).  One gets the state
           variable value + its corresponding k.
        """
        pass ## Templete class
        
class AssigmentRHS(StateRHS):
    def __init__(self, varid_rhs):
        """Simple assigment RHS."""
        super().__init__()
        self.varid_rhs
    def RHS( self, DT):
        return self.V(self.varid_rhs)
        
class Module:
    def __init__( self, Dt):
        """Template class, to represent a module of the general model.
           Delay the definition of the Director.
        """
        self.Dt = Dt #Time steping of module
        self.D = None ## Opened with no director, this is set later with SetDirector

        self.StateRHSs = {}
        self.S_RHS_ids = list(self.StateRHSs.keys())
        self.q = len(self.StateRHSs)
        ### This will hold the values of the state variables
        self.X = zeros(self.q)
        self.F = zeros(self.q)
        ### In the order of this list
        ### ie self.X[i] is the value of variable self.S_ids[i]
        ### This is only done  when steping in the RK method
        self.k = {} # Increment in evaluating RHS, see class StateRHS.RHS
        for varid in self.S_RHS_ids:
            self.k[varid] = 0.0
        ### List of asigment RHSs ... No ODE, only assigment to value at required time
        self.Assigm_StateRHSs = {}
        self.Assigm_S_RHS_ids = list(self.Assigm_StateRHSs.keys())
        self.Assigm_q = 0

    def SetDirector( self, Director):
        self.D = Director
        self.Init()
    
    def AddStateRHS( self, varid, rhs):
        """Adds an instance of a StateRHS to the list of RHSs."""
        self.StateRHSs[varid] = rhs #Add to the dictionary of StateRHSs
        rhs.SetModule(self) #Make StateRHS' modules this one
        self.q += 1
        self.X = zeros(self.q)
        self.F = zeros(self.q)
        self.S_RHS_ids = list(self.StateRHSs.keys())
        self.k[varid] = 0.0
   
    def AddAssigmentStateRHS( self, varid, rhs):
        """Adds an instance of an Assigment StateRHS to the list of RHSs. No ODE RHS"""
        self.Assigm_StateRHSs[varid] = rhs #Add to the dictionary of StateRHSs
        rhs.SetModule(self) #Make StateRHS' modules this one
        self.Assigm_q += 1
        self.Assigm_S_RHS_ids = list(self.Assigm_StateRHSs.keys())
   
    def Init(self):
        """Further initializations after the director has been set."""
        pass

    def t( self ):
        """Get the current time.  Short for:"""
        return self.D.t ### Shared time

    def V( self, varid):
        """Get value of variable.  Short for:"""
        return self.D.Vars[varid].val

    def V_Mean( self, varid):
        """Get mean value of variable.  Short for:"""
        return self.D.Vars[varid].Mean()

    def V_Set( self, varid, val):
        """Set value of variable.  Short for:"""
        self.D.Vars[varid].Set(val)

    def SetX(self):
        """Set the value of self.X: array of size q,
           with the values of state varibles in the order of self.S_ids.
        """
        for i, varid in enumerate(self.S_RHS_ids):
            self.X[i] = self.V(varid)
    
    def AddToX( self, k_vec):
        """Add k_vec to  self.X, and modify the corresponding
           state varibles, in the order of self.S_ids.
        """
        self.X += k_vec
        for i, varid in enumerate(self.S_RHS_ids):
            self.D.Vars[varid].Set(self.X[i])  
    
    def RHS_TestUnits( self ):
        """Calls each of the StateRHS's RHS_TestUnits,  The k vector is 0.0.
           Then F( t+Dt, X) where X is the current value of all module's state variables.
           The same happens with assigment RHSs.
           Prints the results.
        """
        rt = [[ 0, 1, 2, 3]]*(len(self.S_RHS_ids)+len(self.Assigm_S_RHS_ids))
        print("\n")
        for i, varid in enumerate(self.S_RHS_ids):
            rt[i] = self.StateRHSs[varid].TestUnits( varid, assigm=False)
        for j, varid in enumerate(self.Assigm_S_RHS_ids):
            rt[i+j] = self.StateRHSs[varid].TestUnits( varid, assigm=True)
        print("\n")
        return rt

    def RHS( self, k_vec, Dt):
        """Calls each of the StateRHS to form the vector:
           RHS( Dt, k) = \kappa^{-1} F( t+Dt, X+k) where X is the current value of
           all module's state variables.
           k_vec is an array of size q, with the shift values of state varibles
           in the order of self.S_ids.
        """
        for i, varid in enumerate(self.S_RHS_ids):
            self.k[varid] = k_vec[i]
        for i, varid in enumerate(self.S_RHS_ids):
            self.F[i] = self.StateRHSs[varid].RHS(Dt)
        return self.F

    def EvaluateRHS( self, X, t):
        """Evaluate the RHS in X and t.  The above RHS is rather used for Runge-Kutta,
           but this one could be used (slow) to use in odeint for example.
        """
        for i, varid in enumerate(self.S_RHS_ids):
            self.V(varid).Set(X[i])
        for i, varid in enumerate(self.S_RHS_ids):
            self.k[varid] = 0.0
        for i, varid in enumerate(self.S_RHS_ids):
            self.F[i] = self.StateRHSs[varid].RHS( t-self.t() )
        return self.F        
        

    def AdvanceRungeKutta( self, t1, Method=4):
        """
        Rugge-Kutta type ODE solver, of dX/dt = F( X, t, args), X(t0) = X0 (array length q)
        Solution for X(t1).  The time step to be use is less but as close as possible
        to self.Dt.
       
        F is the self.RHS method, X0 is the current state variable values.

        Method=0, is the Euler Method (Ord=1),
        Method=2 is the midpoint RK2 method (Ord=2),
        Method=3 is the RK4 classic method (Ord=4),
        Method=4 is Cash-Karp RK45, with error estimation (Ord=4).

        If the method has error estimation, returns a len(grid) $\times$ q array
        with the X's and a len(grid) array with global error estimates at each node.
        If the method has no error estimates the second item = None.
      
        The whole methods description may be seen in RungueKutta.RKcoef .
        """

        self.SetX() # Set the initial value (current) of state variables

        ### This creates a set of times knots, that terminates in t1 with
        ### step = self.Dt
        tt = append( arange( self.t(), t1, step=self.Dt), [t1])
        
        n = len(tt)  ### Number of time steps
    
        # self.q  ##Dimension of state variables
        k = zeros((RKcoef[Method]['s'], self.q)) ##Size of the Butcher Tableau for the RK method
        tmp = zeros(self.q)
        tmp0 = zeros(self.q)
        # X, dont save intermidiate evaluations
        # self.X  ## Initial value
        if (RKcoef[Method]['ErrorEst']): #Error estimation
            E = zeros(self.q) ## Array to hold the estimated local truncation error, keep the last one only        
        for i in range( 1, n):
            h = tt[i]-tt[i-1]
            # This is F( X, tt[i] + h*RKcoef[Method]['c'][0]) 
            k[0,:] = self.RHS( tmp0, tt[i] + h*RKcoef[Method]['c'][0])
            for j in range( 1, RKcoef[Method]['s']):
                for l in range(self.q):
                    tmp[l] = sum(RKcoef[Method]['a'][j]*k[:j,l])
                # This is F( X + h*tmp, tt[i] + h*RKcoef[Method]['c'][j])
                k[j,:] = self.RHS( h*tmp, tt[i] + h*RKcoef[Method]['c'][j])
            for l in range(self.q):
                tmp[l] = sum(RKcoef[Method]['b']*k[:,l])
            # This is X += h*tmp
            self.AddToX(h*tmp)
            if (RKcoef[Method]['ErrorEst']): #Local Truncation error estimation at the time points
                for l in range(self.q):
                    tmp[l] = sum(RKcoef[Method]['E']*k[:,l])
                ### The local truncation error is h*tmp
                E += h*tmp ### We accumulate the sum of all the local truncation errors

        if (RKcoef[Method]['ErrorEst']):
            self.E = E
            return 1
        else:
            return 1

    def VarAssigment( self, varid, t1):
        """The RHS is called and F( t1, X) and assigned to the lhs."""
        self.D.Vars[varid].Set(self.Assigm_StateRHSs[varid].RHS(t1))
    
    def AdvanceAssigment( self, t1):
        for varid in self.Assigm_S_RHS_ids:
            self.VarAssigment( varid, t1)
        
    def Advance(self, t1):
        """Advance the module from the current time to time t1.
           Return 1 if succesful.
        """
        ### The order might be required differently
        self.AdvanceRungeKutta(t1)
        self.AdvanceAssigment(t1)


class ReadModule(Module):
    def __init__( self, fnam, t_conv_shift, t_conv):
        """Read the Excel file fnam to update a series a Var's accordingly."""

        ### Dt is ignored
        super().__init__( Dt=0.0 )
        
        ### The sheet 'InputVars' contains the information of which variable to update and how
        self.input_vars = read_excel( fnam, ['InputVars'])['InputVars'].set_index('Var', drop=False)
        ### List of data sheet needed
        sheet_list = list(self.input_vars['Sheet'].unique())
        ### Read the rest of the data
        self.data = read_excel( fnam, sheet_list)
        ### This is the list of Var ids to be updated
        self.Assigm_S_RHS_ids = list(self.input_vars['Var'])
        ### Add a column with the current read row number of each variable
        self.input_vars['time_index'] = [0]*len(self.Assigm_S_RHS_ids)
        ### How to convert the data base time to the Director units
        self.tconv_a = t_conv_shift
        self.tconv = t_conv
    
    def GetTime( self, vid, s=0):
        """Get the current time if variable vid, for row self.input_vars.loc[vid,'time_index'] + s,
           in the Director units."""
        try:
            traw = self.data[self.input_vars.loc[vid,'Sheet']].loc[ self.input_vars.loc[vid,'time_index']+s,\
                       self.input_vars.loc[vid,'Time_column']]
        except:
            print("ModMod:ReadModule: time %f beyond data base!")
            raise
        return self.tconv*(self.input_vars.loc[vid,'Time_conv']*(traw - self.input_vars.loc[vid,'Time_conv_shift']) - self.tconv_a)
    
    def GetVal( self, vid, s=0):
        """Get the current value, for row self.input_vars.loc[vid,'time_index'] + s,
           in the Director units."""
        vraw = self.data[self.input_vars.loc[vid,'Sheet']].loc[ self.input_vars.loc[vid,'time_index']+s,\
                       self.input_vars.loc[vid,'Column']]
        return self.input_vars.loc[vid,'Column_conv']*(vraw - self.input_vars.loc[vid,'Column_conv_shift'])
    
    def Advance(self, t1):
        """Update variables to the reading at time t1, interpolate inbetween readings in the data base.
           Readings most be called for incremeting the time only."""
        for vid in self.Assigm_S_RHS_ids:
            tk = self.GetTime(vid)
            while tk <= t1:
                self.input_vars.loc[vid,'time_index'] += 1 ##Next row
                tk = self.GetTime(vid)
            tk_1 = self.GetTime(vid, s=-1)
            vk_1 = self.GetVal(vid, s=-1)
            vk = self.GetVal(vid)
            self.D.Vars[vid].Set( vk_1 + (t1-tk_1)*((vk-vk_1)/(tk-tk_1)) )
        return 1


class Director:
    def __init__( self, t0, time_unit, Vars, Modules, units_symb=True):
        """Holds all variables and runs iterations in modules with the Scheduler.
           t0, initial time. State and Cnts dictionary of Var's, Modules dictionary of
           Modules."""
        self.t = t0 ### Time, shared by all modules
        self.AddTimeUnit( time_unit, units_symb)
        self.Vars = Vars #Dictionary of all variables, may be empty
        self.VarClas = {'Cnts':[], 'State':[]} # Variable classification, start with the special names 'Cnts' and 'State'
        for ky in self.Vars.keys():
            typ = self.Vars[ky].typ
            if not(typ in self.VarClas.keys()): # New type
                self.VarClas[typ] = [ky]
            else:
                self.VarClas[typ] += [ky] # Add variable to type
        self.glob_list = []
        self.local_list = []
            
        self.Modules = Modules #List of Modules, add modules with AddModule

    def AddTimeUnit( self, time_unit, symb_unit=True):
        """Add time unit to Director, symb_unit=True if sympy object."""
        if symb_unit:
            self.symb_time_unit = time_unit
            self.time_unit = '$'+latex( time_unit)+'$'
        else:
            self.time_unit = time_unit
            self.symb_time_unit = None

    def CheckSymbTimeUnits(self, Dir):
        """"Check that the SymbTimeUnits of another directory are the same,
            return the symb_time_unit.
            Raise error if not.
        """
        if self.symb_time_unit != Dir.symb_time_unit:
            raise Exception('VarNotEqual')
            return False
        else:
            return self.symb_time_unit
    
    def AddVar( self, typ, varid, desc, units, val, rec=1, prn=None, prnpres=4):
        """Adds a (global) variable:
           It will create the object Var, the rest of pars are passed to Var to create the Var instance.
        """
        if varid in self.Vars.keys():
            raise ValueError("Director: Var '%s' previously defined." % (varid,))
        for mod_key in self.Modules.keys():
            try:
                if varid in self.Modules[mod_key].Vars.keys(): # Works if mod is a slave Director taken as a module
                    raise ValueError("Director: Var '%s' previously defined in Module: %s." % (varid,self.Modules[mod_key].name))
            except AttributeError: ## mod is in fact a Module, does not have mod.Vars
                continue ### Do nothing
        ### Add the variable
        self.Vars[varid] = Var( typ, varid, desc, units, val, rec=rec, prn=prn, prnpres=prnpres)
        if not(typ in self.VarClas.keys()):
            self.VarClas[typ] = [varid]
        else:
            self.VarClas[typ] += [varid]
        self.glob_list += [varid] # Add to the list of global variables
        
    def AddVarLocal( self, typ, varid, desc, units, val, rec=1, prn=None, prnpres=4):
        """Adds a local variable:
           It will create the object Var, the rest of pars are passed to Var to create the Var instance.
        """
        if varid in self.Vars.keys():
            raise ValueError("Director: Var '%s' previously defined." % (varid,))
        for mod_key in self.Modules.keys():
            try:
                if varid in self.Modules[mod_key].Vars.keys(): # Works if mod is a slave Director taken as a module
                    raise ValueError("Director: Var '%s' previously defined in Module: %s." % (varid,self.Modules[mod_key].name))
            except AttributeError: ## mod is in fact a Module, does not have mod.Vars
                continue ### Do nothing
        ### Add the variable
        self.Vars[varid] = Var( typ, varid, desc, units, val, rec=rec, prn=prn, prnpres=prnpres)
        if not(typ in self.VarClas.keys()):
            self.VarClas[typ] = [varid]
        else:
            self.VarClas[typ] += [varid]
        self.local_list += [varid] # Add to the list of local variables
        
    def AddModule( self, modid, mod):
        """Adds an instance of a module to the list of modules."""
        self.Modules[modid] = mod #Add to the dictionary of Modules
        mod.SetDirector(self) #Make module' director this one, same interface
        
    def MergeVarsFromRHSs( self, RHS_list, call=None):
        """Marges ALL Vars from the list (or one) RHS_list instance(s)."""
        if not(isinstance( RHS_list, list)):
            RHS_list = [RHS_list]
        self.MergeVars( [rhs.GetDirector() for rhs in RHS_list], all_vars=True, call=call)
        return 1
    
    def MergeVars( self, Dir_list, all_vars=False, call=None):
        """Marge all the GLOBAL variables from the Director list Dir_list.
           MERGE ONLY GLOBAL Vars from the key list Dir.glob_list
           (Dir_list may also be just one Director instance).
           
           all_vars=True is used to Merge RHSs only.  Then all Vars are merged.
           
           But raise and error if a Dir defines a glocal Var that is a local Var
           in another Director.  This is dangerous since defining this global Var will
           override any local Var
        
           If variable already exists it most have an equal definition.
           This is normally done at intialization when marging variables from
           several modules.
           
           Put call=__name__ ... only when __name__=="__main__" merging information is printed
           Debugging is done pregressively, so this info should be only necessary in the
           current level being executed.
        """
        if call == None: # No info if it's being executed from main or as an import
            prn = False
        if call == "__main__":
            prn = True # Print info if excuted as main
            print("Director: MergeVars:")
        else:
            prn = False
        if not(isinstance( Dir_list, list)):
            Dir_list = [Dir_list]
        empty_set = set()
        
        vars_origin = {} ## Empty doctionary, to keep track of where each var came from
        for i,Dir in enumerate(Dir_list):
            ### Check if Dir's list of local variables IS NOT defined in the
            ### list of Global variables in other Dir's
            ### ie A local variable most not be defined globally elsewhere.
            for j,Dir2 in enumerate(Dir_list):
                if set(Dir.local_list).intersection(Dir2.glob_list) != empty_set:
                    raise ValueError("Director.MergeVars: GlobalLocal: local Vars of Dir %d defined globally in Dir %d." % ( i, j),\
                         Dir.local_list, " intersects with ", Dir2.glob_list, " = ", set(Dir.local_list).intersection(Dir2.glob_list))
                if i != j:
                    ### Raise an error if repeated local variables are defined as Cnts
                    ### ie shared constant 'Cnts' variables most not be defined locally (!!!):
                    for key in set(Dir.local_list).intersection(Dir2.local_list):
                        if key in Dir.VarClas['Cnts']:
                            raise ValueError("Director.MergeVars: LocalCnts: local 'Cnts' Var '%s' of Dir %d also defined locally in Dir %d." % ( key, i, j))
                    ### THEREFORE: If there is an intersection in local Vars this
                    ### cannot be constants 'Cnts'
            ### Now add Dir global (or all) variables to the this director
            if all_vars:
                var_list = Dir.Vars.keys()
                ins = "RHS"
            else:
                var_list = Dir.glob_list
                ins = "Dir"
            for key in list(var_list):
                if prn:
                    print("%s %d Var '%s': " % ( ins, i,key), end='')
                if key in self.Vars.keys(): # Var already added in this director
                    ### Check if same definition:
                    if self.Vars[key].EqualDef(Dir.Vars[key]):
                        if key in list(vars_origin.keys()):
                            vars_origin[key] += [i] # Keep track of where it is defined
                        else:
                            vars_origin[key]  = [i]
                        ## Delete repeated Var.
                        del Dir.Vars[key]
                        ## Make this key point to the unique var in director:
                        ## NOTE: the (slave) Dir now uses the unique Var 
                        Dir.Vars[key] = self.Vars[key]
                        if prn:
                            print("repeated, check ok.")
                    else:
                        raise ValueError("Director.MergeVars: VarNotEqual: %s %d Var '%s' not equal definition in %s's:"\
                                         % ( ins, i, key, ins), vars_origin[key])
                else: ## New var, add it
                    vars_origin[key] = [i] # Keep track of where it is defined
                    self.Vars[key] = Dir.Vars[key]
                    ## If new type, add the type.
                    typ = self.Vars[key].typ
                    if not(typ in self.VarClas.keys()):
                        self.VarClas[typ] = [key]
                    else:
                        self.VarClas[typ] += [key]
                    if key in Dir.glob_list:
                        self.glob_list += [key] ### Add to list of global variables
                        if prn:
                            print("added to global Vars.")
                    else:
                        self.local_list += [key] ### otherwise add to the list of local variables
                        if prn:
                            print("added to local Vars.")
        return 1
    
    def V( self, varname):
        """Access to variable.
           NOTE, FOR GLOBAL VARS in a Slave Director:
           In a Slave Director self.Vars[varid] points to
           a Var instance used globally, when using MergeVars, while local Vars remain the same.
           Therefore we do not need to change the acces to Vars, either Slave or not Slave
           global or locals (!!).  This improves speed also.
        
           That is:
        """
        return self.Vars[varname].val

    def V_Set( self, varid, val):
        """Set value of variable.
           NOTE, FOR GLOBAL VARS in a Slave Director:
           In a Slave Director self.Vars[varid] points to
           a Var instance used globally, when using MergeVars, while local Vars remain the same.
           Therefore we do not need to change the acces to Vars, either Slave or not Slave
           global or locals (!!).  This improves speed also.
        
           That is:
        """
        return self.Vars[varid].Set(val)

    def PrintVars( self, sel=None):
        """Print variables by type, from the types in sel.
           if sel == None print all types.
        """
        print("Time= %f %s" % ( self.t, self.time_unit))
        if sel == None:
            sel = self.VarClas.keys()
        for typ in sel:
            print("%s:" % (typ,))
            for ky in self.VarClas[typ]: 
                print("%s = %s %s" % ( ky, self.Vars[ky].__str__(), self.Vars[ky].units))

    def Scheduler( self, t1, sch):
        """Advance the modules to time t1. sch is a list of modules id's to run
           its Advance method to time t1.
           
           Advance is the same interface, either if single module or list of modules.
        """
        
        for mod in sch:
            if self.Modules[mod].Advance(t1) != 1:
                print("Director: Error in Advancing Module '%s' from time %f to time %f" % ( mod, self.t, t1))
        self.t = t1
    
    def AddDirectorAsModule( self, modid, Dir):
        """Adds an instance of a Director, as if a module, to the list of **modules**,
           to be able to treat Director, with possible many modules, as one module.
           The only interface needed is Advance."""
        self.Modules[modid] = Dir #Add to the dictionary of Modules
        Dir.BecomeSlave( modid, self) #Make director a slave of this one, with name modid
    
    def BecomeSlave( self, slave_name, Dir):
        """Make this Director become a slave of master Director Dir.
           Aquire the name slave_name ."""
        self.master_dir = Dir
        self.name = slave_name
        
    
    def Advance( self, t1):
        """Polymorphic method to be able to treat a director, with possible many modules,
           as one module.
           
           This is basically a call to Scheduler( t1, self.sch) BUT:
              1) Change current time from master_dir time 
              2) do not update the time at the end.
           
           This is **only** used in Slave mode, when this director is under control of
           another director.  self.name and self.master_dir should have been defined
           in MakeSalve.
           
           Define the sheduling list self.sch previously:
        """
        self.t = self.master_dir.t  ##Will fail if not in master mode
        advances = list()
        for mod in self.sch:
            #breakpoint()
            advances.append(self.Modules[mod].Advance(t1))
            if all(advances) != True:
                print("Slave Dir %s: Error in Advancing Module '%s' from time %f to time %f"\
                      % ( self.name, mod, self.master_dir.t, t1))
                return 0
        return 1
        
    
    def VarToArray( self, ids):
        """Create an array of the values of the varid's in ids of the variable type typ.
           typ = 'State' or 'Cnts'.
                   """
        return array([self.Vars[varid].val for varid in ids])

    def Run( self, Dt, n, sch, save=None):
        """Advance in Dt time steps, n steps with the scheduling sch.
           Save the variables with varid's in save.  Defualt: all State variables.
        """
        if save == None:
            self.save = list(self.VarClas['State'])
        else:
            self.save = save
        trange = arange( self.t+Dt, self.t+(n+1)*Dt, step=Dt)
        self.Output = zeros(( n, 1+len(self.save)))
        self.Output[0,0] = self.t ## Initial time
        self.Output[0,1:] = self.VarToArray( self.save)
        for i, t1 in enumerate(trange):
            self.Scheduler(t1, sch)
            self.Output[i,0] = self.t
            self.Output[i,1:] = self.VarToArray( self.save)
        return self.save

    def PlotVar( self, varid):
        """Plot the results of Run for variable varid."""
        par = self.save.index(varid)
        plot( self.Output[:,0], self.Output[:,1+par], '-')
        title(self.Vars[self.save[par]].prn)
        xlabel(self.time_unit)
        ylabel(self.Vars[self.save[par]].units)
        
    def OutVar( self, varid):
        """
        Returns an array with the results of Run for variable varid.
        """
        par = self.save.index(varid)
        return self.Output[:,1+par]

class Struct():
    '''
    Structure object that helps to define a state/constant as global ModMod variable.
    '''
    def __init__(self, typ = '', varid = '', prn = '', desc = '', units = 1, val = 0, rec = 1, ok='No existe'):
        '''
        Recives all the necesary parameters for defining a ModMod variable. 
        Also you can add the status 'ok' of the variable.
        '''
        self.typ   = typ
        self.varid = varid
        self.prn   = prn
        self.desc  = desc 
        self.units = units
        self.val   = val     
        self.rec   = rec     
        self.ok    = ok

    def addvar_rhs(self, rhs, local=False):
        if local:
            rhs.AddVarLocal(typ=self.typ, varid=self.varid, prn=self.prn, desc=self.desc, units=self.units , val=self.val, rec=self.rec)
        else:
            rhs.AddVar(typ=self.typ, varid=self.varid, prn=self.prn, desc=self.desc, units=self.units , val=self.val, rec=self.rec)


    def addvar_dir(self, dir):
        self.addvar_rhs(dir)

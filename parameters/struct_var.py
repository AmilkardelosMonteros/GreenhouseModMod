class Struct():
    def __init__(self, typ = '', varid = '', prn = '', desc = '', units = 1, val = 0, rec = 1, ok='No existe'):
        self.typ   = typ
        self.varid = varid
        self.prn   = prn
        self.desc  = desc 
        self.units = units
        self.val   = val     
        self.rec   = rec     
        self.ok    = ok

    def addvar_rhs(self, rhs):
        rhs.AddVar(typ=self.typ, varid=self.varid, prn=self.prn, desc=self.desc, units=self.units , val=self.val, rec=self.rec)

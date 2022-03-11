from pandas import read_excel
from ModMod import Module

class ReadModule(Module):
    def __init__( self, fnam, t_conv_shift, t_conv, shift_time = 0):
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
        self.shift_time = shift_time

    
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
        vraw = self.data[self.input_vars.loc[vid,'Sheet']].loc[ self.input_vars.loc[vid,'time_index']+ s + self.shift_time,\
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
            
            tk_1 = self.GetTime(vid, s=-1 )
            vk_1 = self.GetVal(vid, s=-1)
            vk = self.GetVal(vid)
            self.D.Vars[vid].Set( vk_1 + (t1-tk_1)*((vk-vk_1)/(tk-tk_1)) )
        return 1

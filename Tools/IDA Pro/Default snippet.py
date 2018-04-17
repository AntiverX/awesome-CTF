import ida_idd,idc,ida_dbg

def go():
    run_to(0x76794cf6)
    
def gogo():
    t = ida_idd.regval_t()
    t.set_int(0x76794cfa)
    ida_dbg.set_reg_val("PC",t)
while get_reg_value("R7") < 9:
    go()
    GetDebuggerEvent(WFNE_SUSP, -1)
    print hex(idc.get_reg_value("R1"))+" "+hex(idc.get_reg_value("R4"))+"|"+hex(idc.get_reg_value("R1")+10)+" "+hex(idc.get_reg_value("R2"))
    gogo()

print "___"



__author__ =  'Jon K Peck'
__version__=  '1.0.0'

# history
# 09-11-2023 original version
import spss, spssaux
from extension import Template, Syntax, processcmd
import re

# debugging
        # makes debug apply only to the current thread
try:
    import wingdbstub
    import threading
    wingdbstub.Ensure()
    wingdbstub.debugger.SetDebugThreads({threading.get_ident(): 1})
except:
    pass
        
def update(updatesource, idvars, sourceind="", mapx=False):
    """Apply the SPSS UPDATE command to the active dataset"""
    
    # clean up updatesource, which may look like "filespec[datasetname]" due to a CDB bug
    extracted = re.search(r"\[(.*?)\]$", updatesource)
    if extracted:
        updatesource = extracted.group(1)   # take just the contents of the brackets
    if spss.ActiveDataset().lower() == updatesource.lower():
        raise ValueError(_("The active dataset cannot also be the update source"))
    idvars = ' '.join(idvars)
    sourceind = f"/IN={sourceind}" if sourceind else ""
    mapx = "/MAP" if mapx else ""
        
    cmd = f"""UPDATE FILE=* /FILE="{updatesource}" {sourceind}
    /BY {idvars} {mapx}."""
    spss.Submit(cmd)
 
def Run(args):
    """Execute the STATS UPDATE extension command"""
    # This syntax maps to the SPSS UPDATE command, but it can't be
    # the same, because extension XML does not permit anonymous parameters
    # on a subcommand

    args = args[list(args.keys())[0]]
    ###print args   #debug

    oobj = Syntax([
        Template("UPDATESOURCE", subc="",  ktype="literal", var="updatesource", islist=False),
        Template("IDVARS", subc="", ktype="existingvarlist", var="idvars", islist=True), 
        Template("SOURCEIND", subc="", ktype="varname", var="sourceind"),
        Template("MAP", subc="", ktype="bool", var="mapx"),
        
        Template("HELP", subc="", ktype="bool")])
    
    # A HELP subcommand overrides all else
    if "HELP" in args:
        #print helptext
        helper()
    else:
        processcmd(oobj, args, update)

def helper():
    """open html help in default browser window
    
    The location is computed from the current module name"""
    
    import webbrowser, os.path
    
    path = os.path.splitext(__file__)[0]
    helpspec = "file://" + path + os.path.sep + \
         "markdown.html"
    
    # webbrowser.open seems not to work well
    browser = webbrowser.get()
    if not browser.open_new(helpspec):
        print(("Help file not found:" + helpspec))
try:    #override
    from extension import helper
except:
    pass
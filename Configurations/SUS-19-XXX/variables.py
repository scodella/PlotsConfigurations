# variables
    
# Flags  
gv  = ' [GeV]'
pt  = '#font[50]{p}_{T}'
met = pt+'^{miss}'
sll = '#font[12]{ll}'
pll = '('+sll+')'
mt2 = '#font[50]{m}_{T2}'

# Complex variables

nbjets = '2*(trailingPtTagged>=20.)+(leadingPtTagged>=20. && trailingPtTagged<20.)'

# variables = {}

if 'Preselection' in opt.tag:

    variables['ptmiss']        = {  'name'  : 'ptmiss',                #   variable name    
                                    'range' : (  40,    0.,  400.),    #   variable range
                                    'xaxis' : met + gv,                #   x axis name
                                    'fold'  : 1                        #   fold overflow
                                }
    
    variables['njets']         = {  'name'  : 'nJet',                  #   variable name    
                                    'range' : (  6,    0.,     6.),    #   variable range
                                    'xaxis' : 'number of jets',        #   x axis name
                                    'fold'  : 1                        #   fold overflow
                                }
    
    variables['nbjets']        = {  'name'  : nbjets,                    #   variable name    
                                    'range' : (  3,    0.,     3.),      #   variable range
                                    'xaxis' : 'number of b-tagged jets', #   x axis name
                                    'fold'  : 1                          #   fold overflow
                                }
    
    variables['mt2ll']         = {   'name'  : 'mt2ll',                #   variable name    
                                     'range' : (  20,    0.,  200.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }
    
    variables['jetpt']         = {   'name'  : 'CleanJet_pt',          #   variable name    
                                     'range' : (  40,    0.,  200.),   #   variable range
                                     'xaxis' : 'jet ' + pt + gv,       #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }
    
    variables['Lep1pt']        = {   'name'  : 'Lepton_pt[0]',               #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'leading lepton ' + pt + gv,  #   x axis name
                                     'fold'  : 1                             #   fold overflow
                                 }
    
    variables['Lep2pt']        = {   'name'  : 'Lepton_pt[1]',               #   variable name    
                                     'range' : (  40,    0.,  200.),         #   variable range
                                     'xaxis' : 'trailing lepton ' + pt + gv, #   x axis name
                                     'fold'  : 1                             #   fold overflow
                                 }

if 'Validation' in opt.tag or 'Signal' in opt.tag:
    
    variables['mt2ll']         = {   'name'  : 'mt2ll',                #   variable name    
                                     'range' : (   7,    0.,  140.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }
    
    variables['mt2llgen']      = {   'name'  : 'mt2llgen',             #   variable name    
                                     'range' : (   7,    0.,  140.),   #   variable range
                                     'xaxis' : mt2 + pll + gv,         #   x axis name
                                     'fold'  : 1                       #   fold overflow
                                 }



# plot configuration
if opt.lumi>100: lumi_i=int(round(opt.lumi, 0))
else           : lumi_i=round(opt.lumi, 1)
#legend['lumi'] = 'L = '+str(lumi_i)+'/fb'
legend['lumi'] = str(lumi_i)+' fb^{-1} '
legend['sqrt'] = '#sqrt{s} = 13 TeV'

sl  = '#font[12]{l}'
sllatex = '\\font[12]{l}'

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:

    groupPlot['ttbar']  = {
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'isSignal' : 0,
        'color': 400,   # kYellow
        'samples'  : ['ttbar'] 
    }

    groupPlot['WW']  = {
        'nameHR' : 'WW',
        'nameLatex' : '\\WW',
        'isSignal' : 0,
        'color': 851,    # kAzure-9
        'samples'  : ['WW'] 
    }

    groupPlot['tW']  = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'isSignal' : 0,
        'color': 403,   # kYellow+3
        'samples'  : ['STtW', 'tW'] 
    }

    groupPlot['DY']  = {
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'isSignal' : 0,
        'color': 418,    # kGreen+2
        'samples'  : ['DY'] 
    }

    groupPlot['EOYDrellYan']  = {
        'nameHR' : 'EOY Drell-Yan',
        'nameLatex' : 'EOY \\DY',
        'isSignal' : 0,
        #'color': 418,    # kGreen+2
        'color' : '#94a4a2',
        'fill' : 3005,
        'samples'  : ['EOYDrellYan']
    }

    groupPlot['WZremove']  = {
        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',
        #'nameHR' : 'WZ (#rightarrow 3#ell)',
        'nameLatex' : '\\WZ ($\\to 3\\ell\\nu$)',
        'isSignal' : 0,
        'color': 798,    # kOrange-2
        'samples'  : ['WZ']
    }

    groupPlot['ZZ']  = {
        'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
        'nameLatex' : '\\ZZ ($\\to 2\\ell 2\\nu$)',
        'isSignal' : 0,
        'color': 803,   # kOrange+3
        'samples'  : ['ZZTo2L2Nu', 'ZZ'] 
    }

    groupPlot['ttZ']  = {
        'nameHR' : 't#bar{t}Z',
        'nameLatex' : '\\ttZ',
        'isSignal' : 0,
        'color': 802,   # kOrange+2
        'samples'  : ['ttZ'] 
    }

    groupPlot['WZ']  = {
        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',
        #'nameHR' : 'WZ (#rightarrow 3#ell)',
        'nameLatex' : '\\WZ ($\\to 3\\ell\\nu$)',
        'isSignal' : 0,
        'color': 798,    # kOrange-2
        'samples'  : ['WZ'] 
    }

    groupPlot['DYremove']  = {
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'isSignal' : 0,
        'color': 418,    # kGreen+2
        'samples'  : ['DY']
    }
     
    groupPlot['EOYVZ']  = {
        'nameHR' : 'EOY WZ+ggZZ',
        'nameLatex' : 'EOY WZ+ggZZ',
        'isSignal' : 0,
        'color': 798,    # kOrange-2
        'fill' : 3005,
        'samples'  : ['EOYVZ']
    }

    useOthers = True
    ttWOthers = True and useOthers and 'Other' not in opt.tag
    if useOthers:
      groupPlot['Others']  = {  
          'nameHR' : 'Other bkg.',
          'isSignal' : 0,
          'color': 394, #  kYellow-6
          'samples'  : ['VVV', 'Higgs', 'VZ', 'HWW', 'minor' ]
      }
      if ttWOthers: groupPlot['Others']['samples'].append('ttW')
    else:
      groupPlot['VZ'] = {
        'nameHR' : 'VZ (#rightarrow 2' + sl + '2q)',
        'nameLatex' : '\\VZ ($\\to 2\\ell 2\\Pq$)',
        'color'    : 7, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'samples'  : ['VZ' ],
        'scale'    : 1.0
      }
      groupPlot['VVV'] = {
        'nameHR' : 'VVV',
        'nameLatex' : '\\VVV',
        'color'    : 424, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'samples'  : ['VVV' ],
        'scale'    : 1.0
      }
      groupPlot['Higgs'] = {
        'nameHR' : 'H #rightarrow WW/#tau#tau',
        'nameLatex' : '$\\PH\\to \\WW /\\tautau$',
        'color'    : 434, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'samples'  : ['Higgs' ],
        'scale'    : 1.0
      } 
    if not ttWOthers:
      groupPlot['ttW'] = {
        'nameHR' : 't#bar{t}W',
        'nameLatex' : '\\ttW',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'samples'  : ['ttW' ],
        'scale'    : 1.0
      }
    
    groupPlot['EOYOthers']  = {
        'nameHR' : 'EOY Minor bkg.',
        'isSignal' : 0,
        'color': 394, #  kYellow-6
        'fill' : 3005,
        'samples'  : ['EOYQQ', 'EOYH', 'EOY3V' ]
    }
  
    groupPlot['ZZTo4L'] = {
        'nameHR' : 'ZZ (#rightarrow 4' + sl +')',
        'nameLatex' : '\\ZZ ($\\to 4\\ell$)',
        'isSignal' : 0,
        'color': 49,
        'samples' : ['ZZTo4L']
    }

    groupPlot['EOYZZTo4L'] = {
        'nameHR' : 'EOY ZZ (#rightarrow 4' + sl +')',
        'nameLatex' : 'EOY \\ZZ ($\\to 4\\ell$)',
        'isSignal' : 0,
        'color': 49,
        'fill' : 3005,
        'samples' : ['EOYZZ4L']
    }

    if 'SameSignValidationRegionX' in opt.tag:

        groupPlot['ttSemilep']  = {
            'nameHR' : 't#bar{t} Semilep.',
            'nameLatex' : '\\ttbar Semilep.',
            'isSignal' : 0,
            'color': 401,   # kYellow+1
            'samples'  : ['ttSemilep'] 
        }

        groupPlot['ttbar']['nameHR'] += ' Dilep.'
        groupPlot['ttbar']['nameLatex'] += ' Dilep.'
 
    else:

        groupPlot['ttbar']['samples'].extend(['ttSemilep'])

    groupPlot[nameWJets]  = {
        'nameHR' : 'W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : '\\PW+jets ($\\to\\ell\\nu$)',
        'isSignal' : 0,
        'color': 38,
        'samples'  : [nameWJets]
    }

    groupPlot['WJetsPrompt']  = {
        'nameHR' : 'W+jets prompt',
        'nameLatex' : '\\PW+jets prompt',
        'isSignal' : 0,
        'color': 38,
        'samples'  : ['WJetsPrompt']
    }

    groupPlot['WJetsFake']  = {
        'nameHR' : 'W+jets fake',
        'nameLatex' : '\\PW+jets fake',
        'isSignal' : 0,
        'color': 39,
        'samples'  : ['WJetsFake']
    }

    groupPlot['EOYWJets']  = {
        'nameHR' : 'EOY W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : 'EOY \\PW+jets ($\\to\\ell\\nu$)',
        'isSignal' : 0,
        'color': 38,
        'fill' : 3005,
        'samples'  : ['EOYWJets']
    }

#plot = {}

# keys here must match keys in samples.py    
#                    

if 'SM' in opt.sigset or 'Backgrounds' in opt.sigset:
    
    plot['DY']  = {  
        'nameHR' : 'Drell-Yan',
        'nameLatex' : '\\DY',
        'color': 418,    # kGreen+2
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.   ,
    }
    
    plot['ZZTo2L2Nu'] = { 
        'nameHR' : 'ZZ (#rightarrow 2' + sl + '2#nu)',
        'nameLatex' : '\\ZZ ($\\to 2\\ell 2\\nu$)',
        'color'    : 803,   # kOrange+3
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['ttZ'] = { 
        'nameHR' : 't#bar{t}Z',
        'nameLatex' : '\\ttZ',
        'color'    : 802,   # kOrange+2
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['WZ']  = {
        'nameHR' : 'WZ (#rightarrow 3' + sl + ')',  
        'nameLatex' : '\\WZ ($\\to 3\\ell\\nu$)',
        'color': 798,    # kOrange-2
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0 #1.045 #1.0052546#1.1133904#1.0176622                 
    }
    
    plot['WW']  = {  
        'nameHR' : 'WW',
        'nameLatex' : '\\WW',
        'color': 851,    # kAzure-9
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0                  
    }
    
    plot['STtW'] = {
        'nameHR' : 'tW',
        'nameLatex' : '\\tW',
        'color': 403,   # kYellow+3
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttbar'] = {   
        'nameHR' : 't#bar{t}',
        'nameLatex' : '\\ttbar',
        'color': 400,   # kYellow
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttSemilep'] = {   
        'nameHR' : 't#bar{t} Semilep.',
        'nameLatex' : '\\ttbar Semilep.',
        'color': 401,   # kYellow+1
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
    
    plot['ttW'] = { 
        'nameHR' : 't#bar{t}W',
        'nameLatex' : '\\ttW',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
    
    plot['VZ'] = { 
        'nameHR' : 'VZ (#rightarrow 2' + sl + '2q)',
        'nameLatex' : '\\VZ ($\\to 2\\ell 2\\Pq$)',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }
        
    plot['VVV'] = { 
        'nameHR' : 'VVV',
        'nameLatex' : '\\VVV',   
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }

    plot['Higgs'] = { 
        'nameHR' : 'H #rightarrow WW/#tau#tau',
        'nameLatex' : '$\\PH\\to \\WW /\\tautau$',
        'color'    : 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0,
        'scale'    : 1.0
    }

    plot['ZZTo4L'] = {   
        'nameHR' : 'ZZ (#rightarrow 4' + sl +')',
        'nameLatex' : '\\ZZ ($\\to 4\ell$)',
        'color': 49,   
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    plot[nameWJets] = {
        'nameHR' : 'W+jets (#rightarrow ' + sl + '#nu)',
        'nameLatex' : '\\PW+jets ($\\to\\ell\\nu$)',
        'color': 38,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    plot['WJetsPrompt'] = {
        'nameHR' : 'W+jets prompt',
        'nameLatex' : '\\PW+jets prompt',
        'color': 38,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }
 
    plot['WJetsFake'] = {
        'nameHR' : 'W+jets fake',
        'nameLatex' : '\\PW+jets fake',
        'color': 39,
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    plot['minor']  = {
        'nameHR' : 'Minor bkg.',
        'nameLatex' : 'Minor bkg.',
        'color': 394, #  kYellow-6
        'isSignal' : 0,
        'isData'   : 0 ,
        'scale'    : 1.0
    }

    #if 'EOY' in opt.tag:
    plot['EOYZZ4L']       = plot['ZZTo4L'].copy()
    plot['EOYH']          = plot['Higgs'].copy()
    plot['EOYQQ']         = plot['VZ'].copy()
    plot['EOYGluGlu']     = plot['WW'].copy()
    plot['EOYVZ']         = plot['WZ'].copy()
    plot['EOYDrellYan']   = plot['DY'].copy()
    plot['EOY3V']         = plot['VVV'].copy()
    plot['EOYWJets']      = plot[nameWJets].copy()

    # Backward compatibility for background names
    plot['tW']  = plot['STtW']
    plot['ZZ']  = plot['ZZTo2L2Nu']
    plot['HWW'] = plot['Higgs']

sampleToRemoveFromPlot = [ ] 

for sample in plot:
    if sample not in samples:
        sampleToRemoveFromPlot.append(sample)

for sample in sampleToRemoveFromPlot:
    del plot[sample]

eosNameToFix = [ ]
for sample in plot:
    if 'EOY' in sample:
        eosNameToFix.append(sample)
for sample in eosNameToFix:
    plot[sample]['nameHR'] = 'EOY '+plot[sample]['nameHR']
    plot[sample]['nameLatex'] = 'EOY '+plot[sample]['nameLatex']

groupToRemoveFromPlot = [ ] 

for group in groupPlot:
    for sample in sampleToRemoveFromPlot:
        if sample in groupPlot[group]['samples']:
            groupPlot[group]['samples'].remove(sample)
    if len(groupPlot[group]['samples'])==0 or 'remove' in group:
        groupToRemoveFromPlot.append(group)
    
for group in groupToRemoveFromPlot:
    del groupPlot[group]

invertOrder = True
if invertOrder:
    groupPlot = collections.OrderedDict(reversed(groupPlot.items()))
    if 'ZZTo4L' in groupPlot:
        saveZZTo4L = groupPlot['ZZTo4L']
        del groupPlot['ZZTo4L']
        groupPlot['ZZTo4L'] = saveZZTo4L

paletteList = [ '#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581' ]

if hasattr(opt, 'paperStyle'):
    if opt.paperStyle:
        for igroup, group in enumerate(groupPlot):
            groupPlot[group]['color'] = paletteList[igroup]
        #groupPlot['ttbar']['color']  = '#3f90da'
        #groupPlot['WW']['color']     = '#ffa90e'
        #groupPlot['tW']['color']     = '#bd1f01'
        #groupPlot['DY']['color']     = '#94a4a2'
        #groupPlot['ZZ']['color']     = '#832db6'
        #groupPlot['ttZ']['color']    = '#a96b59'
        #groupPlot['WZ']['color']     = '#e76300'
        #groupPlot['Others']['color'] = '#b9ac70'
        #groupPlot['ZZTo4L']['color'] = '#717581'

if invertOrder:
    for crspec in [ 'WZtoWWVal', 'WZVal', 'ttZVal', 'ttZNorm' ]:
        if crspec in opt.tag:
            for bkspec in [ 'WZ', 'ttZ' ]:
                if bkspec in crspec:
                    saveG = groupPlot[bkspec]
                    del groupPlot[bkspec]
                    groupPlot[bkspec] = saveG

# data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    plot['DATA']  = { 
        'nameHR' : 'Data',
        'color': 1 ,  
        'isSignal' : 0,
        'isData'   : 1 ,
        #'isBlind'  : 1
    }

# Signal  

signalType = 3 if ('SM' in opt.sigset or 'Backgrounds' in opt.sigset) else 0

paperSignalColor = 616 #kMagenta #'#717581'
signalColor = paperSignalColor if (hasattr(opt, 'paperStyle') and opt.paperStyle) else 1 if (hasattr(opt, 'postFit') and opt.postFit=='n') else 880 # kViolet

LSP = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
CHR = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
CHP = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{+}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
CHM = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{-}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
STP = '#tilde{t}_{1}'
STB = "#bar{#kern[0.1]{"+STP+"}}"
SLE = '#tilde{#font[12]{l}}'

#signalColor = 2

for massPoint in samples:
    if samples[massPoint]['isSignal']:

        massPointName = massPoint.replace(massPoint.replace('EOY','').split('_')[0],'')
        if hasattr(opt, 'paperStyle') and opt.paperStyle:
            #massPointName = massPointName.replace('_mS-', 'm_{'+STP+'}=').replace('_mC-', 'm_{'+CHR+'}=').replace('_mX-', 'GeV m_{'+LSP+'}=')+'GeV'
            massPointName = massPointName.replace('_mS-', '($m_{\\text{'+STP+'}}=').replace('_mC-', '($m_{\\text{'+CHR+'}}=').replace('_mX-', 'GeV$ m_{'+LSP+'}=')+'GeV)'
            mX = massPoint.split('_mX-')[1]
            if '_mS-' in massPoint:
                mS = massPoint.split('_mS-')[1].split('_')[0]
                massPointName = STP+'#kern[0.15]{'+STB+'},#kern[1.2]{'+STP+'}#kern[0.3]{#rightarrow}#kern[0.8]{t}#kern[0.3]{'+LSP+'},  (#font[50]{m}#kern[0.1]{_{#lower[-0.12]{'+STP+'}}}#kern[0.3]{=}#kern[0.1]{'+mS+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'
            if '_mC-' in massPoint: 
                mC = massPoint.split('_mC-')[1].split('_')[0]
                if 'SlepSnu' in massPoint:
                    massPointName = CHP+'#kern[0.3]{'+CHM+'}, '+CHR+'#kern[0.15]{#rightarrow}#kern[0.15]{#tilde{#font[12]{l}}#nu/#font[12]{l}#tilde{#nu}}#kern[0.15]{#rightarrow}#kern[0.15]{#font[12]{l}}#nu'+LSP+', (#font[50]{m}_{'+CHR+'}#kern[0.3]{=}#kern[0.1]{'+mC+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'
                elif 'pmWW' in massPoint:
                    massPointName = CHP+'#kern[0.3]{'+CHM+'}, '+CHR+'#kern[0.15]{#rightarrow}#kern[0.15]{W}'+LSP+', (#font[50]{m}_{'+CHR+'}#kern[0.3]{=}#kern[0.1]{'+mC+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'
        else:
            massPointName = massPointName.replace('_mS-', 'm_{'+STP+'}=').replace('_mC-', 'm_{'+CHR+'}=').replace('_mX-', ' m_{'+LSP+'}=')
        if 'Slep' in opt.tag or 'Chargino' in opt.tag: massPointName = massPointName.replace(' m_{'+STP+'}=',' m_{'+SLE+'}=')
        massPointNameLatex = massPoint.replace('_mS-', '\\invM{\\PSQtDo}=').replace('_mC-', '\\invM{\\PSGcpmDo}=').replace('_mX-', ', \\invM{\\PSGczDo}=')
        #massPointNameLatex = massPointNameLatex.replace('TChipmSlepSnu', '\\PSGcpmDo\\PSGcpmDo, \\TChipmDecay,') 
        #massPointNameLatex = massPointNameLatex.replace('T2tt', '\\PSQtDo\\PASQtDo, \\PSQtDo\\to\\PQt\\PSGczDo,')
        massPointNameLatex = massPointNameLatex.replace('TChipmSlepSnu', '').replace('T2tt', '')
        massPointNameLatex = '\\ensuremath{'+massPointNameLatex+'}'              

        plot[massPoint]  = { 
                    'nameHR' : massPointName,
                    'nameLatex' : massPointNameLatex,
                    'color': signalColor,  
                    'isSignal' : signalType,
                    'isData'   : 0,
                    'scale'    : 1.0
        }

        groupPlot[massPoint]  = {
                    'nameHR' : massPointName,
                    'nameLatex' : massPointNameLatex,
                    'isSignal' : signalType,
                    'color': signalColor,  
                    'samples'  : [massPoint], 
                    'scale'    : 1.0
        }
                
        signalType = 3
        if not hasattr(opt, 'paperStyle') or not opt.paperStyle:
            signalColor += 1
        else:
            #signalColor = '#92dadd'
            signalColor += 1

#

for group in groupPlot:
    cutToRemoveFromGroup = [ ]
    for cut in cuts:
        samplesInCut = [ ]
        for sample in groupPlot[group]['samples']:
            if not ('removeFromCuts' in samples[sample] and cut in samples[sample]['removeFromCuts']):
                samplesInCut.append(sample)
        if len(samplesInCut)==0:
            cutToRemoveFromGroup.append(cut)
    if len(cutToRemoveFromGroup)>0:
        groupPlot[group]['removeFromCuts'] = cutToRemoveFromGroup
        

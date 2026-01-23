### nuisances

### general parameters

if len(list(yearstag.keys()))!=1:
    print('WARNING: nuisances.py cannot be used on multiple years')
    exit()

for key in yearstag:
    year = '_' + key
    yearstaglist = yearstag[key].split('-')

### nuisances = {}
 
### statistical uncertainty

nuisances['stat']  = {
              'type'  : 'auto',   # Use the following if you want to apply the automatic combine MC stat nuisances.
              'maxPoiss'  : '10',     # Number of threshold events for Poisson modelling
              'includeSignal'  : '1', # Include MC stat nuisances on signal processes (1=True, 0=False)
              'removeZeros' : removeZeros,
              'samples' : {}
             }
if '_NoMCStat' in opt.tag: del nuisances['stat'] 

### global lnN (luminosity and trigger)

for globalNuisance in globalNuisances:

    nuisances[globalNuisance]  = {
                   'name'  : globalNuisances[globalNuisance]['name'].replace('_yeartag', year.replace('noHIPM','').replace('HIPM','')), # Bleah!
                   'samples'  : { },
                   'type'  : 'lnN',
    }
    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            nuisances[globalNuisance]['samples'][sample] = globalNuisances[globalNuisance]['value']

# trigger stat

if 'TrigLatino' not in opt.tag:
    nuisances['trigger']  = {
        'name'    : 'trigger'+year,
        'type'    : 'shape',
        'kind'    : 'weight',
        'samples' : { },
    }
    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            if 'SigV6' not in opt.tag or not samples[sample]['isSignal']:
                nuisances['trigger']['samples'][sample] = [ 'triggerWeight[2]/triggerWeight[1]', 'triggerWeight[0]/triggerWeight[1]' ]
 
# background cross section and scale factor uncertainties

for background in normBackgroundNuisances:
    if background in samples:

        scalefactorFromData = False

        for region in normBackgroundNuisances[background]:
            nuisancename = normBackgroundNuisances[background][region]['name']
            nuisances[nuisancename]  = {
                'name'    : nuisancename+year.replace('noHIPM','').replace('HIPM',''), 
                'samples' : normBackgroundNuisances[background][region]['samples'],
                'cuts'    : normBackgroundNuisances[background][region]['cuts'], 
                'type'    : normBackgroundNuisances[background][region]['type'],
            }
            if 'kind' in normBackgroundNuisances[background][region]:
                nuisances[nuisancename]['kind'] = normBackgroundNuisances[background][region]['kind']
            scalefactorFromData = normBackgroundNuisances[background][region]['scalefactorFromData']  

        if scalefactorFromData: # Remove gloabl lnN uncertainties for backgrounds normalized on data
            for globalNuisance in globalNuisances: 
                if background in nuisances[globalNuisance]['samples']:
                    del nuisances[globalNuisance]['samples'][background]
            if background in nuisances['trigger']['samples']:
                    del nuisances['trigger']['samples'][background]

### shapes

# lepton reco, id, iso, fastsim

for scalefactor in leptonSF:

    nuisances[scalefactor]  = {
        'name'  : scalefactor+year,
        'samples'  : { },
    }
    nuisances[scalefactor]['type'] = leptonSF[scalefactor]['type']   
    if leptonSF[scalefactor]['type']=='shape':
        nuisances[scalefactor]['kind'] = 'weight'   
    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                if ('EOY' not in sample and (not samples[sample]['isFastsim'] or 'SigV6' not in opt.tag)) or 'Extra' not in scalefactor:
                    nuisances[scalefactor]['samples'][sample] = leptonSF[scalefactor]['weight']

# b-tagging scale factors

btagWeight1tagSyst = btagWeight1tag if 'TrigBTag' not in opt.tag else btagWeight1tag.replace('*triggerWeightBTag', '') # Bleah!!!
bSelections = { '1b' : { 'weight' : btagWeight1tagSyst+'_syst/'+btagWeight1tagSyst,
                         'cuts'   : [ '_Tag', 'Fake', 'ttZ', '1tag', '2tag' ] },
                '0b' : { 'weight' : '(1.-'+btagWeight1tagSyst+'_syst)/(1.-'+btagWeight1tagSyst+')',
                         'cuts'   : [ '_Veto', '_NoTag', 'WZ_', 'WZtoWW_', 'ZZ', 'Zpeak' ] },
               }
if 'SameSignVeto' in opt.tag:
    bSelections['0b']['cuts'].append('SS_')
else:
    bSelections['1b']['cuts'].append('SS_')

if 'ttZNormalization' in opt.tag or 'FitCRttZ' in opt.tag:
    if len(list(btagweightmixtagSyst.keys()))>0:
        bSelections['ttZ'] = { 'weight' : btagweightmixtagSyst }
        if len(list(btagweightmixtagISRSyst.keys()))==0:
            bSelections['ttZ']['cuts'] = [ '_Tag', 'ttZ' ] 
        else:
            bSelections['ttZ']['cuts'] = [ 'SR1_Tag', 'SR2_Tag', 'CR1_Tag', 'CR2_Tag' ]
            bSelections['isr'] = { 'weight' : btagweightmixtagISRSyst,
                                   'cuts'   : [ 'SR3_Tag', 'SR4_Tag', 'CR3_Tag', 'CR4_Tag' ] }
        del bSelections['1b']
        del bSelections['0b']
elif len(list(ISRWeightTagRelVar.keys()))>0:
    bSelections['isr'] = { 'weight' : ISRWeightTagRelVar,
                           'cuts'   : [ 'SR3_Tag', 'SR4_Tag' ] }
    bSelections['1b']['cuts'].remove('_Tag')
    bSelections['1b']['cuts'].extend([ 'SR1_Tag', 'SR2_Tag']) 

for scalefactor in bTagNuisances:
    for bsel in bSelections:
        nuisances[scalefactor+bsel]  = {
            'name'  : bTagNuisances[scalefactor]['name'].replace('_yeartag', year),
            'samples'  : { },
            'kind'  : 'weight',
            'type'  : 'shape',
            'cuts'  : [ ]           
        }
        bselweight = bSelections[bsel]['weight']
        scafactvar = bTagNuisances[scalefactor]['var']
        for sample in list(samples.keys()):
            if not samples[sample]['isDATA']:
                if 'FS' not in scalefactor or samples[sample]['isFastsim']:
                    if ('EOY' not in sample and not samples[sample]['isFastsim']) or scalefactor!='btagcor': 
                        if isinstance(bselweight, str):
                            nuisances[scalefactor+bsel]['samples'][sample] = [ bselweight.replace('syst', scafactvar.replace('VAR', 'up'  )),
                                                                               bselweight.replace('syst', scafactvar.replace('VAR', 'down')) ]
                        else:
                            nuisances[scalefactor+bsel]['samples'][sample] = [ bselweight[scalefactor].replace('syst', scafactvar).replace('VAR', 'up'  ), 
                                                                               bselweight[scalefactor].replace('syst', scafactvar).replace('VAR', 'down') ] 

        for cut in list(cuts.keys()):
            for bselcut in bSelections[bsel]['cuts']:
                if bselcut in cut:
                    nuisances[scalefactor+bsel]['cuts'].append(cut)
                    break

# pileup

if '_NoPU' not in opt.tag:
    nuisances['pileup']  = {
        'name'  : 'pileup', # inelastic cross section correlated through the years
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            nuisances['pileup']['samples'][sample] = [ 'puWeightUp/puWeight', 'puWeightDown/puWeight' ] 

# ECAL prefiring

if '2016' in opt.tag or '2017' in opt.tag: 
    nuisances['prefiring']  = {
        'name'  : 'prefiring'+year, 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            nuisances['prefiring']['samples'][sample] = [ 'PrefireWeight_Up/PrefireWeight', 'PrefireWeight_Down/PrefireWeight' ] 

# nonprompt lepton rate

nuisances['nonpromptLep']  = {
    'name'  : 'nonpromptLep'+year, 
    'samples'  : { },
    'kind'  : 'weight',
    'type'  : 'shape',
}
for sample in list(samples.keys()):
    if not samples[sample]['isDATA']:
        nuisances['nonpromptLep']['samples'][sample] = [ nonpromptLepSF_Up+'/'+nonpromptLepSF, nonpromptLepSF_Down+'/'+nonpromptLepSF ] 

# top pt reweighting

if 'ttbar' in samples:
    nuisances['toppt']  = {
        'name'  : 'toppt', # assuming the mismodeling is correlated through the years 
        'samples'  : { 'ttbar' : [ systematicTopPt+'/'+centralTopPt, '1.' ] },
        'kind'  : 'weight',
        'type'  : 'shape',
    }

# isr fastsim

if 'NoISRW' not in opt.tag and 'pmssm' not in opt.sigset:
    nuisances['isrFS']  = {
        'name'  : 'isrFS', # assuming the mismodeling is correlated through the years 
        'samples'  : { },
        'kind'  : 'weight',
        'type'  : 'shape',
    }
    for sample in list(samples.keys()):
        if 'isrObservable' in samples[sample]:
                if samples[sample]['isrObservable']=='njetISR':
                    isrWeight = [ '0.5*(3.*isrW-1.)/isrW', '0.5*(isrW+1.)/isrW' ]
                elif samples[sample]['isrObservable']=='ptISR':
                    isrWeight = [ '(2.*isrW-1.)/isrW', '1./isrW' ]
                else:
                    print('ERROR: no isrW implementation for model', model)
                nuisances['isrFS']['samples'][sample] = isrWeight
else:
    nuisances['isrFS']  = {
        'name'  : 'isrFS',
        'samples'  : { },
        'type'  : 'lnN',
    }
    for sample in list(samples.keys()):
        if samples[sample]['isSignal']:
            nuisances['isrFS']['samples'][sample] = '1.010'

### mt2ll backgrounds (special case for shape uncertainties)

mt2llRegions = [ ]
for cut in cuts:
    ptmissCut = cut.split('_')[0]+'_'
    if ('SR' in ptmissCut or 'VR1' in ptmissCut) and ptmissCut not in mt2llRegions:
        mt2llRegions.append(ptmissCut)

# mt2ll top and WW

addMT2Shapes = 'SignalRegions' in opt.tag

if addMT2Shapes:

    mt2llweightUp = '(1. + 0.75*(mt2ll'+ctrltag+'>=370))'
    mt2llweightDo = '(1. - 0.75*(mt2ll'+ctrltag+'>=370))'

    nuisancekey = 'WZbin'
    nuisances[nuisancekey]  = {
        'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
        'samples'  : { 'WZ' : [ mt2llweightUp, mt2llweightDo] },
        'OneSided' : False,
        'kind'  : 'weight',
        'type'  : 'shape'
    }

    mt2llweightUp = '(1. + 0.2*(mt2ll>=100.)*(mt2ll<160.) + 0.4*(mt2ll>=160.)*(mt2ll<240.) + 0.5*(mt2ll>=240))'
    mt2llweightDo = '1.'

    for mt2llregion in mt2llRegions:
        if 'VR1' in mt2llregion: continue

        if 'WWTails' not in opt.tag.split('_')[0] and 'WWHighs' not in opt.tag.split('_')[0] and 'WWPol1a' not in opt.tag.split('_')[0] and 'WWPol1b' not in opt.tag.split('_')[0]:

            if isShape or hasattr(opt, 'groups') or hasattr(opt,'skipLNN') or '_WWShapeCorr' not in opt.tag:

                nuisancekey = 'WWshape_'+mt2llregion
                nuisances[nuisancekey]  = {
                    'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                    'samples'  : { 'ttbar' : [ mt2llweightUp, mt2llweightDo],
                                   'STtW'  : [ mt2llweightUp, mt2llweightDo],
                                   'WW'    : [ mt2llweightUp, mt2llweightDo] },
                    'OneSided' : True,
                    'kind'  : 'weight',
                    'type'  : 'shape',
                    'cuts'  : [ ]
                } 

                for cut in list(cuts.keys()):
                    if mt2llregion in cut:
                        nuisances[nuisancekey]['cuts'].append(cut)

                if '_WWcorrSR' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWshape'+year.replace('noHIPM','').replace('HIPM','')
                elif '_WWcorrYear' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWshape_'+mt2llregion
                elif '_WWcorr' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWshape'

            if isShape or hasattr(opt, 'groups') or hasattr(opt,'skipLNN') or '_WWShapeCorr' in opt.tag:

                binList = []
                if 'Stop' in opt.tag: binList.extend([ 'Bin6', 'Bin7' ])
                elif 'Merge' not in opt.tag: binList.extend([ 'Bin6', 'Bin7', 'Bin8' , 'Bin9' ])
                else: 
                    if 'SR1' in mt2llregion: binList.extend([ 'Bin6', 'Bin7' ])
                    elif 'SR2' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8' ])
                    elif 'SR3' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8' ])
                    elif 'SR4' in mt2llregion: binList.extend([ 'Bin6', 'Bin7', 'Bin8', 'Bin9' ])

                for ibin in binList:
                    nuisancekey = 'WWshape_'+ibin+'_'+mt2llregion
                    nuisances[nuisancekey]  = {
                        'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                        'samples'  : { 'ttbar' : [ mt2llweightUp, mt2llweightDo],
                                       'STtW'  : [ mt2llweightUp, mt2llweightDo],
                                       'WW'    : [ mt2llweightUp, mt2llweightDo] },
                        'OneSided' : True,
                        'kind'  : 'weight',
                        'type'  : 'shape',
                        'cuts'  : [ ]
                    }

                    for cut in list(cuts.keys()):
                        if mt2llregion in cut:
                            nuisances[nuisancekey]['cuts'].append(cut)

        else:

            nuisancekey = 'WWtails_'+mt2llregion
            nuisances[nuisancekey]  = {
                    'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                    'samples'  : { 'ttbar' : [ WWtailsUp+'/'+WWtails, WWtailsDown+'/'+WWtails ],
                                   'STtW'  : [ WWtailsUp+'/'+WWtails, WWtailsDown+'/'+WWtails ],
                                   'WW'    : [ WWtailsUp+'/'+WWtails, WWtailsDown+'/'+WWtails ] },
                    'kind'  : 'weight',
                    'type'  : 'shape',
                    'cuts'  : [ ]
            }
            if 'WZtoWW' in opt.tag and 'WWPol1a' in opt.tag:
                nuisances[nuisancekey]['samples']['WZ'] = [ WWtailsUp+'/'+WWtails, WWtailsDown+'/'+WWtails ]
            if '_WWcorrSR' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWtails'+year.replace('noHIPM','').replace('HIPM','') 
            elif '_WWcorrYear' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWtails_'+mt2llregion
            elif '_WWcorr' in opt.tag: nuisances[nuisancekey]['correlatedName'] = 'WWtails'

            for cut in list(cuts.keys()):
                if mt2llregion in cut:
                    nuisances[nuisancekey]['cuts'].append(cut)

    if 'WWPhi' in opt.tag:
        nuisancekey = 'WWphi_SR4'
        if 'WWPhib' in opt.tag or 'WWPhic' in opt.tag: 
            if 'WWPhib' in opt.tag:
                p0, p1, p2 = '(6.23149e-01)', '(4.24170e+01)', '(-3.86854e+00)'
                p3, p4, p5 = '(5.60494e-01)', '(6.00449e+01)', '(-5.44043e+00)'
            elif 'WWPhic' in opt.tag:
                p0, p1, p2 = '(2.52859e-01)', '(7.05954e+01)', '(-6.03146e+00)'
                p3, p4, p5 = '(2.53251e-01)', '(1.39018e+02)', '(-8.17122e+00)'
            WWphiUp = '(('+p0+'+'+p1+'*exp('+p2+'*('+dPhiMinlepptmiss+')))/('+p3+'+'+p4+'*exp('+p5+'*('+dPhiMinlepptmiss+'))))'
        if 'WWPhiW' in opt.tag:
            WWphiUp = '1./'+WWphiWeight
        else:
            WWphiUp = '1.65965+(6.22541e-01)*log(('+dPhiMinlepptmiss+')+0.16)'
        nuisances[nuisancekey]  = {
                        'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                        'samples'  : { 'ttbar' : [ WWphiUp, '1.' ],
                                       'STtW'  : [ WWphiUp, '1.' ],
                                       'WW'    : [ WWphiUp, '1.' ] },
                        'kind'  : 'weight',
                        'type'  : 'shape',
                        'cuts'  : [ ]
        }
        if ('WWPhibAll' in opt.tag or 'WWPhicAll' in opt.tag or 'WWPhiWAll' in opt.tag) and '_NoWWPhiMinor' not in opt.tag:
            for sample in samples:
                if not samples[sample]['isDATA'] and not samples[sample]['isSignal']:
                    if sample not in nuisances[nuisancekey]['samples']:
                        nuisances[nuisancekey]['samples'][sample] = [ WWphiUp, '1.' ]
        for cut in list(cuts.keys()):
            if 'SR4' in cut or ('CR4' in cut and '_NoWWPhiMinor' not in opt.tag and ('WWPhibAll' in opt.tag or 'WWPhicAll' in opt.tag or 'WWPhiWAll' in opt.tag)):
                nuisances[nuisancekey]['cuts'].append(cut)

if '_mt2sr4' in opt.tag:
    WWbunkUp = '(1.*(mt2ll>=80.) + 0.77529412*(mt2ll<20.) + 0.93035294*(mt2ll>=20.)*(mt2ll<40.) + 1.1629412*(mt2ll>=40)*(mt2ll<60.) + 1.9640784*(mt2ll>=60)*(mt2ll<80.))'
    WWbunkDown = '1.'
    nuisancekey = 'MT2sr4_'
    nuisances[nuisancekey]  = {
                    'name'  : nuisancekey+year.replace('noHIPM','').replace('HIPM',''),
                    'samples'  : { 'ttbar' : [ WWbunkUp, WWbunkDown ],
                                   'STtW'  : [ WWbunkUp, WWbunkDown ],
                                   'WW'    : [ WWbunkUp, WWbunkDown ] },
                    'kind'  : 'weight',
                    'type'  : 'shape',
                    'cuts'  : [ ]
            }
    for cut in list(cuts.keys()):
        if 'SR4' in cut and 'CR' not in cut:
            nuisances[nuisancekey]['cuts'].append(cut)

# mt2ll top and WW SUS-17-010 style
#mt2llBins = [ ]
#mt2llNuisances = False
#if not isDatacardOrPlot or mt2llNuisances:
#    if 'Optim' not in opt.tag or 'MT2' not in opt.tag:
#        mt2llBins = ['Bin4', 'Bin5', 'Bin6', 'Bin7']
#        mt2llEdges = ['60.', '80.', '100.', '120.', '999999999.']
#        mt2llSystematics = [0.05, 0.10, 0.20, 0.30]
#    elif 'High' in opt.tag and 'Extra' in opt.tag:
#        mt2llBins = ['Bin6', 'Bin7', 'Bin8', 'Bin9' ]
#        mt2llEdges = ['100.', '160.', '240.', '370.', '999999999.']
#        mt2llSystematics = [0.20, 0.30, 0.30, 0.30] # placeholders    
#    elif 'High' in opt.tag:
#        mt2llBins = ['Bin6', 'Bin7', 'Bin8' ]     
#        mt2llEdges = ['100.', '160.', '370.', '999999999.']
#        mt2llSystematics = [0.20, 0.30, 0.30] # placeholders     
#    else:
#        mt2llBins = ['Bin6', 'Bin7' ]
#        mt2llEdges = ['100.', '160.', '999999999.']
#        mt2llSystematics = [0.20, 0.30] # placeholders            
#
#for mt2llregion in mt2llRegions: 
#    if 'VR1' in mt2llregion: continue
#    for mt2llbin in range(len(mt2llBins)):
#
#        mt2llsystname = mt2llregion + mt2llBins[mt2llbin]
#        mt2llweightUp = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.+mt2llSystematics[mt2llbin])+' : 1.'  
#        mt2llweightDo = '(mt2ll>='+mt2llEdges[mt2llbin]+' && mt2ll<'+mt2llEdges[mt2llbin+1]+') ? '+str(1.-mt2llSystematics[mt2llbin])+' : 1.'  
#        
#        nuisances['Top_'+mt2llsystname]  = {
#            'name'  : 'Top_'+mt2llsystname+year,
#            'samples'  : { 
#                'ttbar' : [ mt2llweightUp, mt2llweightDo],
#                'STtW'  : [ mt2llweightUp, mt2llweightDo],
#                'tW'    : [ mt2llweightUp, mt2llweightDo], # backward compatibility for background names
#            },
#            'kind'  : 'weight',
#            'type'  : 'shape',
#            'cuts'  : [ ]           
#        }
#        
#        nuisances['WW_'+mt2llsystname]  = {
#            'name'  : 'WW_'+mt2llsystname+year,
#            'samples'  : { 
#                'WW' : [ mt2llweightUp, mt2llweightDo],
#            },
#            'kind'  : 'weight',
#            'type'  : 'shape',
#            'cuts'  : [ ]           
#        }
#
#        for cut in cuts.keys():
#            if mt2llregion in cut:
#                nuisances['Top_'+mt2llsystname]['cuts'].append(cut)
#                nuisances['WW_' +mt2llsystname]['cuts'].append(cut)

# mt2ll DY (from control regions)
 
# mt2ll ZZ (from k-factors)

# mt2ll signal
if signalReco=='fast' and fastsimMetType!='reco' and '_NoPtMissFast' not in opt.tag and 'SearchRegion' not in opt.tag: 
    if fastsimMetType=='average' or not isFillShape:
        nuisances['ptmissfastsim']  = {
            'name'  : 'ptmissfastsim', # mismodeling correlated through the years?
            'samples'  : { },
            'kind'  : 'tree',
            'type'  : 'shape',
            'folderUp':   directorySig.replace('__susyMT2fast', '__susyMT2reco'),
            'folderDown': directorySig.replace('__susyMT2fast', '__susyMT2genm').replace('Smear', 'Nomin'),
        }
        if fastsimMetType=='acceptance': nuisances['ptmissfastsim']['extremes'] = [ '_reco', '_gen' ]
        for sample in list(samples.keys()):
            if samples[sample]['isFastsim']:
                nuisances['ptmissfastsim']['samples'][sample] = ['1.', '1.']

### QCD scale and PDFs

nuisances['qcdScale'] = {
    'name': 'qcdScale', # Scales correlated through the years?
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ],
}

nuisances['pdf'] = {
    'name': 'pdf', # PDFs correlated through the years?
    'kind': 'weight_rms',
    'type': 'shape',
    'samples': { },
    'cuts' : [ ],
}

for yeartomerge in yearstaglist:

    #theoryRecoFlag = recoFlag+'SigV6' if ('SigV6' in opt.tag or 'EOY' in opt.sigset) else recoFlag
    exec(open('./Data/theoryNormalizations/theoryNormalizations'+recoFlag+'_'+yeartomerge+'.py').read())

    # LHE sca variation weights (w_var / w_nominal)
    # [0] is muR=0.50000E+00 muF=0.50000E+00
    # [1] is muR=0.50000E+00 muF=0.10000E+01
    # [2] is muR=0.50000E+00 muF=0.20000E+01
    # [3] is muR=0.10000E+01 muF=0.50000E+00
    # [4] is muR=0.10000E+01 muF=0.10000E+01
    # [5] is muR=0.10000E+01 muF=0.20000E+01
    # [6] is muR=0.20000E+01 muF=0.50000E+00
    # [7] is muR=0.20000E+01 muF=0.10000E+01
    # [8] is muR=0.20000E+01 muF=0.20000E+01

    for sample in list(samples.keys()):
        if not samples[sample]['isDATA']:
            if sample=='minor':
                nuisances['qcdScale']['samples'][sample] = []
                nuisances['pdf']['samples'][sample] = []
                continue
            elif sample not in theoryNormalizations:
                print('Nuisance warning: sample', sample, 'not in theoryNormalizations')
                continue
            if theoryNormalizations[sample]['qcdScaleStatus']==3:
                qcdScaleVariations = [ ]
                qcdWeightIndexList = [0, 1, 3, 5, 7, 8] if len(theoryNormalizations[sample]['qcdScale'])==9 else [1, 6, 16, 26, 36, 41]
                for i in qcdWeightIndexList:
                    qcdScaleVariations.append('Alt$(LHEScaleWeight['+str(i)+'],1.)/'+theoryNormalizations[sample]['qcdScale'][i])
                nuisances['qcdScale']['samples'][sample] = qcdScaleVariations
            if not samples[sample]['isSignal'] and theoryNormalizations[sample]['pdfStatus']==3:
                pdfVariations = [ ] 
                for i in range(len(theoryNormalizations[sample]['pdf'])):                              
                    pdfVariations.append('Alt$(LHEPdfWeight['+str(i)+'],1.)/'+theoryNormalizations[sample]['pdf'][i])
                nuisances['pdf']['samples'][sample] = pdfVariations

for cut in cuts: # TODO: Why only in the signal regions? 
    if 'SR' in cut.split('_')[0] and 'ObjectReview' not in opt.tag:
        nuisances['qcdScale']['cuts'].append(cut)
        nuisances['pdf']['cuts'].append(cut)

if '_NoQCDScale' in opt.tag: del nuisances['qcdScale']
if '_NoPDF'      in opt.tag: del nuisances['pdf']

### JES, JER and MET

for treeNuisance in treeNuisances:

    for mcType in treeNuisanceDirs[treeNuisance]:
        if 'jesTotalV' in treeNuisance and mcType=='Bkg': continue
        if not isShape and not hasattr(opt, 'skipLNN') and 'FastJEC' in opt.tag and 'jesTotal' in treeNuisance and mcType=='Sig':
            if '_JEUV2' in opt.tag:
                if 'jesTotalV2' not in treeNuisance: continue
            elif '_JEUV3' in opt.tag:
                if 'jesTotalV3' not in treeNuisance: continue
            else:
                if 'jesTotalV' in treeNuisance: continue
        if '_NoSigEU' in opt.tag and mcType=='Sig': continue
        if '_NoJER' in opt.tag and 'jer' in treeNuisance: continue
        if '_NoJES' in opt.tag and 'jes' in treeNuisance: continue
        if '_NoMET' in opt.tag and 'unc' in treeNuisance: continue
        if 'Down' not in treeNuisanceDirs[treeNuisance][mcType] or 'Up' not in treeNuisanceDirs[treeNuisance][mcType]:
            print('nuisance warning: missing trees for', treeNuisance, mcType, 'variations')
        else:

            mcTypeName = 'FS' if (mcType=='Sig' and not treeNuisances[treeNuisance]['BkgToSig']) else ''
            yearCorr = '' if treeNuisances[treeNuisance]['year'] else year # not correlated through the years?

            nuisances[treeNuisance+mcType] = {
                'name': treeNuisance+mcTypeName+yearCorr, 
                'kind': 'tree',
                'type': 'shape',
                'OneSided' : treeNuisances[treeNuisance]['onesided'],
                'synchronized' : False,
                'samples': { },
                'folderDown': treeNuisanceDirs[treeNuisance][mcType]['Down'],
                'folderUp':   treeNuisanceDirs[treeNuisance][mcType]['Up'],
            }
            for sample in list(samples.keys()):
                if not samples[sample]['isDATA'] and not ('NoDY' in opt.tag and treeNuisance=='jer' and '2017' in year and sample=='DY'):# and sample!='WJetsToLNu':
                    if (mcType=='Bkg' and not samples[sample]['isSignal']) or (mcType=='Sig' and samples[sample]['isSignal']):
                        nuisances[treeNuisance+mcType]['samples'][sample] = ['1.', '1.']

            if len(list(nuisances[treeNuisance+mcType]['samples'].keys()))==0:
                del nuisances[treeNuisance+mcType]

    if hasattr(opt, 'cardList') and treeNuisances[treeNuisance]['BkgToSig']:
        if treeNuisance+'Bkg' in nuisances and treeNuisance+'Sig' in nuisances:
            nuisances[treeNuisance+'Bkg']['samples'].update(nuisances[treeNuisance+'Sig']['samples']) 
            del nuisances[treeNuisance+'Sig']

if not isShape and 'FastJEC' in opt.tag and ('_JEUV2' in opt.tag or '_JEUV3' in opt.tag):
    if hasattr(opt, 'cardList'):
        for treeNuisance in treeNuisances:
            if 'jesTotalV' in treeNuisance:
                if treeNuisances[treeNuisance]['BkgToSig']:
                    jesNuisNameBkg = treeNuisance.split('TotalV')[0]+'TotalBkg'
                    if jesNuisNameBkg in nuisances and treeNuisance+'Sig' in nuisances:
                        nuisances[jesNuisNameBkg]['samples'].update(nuisances[treeNuisance+'Sig']['samples'])
                        del nuisances[treeNuisance+'Sig']

### rate parameters
rateparameters = {
    'Topnorm' :  { 
        'samples' : [ 'ttbar', 'tW', 'STtW' ],
        'subcuts' : [ '' ],
    },
    'NoJetRate_JetBack' : {
        'samples' : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts' : [ '_NoJet_' ],
        #'limits'  : '[0.5,1.5]',
    },
    'JetRate_JetBack' : {
        'samples'  : [ 'ttbar', 'tW', 'STtW', 'ttW', 'ttZ' ],
        'subcuts'  : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_JetBack',
    }
}
if '_NoWWRate' not in opt.tag: 
    rateparameters['WWnorm'] = {
        'samples' : [ 'WW' ],
        'subcuts' : [ '' ],
    }
    rateparameters['NoJetRate_DibosonBack'] = {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoJet_' ],
        #'limits'  : '[0.7,1.3]'
    }
    rateparameters['JetRate_DibosonBack'] = {
        'samples' : [ 'WW', 'WZ' ],
        'subcuts' : [ '_NoTag_' ],
        'bondrate' : 'NoJetRate_DibosonBack',
    }
if '_NewBond4' in opt.tag:
    rateparameters['Topnorm']['limits'] = '[0.7,1.3]'
    rateparameters['WWnorm']['limits'] = '[0.5,1.5]'
elif '_NewBond5' in opt.tag:
    rateparameters['Topnorm']['limits'] = '[0.,2.]'
    rateparameters['WWnorm']['limits'] = '[0.,2.]'
elif '_NewBond6' in opt.tag:
    rateparameters['Topnorm']['limits'] = '[-3.,3.]'
    rateparameters['WWnorm']['limits'] = '[-3.,3.]'
if '_NoJetBond' not in opt.tag:
    if '_NewBond6' in opt.tag:
        rateparameters['NoJetRate_JetBack']['limits'] = '[-3.,5.]'
        rateparameters['NoJetRate_DibosonBack']['limits'] = '[-3.,5.]'
    elif '_NewBond5bX' in opt.tag:
        rateparameters['NoJetRate_JetBack']['limits'] = '[0.2,3.]'
        rateparameters['NoJetRate_DibosonBack']['limits'] = '[0.2,3.]'
    elif '_NewBond5bT' in opt.tag:
        rateparameters['NoJetRate_JetBack']['limits'] = '[0.5,1.5]'
        rateparameters['NoJetRate_DibosonBack']['limits'] = '[0.7,1.3]'
    elif '_NewBond3' in opt.tag or '_NewBond4' in opt.tag or '_NewBond5' in opt.tag:
        rateparameters['NoJetRate_JetBack']['limits'] = '[0.2,3.]'
        rateparameters['NoJetRate_DibosonBack']['limits'] = '[0.,3.]'
    else:
        rateparameters['NoJetRate_JetBack']['limits'] = '[0.5,1.5]'
        rateparameters['NoJetRate_DibosonBack']['limits'] = '[0.7,1.3]'
if '_KeepVetoNorm' not in opt.tag:
    del rateparameters['JetRate_JetBack']
    del rateparameters['JetRate_DibosonBack']

if '_TopRP2' in opt.tag:
    rateparameters['Topnormtag'] = {}
    for key in rateparameters['Topnorm']:
        rateparameters['Topnormtag'][key] = rateparameters['Topnorm'][key]
    rateparameters['Topnormtag']['subcuts'] = [ '_Tag_' ]
    rateparameters['Topnorm']['subcuts'] = [ '_Veto_', '_NoJet_', '_NoTag_' ]

if 'FitCR' in opt.tag:
    backgroundCRs = { 'ttZ' : { 'samples' : [ 'ttZ' ],
                                'regions' : { '_Tag_' : [ '_NoTag_', '_Veto_', '_Tag_' ] }, },
                      'WZ'  : { 'samples' : [ 'WZ' ],  
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                      'ZZ'  : { 'samples' : [ 'ZZTo2L2Nu', 'ZZTo4L' ],
                                'regions' : { '_Veto_' : [ '_Veto_', '_Tag_' ] , '_NoTag_' : [ '_NoTag_', '_Tag_' ], '_NoJet_' : [ '_NoJet_' ] }, },
                    }
    if '_NoZZ2Lrate' in opt.tag: backgroundCRs['ZZ']['samples'] = [ 'ZZTo4L' ]
    for controlregion in backgroundCRs:
        for sample in backgroundCRs[controlregion]['samples']:
            for rateparam in list(rateparameters.keys()):
                if sample in rateparameters[rateparam]['samples']: 
                    rateparameters[rateparam]['samples'].remove(sample)
        for region in backgroundCRs[controlregion]['regions']:
            useRegion = False
            for cut in cuts:
                if region in cut:
                    useRegion = True
                    continue
            if useRegion:
                rateparameters['CR'+region+controlregion] = { }
                rateparameters['CR'+region+controlregion]['samples'] = backgroundCRs[controlregion]['samples']
                rateparameters['CR'+region+controlregion]['subcuts'] = backgroundCRs[controlregion]['regions'][region]
                if '_NoCRBond' not in opt.tag:
                    if '_NewBond6a' in opt.tag:
                        rateparameters['CR'+region+controlregion]['limits'] = '[-5.,5.]'
                    elif '_NewBond2a' in opt.tag or '_NewBond3a' in opt.tag or '_NewBond4a' in opt.tag or '_NewBond5a' in opt.tag:
                        rateparameters['CR'+region+controlregion]['limits'] = '[-3.,5.]'
                    elif '_NewBond5bC' in opt.tag:
                        rateparameters['CR'+region+controlregion]['limits'] = '[0.3,1.7]'
                    elif '_NewBond2b' in opt.tag or '_NewBond3b' in opt.tag or '_NewBond4b' in opt.tag or '_NewBond5bX' in opt.tag:
                        rateparameters['CR'+region+controlregion]['limits'] = '[-3.,7.]'
                    elif '_NewBond2' in opt.tag or '_NewBond3' in opt.tag or '_NewBond4' in opt.tag or '_NewBond5' in opt.tag: 
                        rateparameters['CR'+region+controlregion]['limits'] = '[0.,5.]' 
                    elif '_NewBond' in opt.tag: 
                        rateparameters['CR'+region+controlregion]['limits'] = '[0.2,2.]'
                    else: 
                        rateparameters['CR'+region+controlregion]['limits'] = '[0.3,1.7]'

if hasattr(opt, 'outputDirDatacard'):
    rateParameterToMerge = []
    fileIn = ROOT.TFile(opt.inputFile, 'READ')
    for mt2llregion in mt2llRegions: 
        for rateparam in rateparameters: 
            
            if 'CR_' in rateparam:
                useControlRegion = False            
                for cut in cuts:
                    if mt2llregion in cut and rateparam.split('_')[1]==cut.split('_')[1]:
                        useControlRegion = True
                        continue
                if not useControlRegion: continue

            rateparamname = rateparam + '_' + mt2llregion
            #rateparamnamename = rateparamname if mt2llregion!='SR1_' or 'NoJetRate' not in rateparam else rateparam + '_SR2_'
            
            for sample in rateparameters[rateparam]['samples']:

                if sample not in samples: continue # backward compatibility for background names

                isControlSample = True if ('isControlSample' in samples[sample] and samples[sample]['isControlSample']==1) else False

                initialValue = '1.00' if 'initval' not in list(rateparameters[rateparam].keys()) else rateparameters[rateparam]['initval']

                nuisances[sample+rateparamname]  = {
                    'name'  : rateparamname+year,
                    'samples'  : { sample : initialValue },
                    'type'  : 'rateParam',
                    'cuts'  : [ ] 
                }
                
                if 'limits' in list(rateparameters[rateparam].keys()):
                    nuisances[sample+rateparamname]['limits'] = rateparameters[rateparam]['limits'] 
                    
                for cut in list(cuts.keys()):
                    if (mt2llregion in cut and not isControlSample) or (mt2llregion.replace('SR', 'CR').replace('VR1', 'CR0').replace('_','') in cut and 'CR_' in rateparam and rateparam.split('_')[2]==cut.split('_')[2]):
                        for subcut in rateparameters[rateparam]['subcuts']:
                            if subcut in cut:
                                nuisances[sample+rateparamname]['cuts'].append(cut)
                                if '_mergeRPfull' in opt.tag:
                                    if 'CR34_' in cut or 'CR43_' in cut: 
                                        if rateparamname not in rateParameterToMerge:
                                            rateParameterToMerge.append(rateparamname)
                                elif 'CR' in cut:
                                    if rateparamname not in rateParameterToMerge:
                                        for variable in list(variables.keys()):
                                            if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:
                                                histoData = fileIn.Get(cut+'/'+variable+'/histo_DATA')
                                                if histoData.Integral()==0.:
                                                    rateParameterToMerge.append(rateparamname)
                        
                if 'bondrate' in list(rateparameters[rateparam].keys()):
                                
                    #fileIn = ROOT.TFile(opt.inputFile, "READ")

                    nuisances[sample+rateparamname]['bond'] = {}

                    for cut in nuisances[sample+rateparamname]['cuts']:

                        nuisances[sample+rateparamname]['bond'][cut] = {}

                        for variable in list(variables.keys()):
                            if 'cuts' in variables[variable] and cut not in variables[variable]['cuts']: continue

                            histoB = fileIn.Get(cut+'/'+variable+'/histo_'+sample)
                            cutB = rateparameters[rateparam]['subcuts'][0]
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcuts'][0]
                            cutA = rateparameters[rateparameters[rateparam]['bondrate']]['subcuts'][0]
                            histoA = fileIn.Get(cut.replace(cutB, cutA)+'/'+variable+'/histo_'+sample)
                            yieldB = '%-.4f' % histoB.Integral()
                            yieldA = '%-.4f' % histoA.Integral()
            
                            bond_formula = '1+'+yieldA+'/'+yieldB+'*(1.-@0)' 
                            bond_parameters = rateparameters[rateparam]['bondrate']+'_'+mt2llregion+year
                            
                            nuisances[sample+rateparamname]['bond'][cut][variable] =  { bond_formula : bond_parameters }

                    #fileIn.Close()

    fileIn.Close()

    if '_mergeRPfull' in opt.tag:
        changeSampleRateParams, removeSampleRateParams, cutsToKeep = [], [], {}
        for rateParam in rateParameterToMerge:
            rateParameterToDelete = rateParam.replace('SR3','SR4') if 'SR3' in rateParam else rateParam.replace('SR4','SR3')
            for samplerateparam in nuisances:
                if rateParam in samplerateparam:
                    changeSampleRateParams.append(samplerateparam) 
                    removeSampleRateParams.append(samplerateparam.replace(rateParam,rateParameterToDelete))
                    cutsToKeep[samplerateparam] = [ cut for cut in nuisances[samplerateparam.replace(rateParam,rateParameterToDelete)]['cuts'] if 'SR' in cut  ]
        for samplerateparam in removeSampleRateParams:
            del nuisances[samplerateparam]
        for samplerateparam in changeSampleRateParams:
            nuisances[samplerateparam]['name'] = nuisances[samplerateparam]['name'].replace('SR3','SR34').replace('SR4','SR43')
            nuisances[samplerateparam]['cuts'].extend(cutsToKeep[samplerateparam])

    elif '_mergeRP' in opt.tag:
        for rateParam in rateParameterToMerge:

            keepRateParam = rateParam.replace('SR3','SR4') if 'SR3' in rateParam else rateParam.replace('SR4','SR3')
            if keepRateParam==rateParam or keepRateParam in rateParameterToMerge:
                print('CR rate parameters with empty regions not supported:', rateParam)
                exit()

            keepSampleRateParams, removeSampleRateParams = [], []
            for samplerateparam in nuisances:
                if keepRateParam in samplerateparam:
                    keepSampleRateParams.append(samplerateparam)
                    removeSampleRateParams.append(samplerateparam.replace(keepRateParam,rateParam))

            for samplerateparam in keepSampleRateParams:
                nuisances[samplerateparam]['name'] = nuisances[samplerateparam]['name'].replace('SR3','SR34').replace('SR4','SR43')
                if '_mergeRPfull' in opt.tag:
                    cutsToAppend = []
                    for cut in nuisances[samplerateparam]['cuts']:
                        cutsToAppend.append(cut.replace('CR3','CR34').replace('CR4','CR43') if 'CR' in cut else cut)
                    nuisances[samplerateparam]['cuts'] = cutsToAppend
                for cut in nuisances[samplerateparam.replace(keepRateParam,rateParam)]['cuts']:
                    cutToAppend = cut.replace('CR3','CR43').replace('CR4','CR34') if 'CR' in cut and '_mergeRPfull' in opt.tag else cut
                    nuisances[samplerateparam]['cuts'].append(cutToAppend)

            for samplerateparam in removeSampleRateParams:
                del nuisances[samplerateparam]

### Cleaning 

nuisanceToRemove = [ ]

for nuisance in list(nuisances.keys()):

    if 'cuts' in nuisances[nuisance]:
        if len(nuisances[nuisance]['cuts'])==0:
            nuisanceToRemove.append(nuisance)

    if nuisance!='stat' and nuisance not in nuisanceToRemove and 'samples' in nuisances[nuisance]:
        if len(nuisances[nuisance]['samples'])==0:
            nuisanceToRemove.append(nuisance)

    if '_noTreeNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'kind' in nuisances[nuisance] and nuisances[nuisance]['kind']=='tree':
            nuisanceToRemove.append(nuisance)

    if '_noShapeNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='shape':
            nuisanceToRemove.append(nuisance)

    if '_nolnNNuisances' in opt.tag:
        if nuisance not in nuisanceToRemove and 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='lnN':
            nuisanceToRemove.append(nuisance)

    if '_DYsplit' in opt.tag:
        if 'normDY' in nuisance:
            nuisanceToRemove.append(nuisance)
            for mt2llregion in mt2llRegions:
                nuisances[nuisance+'_'+mt2llregion] = {}
                for key in nuisances[nuisance]:
                    nuisances[nuisance+'_'+mt2llregion][key] = nuisances[nuisance][key] 
                nuisances[nuisance+'_'+mt2llregion]['name'] = nuisances[nuisance+'_'+mt2llregion]['name'].replace(nuisance,nuisance+'_'+mt2llregion)
                cutToAdd = []
                for cut in nuisances[nuisance+'_'+mt2llregion]['cuts']:
                    if mt2llregion in cut or mt2llregion.replace('SR','CR') in cut: cutToAdd.append(cut)
                nuisances[nuisance+'_'+mt2llregion]['cuts'] = cutToAdd  

    if '_SplitSR' in opt.tag and 'qqqq' not in opt.tag:
        if '_SR' not in nuisance and nuisance!='stat' and nuisances[nuisance]['type']!='rateParam':
            if 'btag' in nuisance and '_SplitSRnobtag' in opt.tag: continue
            if 'lepIdIso' in nuisance and '_SplitSRnoidiso' in opt.tag: continue
            if 'qq' in opt.tag:
                qqList = opt.tag.split('qq')[1].split('.')
                skipThis = True
                for qqnuis in qqList:
                    if qqnuis in nuisance: skipThis = False
                    elif qqnuis=='normX' and 'norm' in nuisance and 'normDY' not in nuisance: skipThis = False
                if skipThis: continue
            if 'cuts' not in nuisances[nuisance]: nuisances[nuisance]['cuts'] = list(cuts.keys())
            nuisanceToRemove.append(nuisance)
            for mt2llregion in mt2llRegions:
                nuisances[nuisance+'_'+mt2llregion] = {}
                for key in nuisances[nuisance]:
                    nuisances[nuisance+'_'+mt2llregion][key] = nuisances[nuisance][key]
                nuisances[nuisance+'_'+mt2llregion]['name'] = nuisances[nuisance+'_'+mt2llregion]['name'] + '_' + mt2llregion
                cutToAdd = []
                for cut in nuisances[nuisance+'_'+mt2llregion]['cuts']:
                    if mt2llregion in cut or mt2llregion.replace('SR','CR') in cut: cutToAdd.append(cut)
                nuisances[nuisance+'_'+mt2llregion]['cuts'] = cutToAdd

    if '_SplitFlav' in opt.tag and 'qqqq' not in opt.tag:
        if '_em' not in nuisance and '_sf' not in nuisance and nuisance!='stat' and 'CR' not in nuisance:
            if 'btag' in nuisance and 'nobtag' in opt.tag: continue
            if 'lepIdIso' in nuisance and 'noidiso' in opt.tag: continue
            if 'Smooth' in nuisance and 'nojeu' in opt.tag: continue
            if 'normDY' in nuisance and 'nody' in opt.tag: continue
            if 'Topnorm' in nuisance and 'notopnorm' in opt.tag: continue
            if 'WWnorm' in nuisance and 'nowwnorm' in opt.tag: continue
            if 'qq' in opt.tag:
                qqList = opt.tag.split('qq')[1].split('.')
                skipThis = True
                for qqnuis in qqList:
                    if qqnuis in nuisance: skipThis = False
                    elif qqnuis=='normX' and 'norm' in nuisance and 'normDY' not in nuisance: skipThis = False
                if skipThis: continue
            if 'norm' in nuisance and 'nonorm' in opt.tag: continue
            if 'nolep' in opt.tag and 'lep' in nuisance: continue
            if 'IdIsoFS' in nuisance and 'noidisofs' in opt.tag: continue
            if 'cuts' not in nuisances[nuisance]: nuisances[nuisance]['cuts'] = list(cuts.keys())
            nuisanceToRemove.append(nuisance)
            for flav in [ 'em', 'sf']:
                nuisances[nuisance+'__'+flav] = {}
                for key in nuisances[nuisance]:
                    nuisances[nuisance+'__'+flav][key] = nuisances[nuisance][key]
                nuisances[nuisance+'__'+flav]['name'] = nuisances[nuisance+'__'+flav]['name'] + '__' + flav
                if 'correlatedName' in nuisances[nuisance+'__'+flav]:
                    nuisances[nuisance+'__'+flav]['correlatedName'] = nuisances[nuisance+'__'+flav]['correlatedName'] + '__' + flav
                cutToAdd = []
                for cut in nuisances[nuisance+'__'+flav]['cuts']:
                    if flav in cut or 'CR' in cut: cutToAdd.append(cut)
                nuisances[nuisance+'__'+flav]['cuts'] = cutToAdd

    if '_SplitMT2tails' in opt.tag and 'WWtails' in nuisance:
        if '_SplitMT2tailssr' in opt.tag and opt.tag.split('_SplitMT2tails')[1].split('_')[0].upper() in nuisance:
            nuisanceToRemove.append(nuisance)
            for smp in [ 'top', 'WW' ]:
                nuisanceSmp = nuisance.replace('WWtails','WWtails'+'__'+smp)
                nuisances[nuisanceSmp] = {}
                for key in nuisances[nuisance]:
                    if key!='name' and key!='samples':
                        nuisances[nuisanceSmp][key] = nuisances[nuisance][key]
                nuisances[nuisanceSmp]['name'] = nuisances[nuisance]['name'].replace('WWtails','WWtails'+'__'+smp) 
                nuisances[nuisanceSmp]['samples'] = {}
                if smp=='top': 
                    nuisances[nuisanceSmp]['samples']['ttbar'] = nuisances[nuisance]['samples']['ttbar']
                    nuisances[nuisanceSmp]['samples']['STtW']  = nuisances[nuisance]['samples']['STtW']
                elif smp=='WW':
                    nuisances[nuisanceSmp]['samples']['WW'] = nuisances[nuisance]['samples']['WW']
                if 'correlatedName' in nuisances[nuisanceSmp]:
                    nuisances[nuisanceSmp]['correlatedName'] = nuisances[nuisanceSmp]['correlatedName'].replace('WWtails','WWtails'+'__'+smp)

    if '_SplitWWPhi' in opt.tag:
        if 'WWphi' in nuisance:
            nuisanceToRemove.append(nuisance)
            for smp in [ 'WZ', 'WW' ]:
                nuisanceSmp = nuisance.replace('WWphi','WWphi__'+smp)
                nuisances[nuisanceSmp] = {}
                for key in nuisances[nuisance]:
                    if key!='name' and key!='samples':
                        nuisances[nuisanceSmp][key] = nuisances[nuisance][key]
                nuisances[nuisanceSmp]['name'] = nuisances[nuisance]['name'].replace('WWphi','WWphi__'+smp)
                nuisances[nuisanceSmp]['samples'] = {}
            for sample in nuisances[nuisance]['samples']:
                if sample=='ttbar' or sample=='STtW' or sample=='WW': 
                    nuisances[nuisance.replace('WWphi','WWphi__WW')]['samples'][sample] = nuisances[nuisance]['samples'][sample]
                else:
                    nuisances[nuisance.replace('WWphi','WWphi__WZ')]['samples'][sample] = nuisances[nuisance]['samples'][sample]

for nuisance in nuisanceToRemove:
    if nuisance in nuisances: del nuisances[nuisance]

### Nasty tricks ...

nuisanceToRemove = [ ]  

if 'SignalRegion' in opt.tag or 'ValidationRegion' in opt.tag or 'ttZNormalization' in opt.tag or 'SearchRegion' in opt.tag:
        
    if 'SignalRegion' not in opt.tag and 'SearchRegion' not in opt.tag:
        for nuisance in nuisances:
            if nuisance!='stat' and 'norm' in nuisances[nuisance]['name'] and not hasattr(opt, 'outputDirDatacard'):
                nuisanceToRemove.append(nuisance)

    if 'JetUncertainties' in opt.tag:

        nuisanceToDuplicate = []
        for nuisance in nuisances:
            if nuisance!='stat' and 'jesTotal' not in nuisance and 'unclustEn' not in nuisance and 'jer' not in nuisance:
                nuisanceToRemove.append(nuisance)
            elif nuisance!='stat':
                nuisanceToDuplicate.append(nuisance)
                nuisances[nuisance]['cuts'] = []
                for cut in cuts:
                    if 'jesTotal' not in cut and 'unclustEn' not in cut and 'jer' not in cut:
                        nuisances[nuisance]['cuts'].append(cut)
        if not isShape:
            for nuisance in nuisanceToDuplicate:
                nuisances[nuisance+'MET'] = {}
                for key in nuisances[nuisance]:
                    nuisances[nuisance+'MET'][key] = nuisances[nuisance][key]
                nuisances[nuisance+'MET']['name'] = nuisances[nuisance+'MET']['name'].replace(year,'MET'+year)
                    
    if 'SYST' in opt.tag:
        for nuisance in nuisances:
            if nuisance!='stat':
                nuisanceToRemove.append(nuisance)

elif 'unEn' in opt.tag or 'TwoLeptons' in opt.tag or 'FastVsFullFS' in opt.tag:

    for nuisance in nuisances:
        if nuisance!='stat' and 'jes' not in nuisance and 'jer' not in nuisance and 'unclustEn' not in nuisance:
            nuisanceToRemove.append(nuisance)
        elif nuisance!='stat' and 'unEn' in opt.tag and 'FastVsFullFS' not in opt.tag:
            nuisances[nuisance]['cuts'] = [ 'TwoLep' ] 

else:

    for nuisance in nuisances:
        if nuisance!='stat' and 'lumi' not in nuisance: # example ...
            nuisanceToRemove.append(nuisance)

if '_KeepNuis' in opt.tag:
    for nuisance in nuisances:
        if nuisance!='stat' and 'name' in nuisances[nuisance]:
            keepNuis = False
            for nuisToKeep in opt.tag.split('_KeepNuis:')[-1].split('_')[0].split(':'):
                if nuisToKeep in nuisances[nuisance]['name']: 
                    keepNuis = True
                    break
            if not keepNuis: nuisanceToRemove.append(nuisance)

if '_BTV' in opt.tag:
    nuisanceToRemove.append('stat')
    for nuisance in nuisances:
        if 'name' in nuisances[nuisance]:
            if 'mistag' not in nuisances[nuisance]['name'] and 'ctag' not in nuisances[nuisance]['name'] and 'btag' not in nuisances[nuisance]['name']:
                nuisanceToRemove.append(nuisance)

if '_KillSyst' in opt.tag:
    for nuisance in nuisances:
        if nuisance!='stat':
            if nuisances[nuisance]['type']!='rateParam':
                nuisanceToRemove.append(nuisance)

for nuisance in nuisanceToRemove:
    del nuisances[nuisance]

if len(yearstaglist)>1:
  
   nuisanceToRemove = [ ]

   for nuisance in nuisances:
       if 'WWshape' in nuisance or 'WZbin' in nuisance or 'WWtails' in nuisance or 'WWphi' in nuisance: continue
       if 'type' in nuisances[nuisance] and nuisances[nuisance]['type']=='shape':
           if year in nuisances[nuisance]['name']:
               nuisanceToRemove.append(nuisance)

   for nuisance in nuisanceToRemove:

       for ytag in yearstaglist:
           nuisances[nuisance+'_'+ytag] = nuisances[nuisance].copy()
           nuisances[nuisance+'_'+ytag]['name'] = nuisances[nuisance+'_'+ytag]['name'].replace(year, '_'+ytag)

       del nuisances[nuisance]


   #for nuisance in sorted (nuisances.keys()):
   #    print nuisance
   #    if nuisance!='stat':
   #       print '             ', nuisances[nuisance]['name']

   #exit()


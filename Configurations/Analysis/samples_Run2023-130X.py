import os
import subprocess
import math
import string
from LatinoAnalysis.Tools.commonTools import *
from collections import OrderedDict

### Generals

opt.campaign = 'Summer23BPix' if 'Summer23BPix' in opt.tag else 'Summer23'

opt.CME = '13.6'
opt.lumi = 1. if 'Validation' in opt.tag else 9.451 if 'Summer23BPix' in opt.campaign else 17.650

# https://github.com/cms-sw/cmssw/blob/master/SimGeneral/MixingModule/python/
opt.simulationPileupFile = 'pileup_DistrWinter22_Run3_2022_LHC_Simulation_10h_2h.root'
if 'Summer23BPix' in opt.campaign: 
    opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_13_3_1/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2023/2023D.root'
    opt.simulationPileupList = [ 0.000158878446531, 3.72079495004e-05, 4.81640545476e-05, 4.57853820338e-05, 4.48623875183e-05, 5.84446325801e-05, 6.21371953105e-05, 7.03017263882e-05, 8.14053877829e-05, 8.70272731863e-05, 8.31197017269e-05, 9.10479801679e-05, 0.000157953009035, 0.000116574062554, 0.000129294975462, 0.000144545642223, 0.000217078041821, 0.000440232973883, 0.000773662434135, 0.00110283621902, 0.00142257438371, 0.00176809978781, 0.00208600425923, 0.00241950256675, 0.00296346767304, 0.00376702592516, 0.00484406195225, 0.00613147621346, 0.00769025671271, 0.00948861093862, 0.0109925387243, 0.0123667087551, 0.013627393454, 0.0146345506473, 0.015512752756, 0.0165376249303, 0.0175929813666, 0.018477824153, 0.0192112990472, 0.0196645289817, 0.0201161023712, 0.0206504959528, 0.020879696658, 0.0210625541872, 0.0212334411744, 0.0213619175725, 0.0217040066936, 0.022158015445, 0.0228131566405, 0.0238090615222, 0.0245709343881, 0.0255676600477, 0.0269068441176, 0.0282418222377, 0.0301095236733, 0.0322607862482, 0.0340215193181, 0.0351963407371, 0.0355890314646, 0.0353316943073, 0.0341387294252, 0.0328144650238, 0.0308479015762, 0.0279916459339, 0.0248514911256, 0.0219924532015, 0.0191273076414, 0.0162191660774, 0.0134212379857, 0.0108569317827, 0.00894075906105, 0.00721689444201, 0.00577376618889, 0.0045988410223, 0.00345625399226, 0.00268987667653, 0.00203585450746, 0.00148498442583, 0.00104550889127, 0.000680880800731, 0.000378259194695, 0.000208622992464, 0.000137403591797, 9.84678907631e-05, 6.66619364389e-05, 4.98540448905e-05, 3.6916797972e-05, 2.83299393313e-05, 2.35951729274e-05, 1.47733031993e-05, 1.30753995144e-05, 1.17148517026e-05, 7.73674081622e-06, 4.60860216753e-06, 3.2973125953e-07, 1.89267830307e-07, 6.32999965354e-08, 0.0, 0.0, 0.0 ] 
    opt.simulationPileupFile = 'mix_2023_25ns_EraD_PoissonOOTPU_cfi.root'

elif 'Summer23' in opt.campaign: 
    opt.dataPileupFile = '/afs/cern.ch/work/s/scodella/BTagging/CMSSW_13_3_1/src/LatinoAnalysis/NanoGardener/python/data/PUweights/2023/2023C.root'
    opt.simulationPileupList = [ 2.38822148706e-05, 4.75152134008e-05, 6.30191527793e-05, 6.68452240771e-05, 8.1025250051e-05, 9.79468565963e-05, 9.95081424719e-05, 9.33708830231e-05, 9.50909917671e-05, 0.000100651134241, 0.000103078257098, 0.000111034560318, 0.000122287617571, 0.000133124512985, 0.00014956573019, 0.000186137627395, 0.000228156756843, 0.000282331058406, 0.000331622711531, 0.000391461449341, 0.000517949289644, 0.000772840072265, 0.00117177950147, 0.00170218286606, 0.00236820136292, 0.00313598312592, 0.00408745219886, 0.00527840094237, 0.00673298586987, 0.00828009786211, 0.00981421228066, 0.0113605372864, 0.0128822615559, 0.0143533259986, 0.0156697830309, 0.0169254217283, 0.018080221643, 0.0189942713703, 0.0198224792894, 0.0205857576279, 0.0212350460744, 0.0217526935632, 0.022272803428, 0.0228031352959, 0.0231877786772, 0.0236794597607, 0.0242098757217, 0.0250255926642, 0.0259084771241, 0.0270883359038, 0.0283842141201, 0.0296138041433, 0.0312398518545, 0.0328769694128, 0.0343573284679, 0.0359444082242, 0.0371707283039, 0.0379191373689, 0.0376984798185, 0.0364701631509, 0.0342333461199, 0.030918081708, 0.02719246186, 0.0234422219723, 0.0199428306976, 0.0167530883095, 0.0139446903019, 0.0115684641268, 0.0095875821463, 0.00792109671955, 0.00642645801884, 0.00514147006535, 0.004014647174, 0.00312068891816, 0.00254047982771, 0.00206998047115, 0.00170256713492, 0.00142457093791, 0.00112986818813, 0.000874387606181, 0.000666515127689, 0.000479354340271, 0.000316491543232, 0.000182306321277, 9.7983507813e-05, 5.59397929391e-05, 3.25116880719e-05, 2.05226891643e-05, 1.08317242834e-05, 4.61503191047e-06, 1.49869506368e-06, 3.4791503138e-07, 1.59930964479e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    opt.simulationPileupFile = 'mix_2023_25ns_EraC_PoissonOOTPU_cfi.root'

fragTune = 'fragCP5BL'
jetEnergyUncertaintyFile = 'Summer23BPixPrompt23_V1_MC_Uncertainty_AK4PFPuppi.txt' if 'Summer23BPix' in opt.campaign else 'Summer23Prompt23_V1_MC_Uncertainty_AK4PFPuppi.txt'

treePrefix = ''

opt.method = 'System8' if 'System8' in opt.tag else 'PtRel'

### Process utilities

isDatacardOrPlot = hasattr(opt, 'outputDirDatacard') or hasattr(opt, 'postFit') or hasattr(opt, 'skipLNN') or hasattr(opt, 'inputDirMaxFit')
isPlot = hasattr(opt, 'postFit')
isShape = hasattr(opt, 'doHadd')
isFillShape = isShape and not opt.doHadd
opt.isShape = isShape

bIsSignal = opt.method=='PtRel' and not isPlot
if hasattr(opt, 'action') and opt.action=='plotNuisances': bIsSignal = False

if isFillShape and 'MergedLight' in opt.tag:
    print('Cannot fill shapes for', opt.tag, 'directly from trees')
    exit()

### Directories

skipTreesCheck = False if isShape or 'PtHatWeights' in opt.tag else True

if opt.sigset=='SM' and isFillShape:
    print('Error: SM cannot be used when filling the shapes. Use Data and MC separately instead') 

SITE=os.uname()[1]
if 'cern' not in SITE and 'ifca' not in SITE and 'cloud' not in SITE: SITE = 'cern'

if 'cern' in SITE:
    treeBaseDirMC   = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons'
    treeBaseDirData = '/eos/cms/store/group/phys_btag/milee/BTA_addPFMuons'
else: print('trees for', campaign, 'campaign available only at cern')

ProductionMC   = opt.campaign
ProductionData = opt.campaign
  
directoryBkg  = '/'.join([ treeBaseDirMC,   ProductionMC  , '' ])
directoryData = '/'.join([ treeBaseDirData, ProductionData, '' ])

### Campaign parameters

# global parameters
minJetPt  =   20.
maxJetPt  = 1400.
maxJetEta = '2.5'
minPlotPt =   20.
maxPlotPt = 1000.

campaignRunPeriod = { 'year' : '2023' }
campaignRunPeriod['period']    = '2023D' if 'Summer23BPix' in opt.campaign else '2023C'
campaignRunPeriod['pileup']    = opt.campaign
campaignRunPeriod['prescales'] = opt.campaign

ptrelRange = (50, 0., 4.) if opt.method=='PtRel' else (70, 0., 7.)

# triggers
triggerInfos = { 'BTagMu_AK4DiJet20_Mu5'  : { 'jetPtRange' : [  '20.',   '50.' ], 'ptAwayJet' : '20.', 'ptTriggerEmulation' :  '30.', 'jetTrigger' :  'PFJet40', 'idx' : '32', 'idxJetTrigger' : '0' },
                 'BTagMu_AK4DiJet40_Mu5'  : { 'jetPtRange' : [  '50.',  '100.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '50.', 'jetTrigger' :  'PFJet40', 'idx' : '33', 'idxJetTrigger' : '0' },
                 'BTagMu_AK4DiJet70_Mu5'  : { 'jetPtRange' : [ '100.',  '140.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :  '80.', 'jetTrigger' :  'PFJet60', 'idx' : '34', 'idxJetTrigger' : '1' },
                 'BTagMu_AK4DiJet110_Mu5' : { 'jetPtRange' : [ '140.',  '200.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '140.', 'jetTrigger' :  'PFJet80', 'idx' : '35', 'idxJetTrigger' : '2' },
                 'BTagMu_AK4DiJet170_Mu5' : { 'jetPtRange' : [ '200.',  '320.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' : '200.', 'jetTrigger' : 'PFJet140', 'idx' : '36', 'idxJetTrigger' : '3' },
                 'BTagMu_AK4Jet300_Mu5'   : { 'jetPtRange' : [ '320.', '1400.' ], 'ptAwayJet' : '30.', 'ptTriggerEmulation' :   '0.', 'jetTrigger' : 'PFJet260', 'idx' : '37', 'idxJetTrigger' : '5' },
                }

# b-tagging algorithms and working points

bTagAlgorithms = [ 'DeepJet', 'ParticleNet', 'ParT' ]
workingPointName = [ 'Loose', 'Medium', 'Tight', 'eXtraTight', 'eXtraeXtraTight' ]
workingPointLimit = [ 0.1, 0.01, 0.001, 0.0005, 0.0001 ]

if opt.campaign=='Summer23BPix':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.6563', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXT': {'cut': '0.7544', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0683', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.1919', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0359', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.3494', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.7994', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6133', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.2435', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.048', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXXT': {'cut': '0.9688', 'discriminant': 'PNetBDisc'}, 'ParTXXT': {'cut': '0.9883', 'discriminant': 'ParTBDisc'}, 'ParTXT': {'cut': '0.8877', 'discriminant': 'ParTBDisc'}, 'DeepJetXXT': {'cut': '0.9483', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetXT': {'cut': '0.7671', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '2.551',  'AwayJetDown' : '1.215' , 'AwayJetUp' : '5.173' }

elif opt.campaign=='Summer23':
    bTagWorkingPoints = {'DeepJetT': {'cut': '0.6553', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXT': {'cut': '0.7515', 'discriminant': 'PNetBDisc'}, 'ParTL': {'cut': '0.0681', 'discriminant': 'ParTBDisc'}, 'ParticleNetM': {'cut': '0.1917', 'discriminant': 'PNetBDisc'}, 'ParticleNetL': {'cut': '0.0358', 'discriminant': 'PNetBDisc'}, 'ParTM': {'cut': '0.3487', 'discriminant': 'ParTBDisc'}, 'ParTT': {'cut': '0.7969', 'discriminant': 'ParTBDisc'}, 'ParticleNetT': {'cut': '0.6172', 'discriminant': 'PNetBDisc'}, 'DeepJetM': {'cut': '0.2431', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetL': {'cut': '0.0479', 'discriminant': 'DeepFlavourBDisc'}, 'ParticleNetXXT': {'cut': '0.9659', 'discriminant': 'PNetBDisc'}, 'ParTXXT': {'cut': '0.9883', 'discriminant': 'ParTBDisc'}, 'ParTXT': {'cut': '0.8882', 'discriminant': 'ParTBDisc'}, 'DeepJetXXT': {'cut': '0.9459', 'discriminant': 'DeepFlavourBDisc'}, 'DeepJetXT': {'cut': '0.7667', 'discriminant': 'DeepFlavourBDisc'}}
    btagAwayJetTagger, btagAwayJetDiscriminant = 'JBP', 'Bprob'
    btagAwayJetVariations = { 'AwayJetTag' : '2.555',  'AwayJetDown' : '1.221' , 'AwayJetUp' : '5.134' }

if 'WorkingPoints' in opt.tag:
    bTagWorkingPoints[btagAwayJetTagger+'L'] = {'cut': btagAwayJetVariations['AwayJetDown'], 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'M'] = {'cut': btagAwayJetVariations['AwayJetTag'] , 'discriminant': btagAwayJetDiscriminant}
    bTagWorkingPoints[btagAwayJetTagger+'T'] = {'cut': btagAwayJetVariations['AwayJetUp']  , 'discriminant': btagAwayJetDiscriminant}

if 'PtRelTemplates' in opt.tag:
    if btagAwayJetTagger+'T' not in bTagWorkingPoints:
        bTagWorkingPoints[btagAwayJetTagger+'T'] = {'cut': btagAwayJetVariations['AwayJetUp']  , 'discriminant': btagAwayJetDiscriminant}

if 'btag' in opt.tag:
    btagWPToRemove = []
    for btagwp in bTagWorkingPoints:
        if 'btagveto' in opt.tag:
           if opt.tag.split('btagveto')[1].split('_')[0] in btagwp:
               btagWPToRemove.append(btagwp)
        elif opt.tag.split('btag')[1].split('_')[0] not in btagwp:
           btagWPToRemove.append(btagwp)
    for btagwp in btagWPToRemove:
        del bTagWorkingPoints[btagwp]

# jet pt bins
if 'ProdFine' in opt.tag or 'Validation' in opt.tag:
    jetPtBins = { 'Pt20to30'    : [   '20.',   '30.' ], 'Pt30to40'     : [   '30.',   '40.' ], 'Pt40to50'    : [   '40.',   '50.' ], 'Pt50to60'     : [   '50.',   '60.' ], 
                  'Pt60to70'    : [   '60.',   '70.' ], 'Pt70to80'     : [   '70.',   '80.' ], 'Pt80to100'   : [   '80.',  '100.' ], 'Pt100to120'   : [  '100.',  '120.' ], 
                  'Pt120to140'  : [  '120.',  '140.' ], 'Pt140to160'   : [  '140.',  '160.' ], 'Pt160to200'  : [  '160.',  '200.' ], 'Pt200to260'   : [  '200.',  '260.' ], 
                  'Pt260to300'  : [  '260.',  '300.' ], 'Pt300to320'   : [  '300.',  '320.' ], 'Pt320to400'  : [  '320.',  '400.' ], 'Pt400to500'   : [  '400.',  '500.' ], 
                  'Pt500to600'  : [  '500.',  '600.' ], 'Pt600to800'   : [  '600.',  '800.' ], 'Pt800to1000' : [  '800.', '1000.' ], 'Pt1000to1400' : [ '1000.', '1400.' ], 
                 }
elif 'ProdRun2' in opt.tag or ('Templates' in opt.tag and 'Prod' not in opt.tag):
    jetPtBins = { 'Pt20to30'    : [   '20.',   '30.' ], 'Pt30to50'     : [   '30.',   '50.' ], 'Pt50to70'    : [   '50.',   '70.' ], 'Pt70to100'    : [   '70.',  '100.' ], 
                  'Pt100to140'  : [  '100.',  '140.' ], 'Pt140to200'   : [  '140.',  '200.' ], 'Pt200to300'  : [  '200.',  '300.' ], 'Pt300to600'   : [  '300.',  '600.' ], 
                  'Pt600to1000' : [  '600.', '1000.' ], 'Pt1000to1400' : [ '1000.', '1400.' ], 
                 }
elif opt.method+'Data' in opt.tag:
    jetPtBins = { }
    for trigger in triggerInfos:
        jetPtBins[trigger] = [ str(minJetPt), str(maxJetPt) ] 
else: 
    jetPtBins = { }
    for trigger in triggerInfos:
        jetPtBins[trigger] = triggerInfos[trigger]['jetPtRange']

if 'JetPt' in opt.tag:
    ptBinToRemove = []
    for ptbin in jetPtBins:
        if 'JetPtVeto' in opt.tag:
           if ptbin in 'Pt'+opt.tag.split('JetPtVeto')[1].split('_')[0]:
               ptBinToRemove.append(ptbin)
        elif ptbin not in 'Pt'+opt.tag.split('JetPt')[1].split('_')[0]:
           ptBinToRemove.append(ptbin)
    for ptbin in ptBinToRemove:
        del jetPtBins[ptbin]

# systematics

csvSystematics = OrderedDict()
csvSystematics['central'] = 'Final'
for variation in [ 'Up', 'Down' ]:
    csvSystematics[variation.lower()]                   = 'Final'+variation
    csvSystematics[variation.lower()+'_statistic']      = 'Statistics'+variation
    csvSystematics[variation.lower()+'_jetaway']        = 'AwayJet'+variation
    csvSystematics[variation.lower()+'_mupt']           = 'MuPt'+variation
    csvSystematics[variation.lower()+'_mudr']           = 'MuDR'+variation
    csvSystematics[variation.lower()+'_jes']            = 'JEU'+variation
    csvSystematics[variation.lower()+'_pileup']         = 'pileup'+variation
    csvSystematics[variation.lower()+'_gluonsplitting'] = 'gluonSplitting'+variation
    csvSystematics[variation.lower()+'_bfragmentation'] = 'bfragmentation'+variation
    csvSystematics[variation.lower()+'_bdecays']        = 'bdecays'+variation
    csvSystematics[variation.lower()+'_btempcorr']      = 'CorrB'+variation
    csvSystematics[variation.lower()+'_cjets']          = 'cjets'+variation
    csvSystematics[variation.lower()+'_l2c']            = 'lightCharmRatio'+variation
    csvSystematics[variation.lower()+'_ltempcorr']      = 'CorrL'+variation

systematicVariations = [ '' ]

if 'Templates' in opt.tag:
    systematicVariations.extend([ 'MuPtUp', 'MuPtDown', 'MuDRUp', 'MuDRDown' ])
    if ('Validation' not in opt.tag and ('SM' in opt.sigset or 'MC' in opt.sigset) and ('ForFit' not in opt.tag or '_nuisSelections' in opt.tag)) or '_selJEU' in opt.tag: 
        systematicVariations.extend([ 'JEUUp', 'JEUDown' ])
    if 'Light' not in opt.tag:
        systematicVariations.insert(1, 'AwayJetDown')
        systematicVariations.insert(1, 'AwayJetUp')

systematicNuisances = []

applyBFragmentation = 1

if 'NoPU' not in opt.tag and 'Validation' not in opt.tag: systematicNuisances.append('pileup')
systematicNuisances.append('gluonSplitting')
if applyBFragmentation>=1: systematicNuisances.append('bfragmentation')
systematicNuisances.append('bdecay')
if opt.method=='PtRel': systematicNuisances.append('lightCharmRatio')

if 'Templates' in opt.tag and 'ForFit' in opt.tag and '_nuisSelections' in opt.tag: 
    if '_noselrefit' in opt.tag or '_norefit' in opt.tag: systematicVariations = [ 'JEUUp', 'JEUDown' ]
    for nuisance in systematicNuisances:
        systematicVariations.append(nuisance+'Up')
        systematicVariations.append(nuisance+'Down')

# Template corrections

templateTreatments = [ 'corr', 'nuis', 'syst' ]
bTemplateCorrector = {}
for btagWP in bTagWorkingPoints: bTemplateCorrector[btagWP] = 'ParTT' if 'DeepJet' in btagWP else 'DeepJetT'

if 'PtRelTemplates' in opt.tag and 'ForFit' in opt.tag:
    
   templateTreatmentFlag = opt.tag.split('Templates')[1].split('2D')[0].split('ForFit')[0]

   templateCorrectionNuisances = {}   
   if 'Nuis' in templateTreatmentFlag:
       for flavour in templateTreatmentFlag.split('Nuis')[1].split('Syst')[0]:
           templateCorrectionNuisances['Corr'+flavour] = flavour.lower()+'jets'

   if 'Syst' in templateTreatmentFlag and 'nocorrrefit' not in opt.tag and 'norefit' not in opt.tag:
       for flavour in templateTreatmentFlag.split('Syst')[1]:
           systematicVariations.append('Corr'+flavour) 

if '_sel' in opt.tag:
    selectionToRemove = []
    for tagoption in opt.tag.split('_'):
        if 'sel' in tagoption:
            for selection in systematicVariations:
               sel = 'Central' if selection=='' else selection
               if 'veto' in tagoption:
                   if sel in tagoption: selectionToRemove.append(selection)
               elif sel not in tagoption: selectionToRemove.append(selection)
            for nuisance in systematicNuisances:
                for variation in [ 'Up', 'Down' ]:
                    if nuisance+variation in tagoption: systematicVariations.append(nuisance+variation)
    for selection in selectionToRemove:
        systematicVariations.remove(selection)

# muon kinematics selection
  
if 'PtRel' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt),         '30.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.20', '0.15', '999.' ] },
                    'Bin2' : { 'range' : [         '30.',         '80.' ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.15', '0.12', '999.' ] },
                    'Bin3' : { 'range' : [         '80.', str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.12', '0.09', '999.' ] } }

elif 'System8' in opt.method:
    muonKinBins = { 'Bin1' : { 'range' : [ str(minJetPt), str(maxJetPt) ], 'pt' : [ '5.', '6.', '8.' ], 'dr' : [ '0.40', '0.30', '999.' ] } }

muonKinSelection = 'Central'
for systvar in systematicVariations:
    if 'Mu' in systvar and systvar in opt.tag: muonKinSelection = systvar

# pt-hat safety thresholds

if 'Light' not in opt.tag:
    pthatThresholds = {  20. :  60.,  30. :  85.,  50. : 120.,  80. : 160., 120. : 220., 
                        170. : 320., 300. : 440., 470. : 620., 600. : 720., 800. : 920. }
else:
    #pthatThresholds = {  30. : 200.,  50. : 200.,  80. : 200., 120. : 250., 170. : 340., 300. : 520. }
    pthatThresholds = {  80. : 200., 120. : 250., 170. : 340., 300. : 520. }

# kinematic weights setting
kinematicWeightsMap = { 'QCDMu'  : [ 'QCDMu', 'bjets', 'cjets', 'ljets', 'light' ],
                        'QCD'    : [ 'QCD' ],
                        'Jet'    : [ 'Jet' ]
                       }

### Complex variables

# event
nJetMax = 20
goodPV  = 'PV_chi2<100.' # No nPV so far in the trees

# working points
jetPt   = 'Jet_pT'
if 'RawPt'   in opt.tag: jetPt = 'Jet_uncorrpt'
if 'JEUDown' in opt.tag: jetPt = 'jetEnDown'
elif 'JEUUp' in opt.tag: jetPt = 'jetEnUp'
goodJetForDisc = '((JETIDX<nJet)*(Alt$('+jetPt+'[JETIDX],0.)>=30.)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$(Jet_hadronFlavour[JETIDX],-1)==JETFLV)*(Alt$(Jet_tightID[JETIDX],0)==1))'
jetDisc = '(999999.*(!('+goodJetForDisc+')) + '+goodJetForDisc+'*(Alt$(Jet_BTAGDISC[JETIDX],999999.)))'

# kinematic weights
jetKinematicWeight = '1.'
if '.' in opt.tag:
    jetKinematicWeightList = []
    for x in opt.tag.split('.'):
        if opt.method not in x: jetKinematicWeightList.append('Alt$('+x+'[JETIDX],1.)')
    jetKinematicWeight = '*'.join(jetKinematicWeightList)
# This does not work in python3
#jetKinematicWeight = '*'.join([ 'Alt$('+x+'[JETIDX],1.)' for x in opt.tag.split('.') if opt.method not in x ]) if '.' in opt.tag else '1.'

# mu-jet
jetSel      = 'Jet_tightID==1 && abs(Jet_eta)<='+maxJetEta+' && '+jetPt+'>='+str(minJetPt)
#  muSel       = 'PFMuon_GoodQuality>=2 && PFMuon_pt>5. && abs(PFMuon_eta)<2.4 && PFMuon_IdxJet>=0'
#  muJetEvt    = 'Sum$('+muSel+')==1'
#  muPt        = 'Sum$(('+muSel+')*PFMuon_pt)'
#  muEta       = 'Sum$(('+muSel+')*PFMuon_eta)'
#  muPhi       = 'Sum$(('+muSel+')*PFMuon_phi)'
#  muPtRel     = 'Sum$(('+muSel+')*PFMuon_ptrel)'
#  muJetIdx    = 'Sum$(('+muSel+')*PFMuon_IdxJet)'
muJetEvt    = 'muonJetFinder[0]>=0'
muIdx       = 'abs(muonJetFinder[0])'
muPt        = 'PFMuon_pt['+muIdx+']'
muEta       = 'PFMuon_eta['+muIdx+']'
muPhi       = 'PFMuon_phi['+muIdx+']'
muPtRel     = 'PFMuon_ptrel['+muIdx+']'
muJetIdx    = 'abs(muonJetFinder[1])'
muJetPt     = jetPt+'['+muJetIdx+']'
muJetEta    = 'Jet_eta['+muJetIdx+']'
muJetPhi    = 'Jet_phi['+muJetIdx+']'
muJetSel    = muJetIdx+'>=0 && Jet_tightID['+muJetIdx+']==1 && abs('+muJetEta+')<='+maxJetEta
muJetDR     = 'sqrt(acos(cos('+muPhi+'-'+muJetPhi+'))*acos(cos('+muPhi+'-'+muJetPhi+'))+('+muEta+'-'+muJetEta+')*('+muEta+'-'+muJetEta+'))'
muJetKinematicWeight = jetKinematicWeight.replace('JETIDX',muJetIdx)

# away jet
awayDeltaPhi = 'acos(cos(Jet_phi-Jet_phi['+muJetIdx+']))'
awayDeltaEta = '(Jet_eta-Jet_eta['+muJetIdx+'])'
awayDeltaR   = 'sqrt('+awayDeltaPhi+'*'+awayDeltaPhi+'+'+awayDeltaEta+'*'+awayDeltaEta+')'

awayJetTagSelection = 'AwayJetTag'
for systvar in systematicVariations:
    if 'AwayJet' in systvar and systvar in opt.tag: awayJetTagSelection = systvar

if 'PtRel' in opt.method:
    awayJetNCut     = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations[awayJetTagSelection]+')==1'
    awayJetPtCut    = 'Sum$('+jetSel+' && '+awayDeltaR+'>1.5 && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations[awayJetTagSelection]+' && '+jetPt+'>=AWAYJETPTCUT)==1'
    awayJetLightCut = 'Sum$('+jetSel+' && '+awayDeltaR.replace(muJetIdx,'JETIDX')+'>1.5 && '+jetPt+'>=AWAYJETPTCUT)>=1'
    awayJetCut      = awayJetNCut+' && '+awayJetPtCut

elif 'System8' in opt.method: # Not sure System8 does really this
    #awayJetCut = 'Sum$('+jetSel+' && '+jetPt+'>=AWAYJETPTCUT && '+awayDeltaR+'>0.05 && Jet_'+btagAwayJetDiscriminant+'>=-999999.)>=1'
    #awayJetCand = [ '('+str(ijet)+'<nJet && Alt$(Jet_tightID['+str(ijet)+'],0)==1 && abs(Alt$(Jet_eta['+str(ijet)+'],5.))<='+maxJetEta+' && '+str(ijet)+'!='+muJetIdx+' && Alt$('+jetPt+'['+str(ijet)+'],0.)>=AWAYJETPTCUT && Alt$(Jet_'+btagAwayJetDiscriminant+'['+str(ijet)+'],-9999999.)>=-999999. && Sum$('+jetSel+' && '+jetPt+'!='+muJetPt+' && '+jetPt+'>'+jetPt+'['+str(ijet)+'])==0)' for ijet in range(5) ]
    awayJetCand = []
    for ijet in range(5):
        awayJetCand.append( '('+str(ijet)+'<nJet && Alt$(Jet_tightID['+str(ijet)+'],0)==1 && abs(Alt$(Jet_eta['+str(ijet)+'],5.))<='+maxJetEta+' && '+str(ijet)+'!='+muJetIdx+' && Alt$('+jetPt+'['+str(ijet)+'],0.)>=AWAYJETPTCUT && Alt$(Jet_'+btagAwayJetDiscriminant+'['+str(ijet)+'],-9999999.)>=-999999. && Sum$('+jetSel+' && '+jetPt+'!='+muJetPt+' && '+jetPt+'>'+jetPt+'['+str(ijet)+'])==0)' )
    awayJetCut = '('+' || '.join(awayJetCand )+')'   

# trigger
bitIdx      = 'int(triggerIdx/32)'
triggerCut  = '( BitTrigger['+bitIdx+'] & ( 1 << (triggerIdx - '+bitIdx+'*32) ) )>0'
triggerEmul = 'Sum$('+jetSel+' && '+awayDeltaR+'>0.05 && '+jetPt+'>=TRGEMULJETPTCUT)>=1' 

# light jets
lightJetSel = '((JETIDX<nJet)*(Alt$(Jet_tightID[JETIDX],0)==1)*(abs(Alt$(Jet_eta[JETIDX],5.))<'+maxJetEta+')*(Alt$('+jetPt+'[JETIDX],-1.)>=PTMIN)*(Alt$('+jetPt+'[JETIDX],999999.)<PTMAX)*(Sum$(PFMuon_GoodQuality>=1 && PFMuon_IdxJet==JETIDX)==0)*(Sum$(Jet_tightID==1 && '+jetPt+'!='+jetPt+'[JETIDX] && Jet_'+btagAwayJetDiscriminant+'>='+btagAwayJetVariations['AwayJetDown']+')==0))'
lightJetPt     = 'Alt$('+jetPt+'[JETIDX],-999.)'
lightJetEta    = 'Alt$(Jet_eta[JETIDX],-999.)'

# light tracks
nLightTrkMax  = 50
trackJetIdx   = 'TrkInc_jetIdx'
trakPt        = 'TrkInc_pt'
trackJetDR    = muJetDR.replace(muJetIdx,'JETIDX').replace(muPhi,'TrkInc_phi[TRKIDX]').replace(muEta,'TrkInc_eta[TRKIDX]')
lightTrkPtRel = 'Alt$(TrkInc_ptrel[TRKIDX],-999.)'
lightTrkSel   = '((TRKIDX<nTrkInc)*(Alt$('+trackJetIdx+'[TRKIDX],-1)>=0)*(Alt$('+trakPt+'[TRKIDX],0.)>TRKPTCUT)*(abs(Alt$(TrkInc_eta[TRKIDX],5.))<2.4)*('+trackJetDR+'<TRKDRCUT))'
nLightTrkJet  = 'Sum$('+trackJetIdx+'==JETIDX && '+trakPt+'>TRKPTCUT && abs(TrkInc_eta)<2.4 && '+trackJetDR.replace('[TRKIDX]','')+'<TRKDRCUT)'

# generation weights
muJetFromB    = '(Jet_hadronFlavour['+muJetIdx+']==5)'
muJetFromC    = '(Jet_hadronFlavour['+muJetIdx+']==4)'
muJetFromL    = '(Jet_hadronFlavour['+muJetIdx+']<4)'
muJetNotFromB = '(Jet_hadronFlavour['+muJetIdx+']!=5)'

# gluon splitting
BHadronDeltaR    = 'sqrt(acos(cos(BHadron_phi-Jet_phi['+muJetIdx+']))*acos(cos(BHadron_phi-Jet_phi['+muJetIdx+']))+(BHadron_eta-Jet_eta['+muJetIdx+'])*(BHadron_eta-Jet_eta['+muJetIdx+']))'
isGluonSplitting = '(Sum$('+BHadronDeltaR+'<=0.4 && BHadron_hasBdaughter==0)>=2)' 

### MC

if 'SM' in opt.sigset or 'MC' in opt.sigset:

    qcdMuName = 'QCD_PT-PTHATBIN_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8'
    qcdName   = 'QCD_PT-PTHATBIN_TuneCP5_13p6TeV_pythia8'
    ttbarName = 'TTto4Q_TuneCP5_13p6TeV_powheg-pythia8'

    if opt.campaign=='Summer23BPix':
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '26692302', 'weight': '3.616979906791104'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '33019106', 'weight': '0.2345279124153149'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '31598705', 'weight': '0.022199076829256134'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '22802000', 'weight': '0.0009314340847294096'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '41002587', 'weight': '9.628031519084393e-05'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '22380325', 'weight': '1.036494599609255'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '12720414', 'weight': '27.29400159460219'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '31914516', 'weight': '46.58453852159312'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '22833444', 'weight': '0.002931570900999429'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '4999753', 'weight': '580.5726802904063'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '33189564', 'weight': '75.89117470780876'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '15340005', 'weight': '8.68502650422865e-05'}}
        qcdPtHatBins = {'80to120': {'ext': '', 'xSec': '2762530*1', 'events': '8967000', 'weight': '308.0773948923832'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '8688750', 'weight': '2210.2488850525106'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '17354000', 'weight': '0.45078944335599863'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '20342000', 'weight': '0.009187887130075706'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '5976000', 'weight': '0.001576020749665328'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '11908000', 'weight': '0.0027118743701713133'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '8964000', 'weight': '52.554663096831774'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '1794000', 'weight': '0.0004697045707915273'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '900000', 'weight': '0.00012771444444444445'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '581000', 'weight': '1.175526678141136e-05'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '240000', 'weight': '6.893541666666667e-07'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '5988000', 'weight': '3207.130928523714'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '1199270', 'weight': '95141.2109032995'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '8382000', 'weight': '0.07733237890718206'}, '15to30': {'ext': '', 'xSec': '1327600000', 'events': '1198520', 'weight': '1107699.4960451224'}}
 
    elif opt.campaign=='Summer23':
        qcdMuPtHatBins = {'80to120': {'ext': '', 'xSec': '2536000*0.03807', 'events': '26526706', 'weight': '3.639559318069873'}, '170to300': {'ext': '', 'xSec': '114200*0.06781', 'events': '32267222', 'weight': '0.23999283235476543'}, '300to470': {'ext': '', 'xSec': '7678*0.09136', 'events': '31532825', 'weight': '0.02224545628246121'}, '600to800': {'ext': '', 'xSec': '180.6*0.1176', 'events': '22710862', 'weight': '0.0009351719014452203'}, '800to1000': {'ext': '', 'xSec': '30.89*0.1278', 'events': '40933077', 'weight': '9.64438124209426e-05'}, '120to170': {'ext': '', 'xSec': '444900*0.05214', 'events': '21827015', 'weight': '1.0627695083363438'}, '50to80': {'ext': '', 'xSec': '15710000*0.0221', 'events': '12720414', 'weight': '27.29400159460219'}, '30to50': {'ext': '', 'xSec': '114100000*0.01303', 'events': '31914516', 'weight': '46.58453852159312'}, '470to600': {'ext': '', 'xSec': '630.3*0.1062', 'events': '22598146', 'weight': '0.00296209520904945'}, '15to20': {'ext': '', 'xSec': '907100000*0.0032', 'events': '4999753', 'weight': '580.5726802904063'}, '20to30': {'ext': '', 'xSec': '420500000*0.00599', 'events': '33189564', 'weight': '75.89117470780876'}, '1000': {'ext': '', 'xSec': '9.935*0.1341', 'events': '15219182', 'weight': '8.753975739300575e-05'}}
        qcdPtHatBins = {'80to120': {'ext': '', 'xSec': '2762530*1', 'events': '8967000', 'weight': '308.0773948923832'}, '170to300': {'ext': '', 'xSec': '19204300', 'events': '8602750', 'weight': '2232.344308506001'}, '300to470': {'ext': '', 'xSec': '7823', 'events': '17354000', 'weight': '0.45078944335599863'}, '600to800': {'ext': '', 'xSec': '186.9', 'events': '20084000', 'weight': '0.009305915156343358'}, '1000to1400': {'ext': '', 'xSec': '9.4183', 'events': '5976000', 'weight': '0.001576020749665328'}, '800to1000': {'ext': '', 'xSec': '32.293', 'events': '11908000', 'weight': '0.0027118743701713133'}, '120to170': {'ext': '', 'xSec': '471100', 'events': '8964000', 'weight': '52.554663096831774'}, '1400to1800': {'ext': '', 'xSec': '0.84265', 'events': '1794000', 'weight': '0.0004697045707915273'}, '1800to2400': {'ext': '', 'xSec': '0.114943', 'events': '900000', 'weight': '0.00012771444444444445'}, '2400to3200': {'ext': '', 'xSec': '0.00682981', 'events': '581000', 'weight': '1.175526678141136e-05'}, '3200': {'ext': '', 'xSec': '0.000165445', 'events': '240000', 'weight': '6.893541666666667e-07'}, '50to80': {'ext': '', 'xSec': '19204300', 'events': '5988000', 'weight': '3207.130928523714'}, '30to50': {'ext': '', 'xSec': '114100000', 'events': '1199270', 'weight': '95141.2109032995'}, '470to600': {'ext': '', 'xSec': '648.2', 'events': '8382000', 'weight': '0.07733237890718206'}, '15to30': {'ext': '', 'xSec': '1327600000', 'events': '1198520', 'weight': '1107699.4960451224'}}

    if 'Validation' in opt.tag:
        for pthatbin in list(qcdMuPtHatBins.keys()):
            if pthatbin!='80to120': del qcdMuPtHatBins[pthatbin]
        for pthatbin in list(qcdPtHatBins.keys()):
            if pthatbin!='80to120': del qcdPtHatBins[pthatbin]

    if 'WorkingPoints' in opt.tag or 'PtHatWeights' in opt.tag or 'Light' in opt.tag:

        nPtHatBins = len(list(qcdPtHatBins.keys()))        

        qcdTrees = []
        for pth in qcdPtHatBins:
            if pth=='80to120' or 'WorkingPoints' not in opt.tag:
                ptHatTrees = getSampleFiles(directoryBkg+qcdName.replace('PTHATBIN',pth)+qcdPtHatBins[pth]['ext']+'/','',True,treePrefix,skipTreesCheck)
                if 'PtHatWeights' in opt.tag: samples['QCD_'+pth] = { 'name' : ptHatTrees }
                else: qcdTrees += ptHatTrees

        if 'WorkingPoints' in opt.tag or 'Light' in opt.tag:
            samples['QCD']   = { 'name' : qcdTrees, 'weight' : '1.', 'isSignal' : 0 }
            #if 'WorkingPoints' in opt.tag:
            #    samples['ttbar'] = { 'name' : getSampleFiles(directoryBkg+ttbarName+'/',ttbarName,True,treePrefix,skipTreesCheck), 'weight' : '1.', 'isSignal' : 0 }

        if 'PtHatWeights' not in opt.tag and 'Validation' not in opt.tag:
            for sample in samples:
                for pth in qcdPtHatBins:
                    addSampleWeight(samples, sample, qcdName.replace('PTHATBIN',pth).split('_',1)[-1], qcdPtHatBins[pth]['weight'])

    if 'PtHatWeights' in opt.tag or opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag or opt.method+'Templates' in opt.tag:

        nPtHatBins = len(list(qcdMuPtHatBins.keys()))

        qcdMuTrees = []
        for pth in qcdMuPtHatBins:
            ptHatTrees = getSampleFiles(directoryBkg+qcdMuName.replace('PTHATBIN',pth)+qcdMuPtHatBins[pth]['ext']+'/','',True,treePrefix,skipTreesCheck)
            if 'PtHatWeights' in opt.tag: samples['QCDMu_'+pth] = { 'name' : ptHatTrees }
            else: qcdMuTrees += ptHatTrees

        if opt.method+'Kinematics' in opt.tag or 'DataKinematics' in opt.tag:
            samples['QCDMu'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight               , 'isSignal' : 1 }

        elif opt.method+'Templates' in opt.tag:
            samples['bjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromB, 'isSignal' : bIsSignal }
            if 'PtRel' in opt.method:
                if '2D' not in opt.tag: samples['cjets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromC, 'isSignal' : 0 }
                samples['ljets'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetFromL, 'isSignal' : 0 }
            elif 'System8' in opt.method:
                samples['light'] = { 'name' : qcdMuTrees, 'weight'   : muJetKinematicWeight+'*'+muJetNotFromB, 'isSignal' : 0 }

        if 'PtHatWeights' not in opt.tag and 'Validation' not in opt.tag:
            for sample in samples:
                for pth in qcdMuPtHatBins:
                    addSampleWeight(samples, sample, qcdMuName.replace('PTHATBIN',pth).split('_',1)[-1], qcdMuPtHatBins[pth]['weight'])

# Common MC keys

for sample in samples:

    samples[sample]['isDATA']    = 0
    samples[sample]['isFastsim'] = 0
    samples[sample]['treeType']  = 'MC'
    samples[sample]['suppressNegative']          = ['all']
    samples[sample]['suppressNegativeNuisances'] = ['all']
    samples[sample]['suppressZeroTreeNuisances'] = ['all']
    samples[sample]['split'] = 'AsMuchAsPossible'
    samples[sample]['JobsPerSample'] = 20*nPtHatBins if 'Light' in opt.tag else 8*nPtHatBins

### Data

if 'SM' in opt.sigset or 'Data' in opt.sigset:

    dataSetName = 'BTagMu' if 'Light' not in opt.tag else 'JetMET'

    runPeriods = {}
    if 'Summer23BPix' in opt.campaign:
        if dataSetName=='BTagMu':
            runPeriods['Run2023D1'] = { 'subdir' : dataSetName + 'Run2023D-22Sep2023_v1-v1' }
            runPeriods['Run2023D2'] = { 'subdir' : dataSetName + 'Run2023D-22Sep2023_v2-v1' }
        else:  
            runPeriods['Run2023D1'] = { 'subdir' : dataSetName + '0Run2023D-22Sep2023_v1-v1' }
            runPeriods['Run2023D2'] = { 'subdir' : dataSetName + '0Run2023D-22Sep2023_v2-v1' }
            runPeriods['Run2023D3'] = { 'subdir' : dataSetName + '1Run2023D-22Sep2023_v1-v1' }
            runPeriods['Run2023D4'] = { 'subdir' : dataSetName + '1Run2023D-22Sep2023_v2-v1' }
    elif 'Summer23' in opt.campaign:
        if dataSetName=='BTagMu':
            runPeriods['Run2023C1'] = { 'subdir' : dataSetName + 'Run2023C-22Sep2023_v1-v1' }
            runPeriods['Run2023C2'] = { 'subdir' : dataSetName + 'Run2023C-22Sep2023_v2-v1' }
            runPeriods['Run2023C3'] = { 'subdir' : dataSetName + 'Run2023C-22Sep2023_v3-v1' }
            runPeriods['Run2023C4'] = { 'subdir' : dataSetName + 'Run2023C-22Sep2023_v4-v1' }
        else:
            runPeriods['Run2023C1'] = { 'subdir' : dataSetName + '0Run2023C-22Sep2023_v1-v1' }
            runPeriods['Run2023C2'] = { 'subdir' : dataSetName + '0Run2023C-22Sep2023_v2-v1' }
            runPeriods['Run2023C3'] = { 'subdir' : dataSetName + '0Run2023C-22Sep2023_v3-v1' }
            runPeriods['Run2023C4'] = { 'subdir' : dataSetName + '0Run2023C-22Sep2023_v4-v1' }
            runPeriods['Run2023C5'] = { 'subdir' : dataSetName + '1Run2023C-22Sep2023_v1-v1' }
            runPeriods['Run2023C6'] = { 'subdir' : dataSetName + '1Run2023C-22Sep2023_v2-v1' }
            runPeriods['Run2023C7'] = { 'subdir' : dataSetName + '1Run2023C-22Sep2023_v3-v1' }
            runPeriods['Run2023C8'] = { 'subdir' : dataSetName + '1Run2023C-22Sep2023_v4-v1' }

    dataTrees = [ ]
    for runPeriod in runPeriods:
  
        dataDir = '/'.join([ directoryData, runPeriods[runPeriod]['subdir'], '' ]) 
        dataTrees += getSampleFiles(dataDir,  '', True, treePrefix, skipTreesCheck)
 
    dataName = 'DATA' if dataSetName=='BTagMu' else 'Jet'
    samples[dataName]  = { 'name'      : dataTrees ,
                           'weight'    : '1.' ,
                           'isData'    : ['all'] ,
                           'treeType'  : 'Data' ,
                           'isSignal'  : 0 ,
                           'isDATA'    : 1 ,
                           'isFastsim' : 0 ,
                           'split'     : 'AsMuchAsPossible',
                           'JobsPerSample' : 20*len(list(runPeriods.keys())) if 'Light' in opt.tag else 8*len(list(runPeriods.keys()))
                          }
     
### Files per job

removeFromSplit = []
 
for sample in samples:
    if 'FilesPerJob' not in samples[sample]:
        ntrees = len(samples[sample]['name']) 
        multFactor = 6 if 'JobsPerSample' not in samples[sample] else int(samples[sample]['JobsPerSample'])
        filesPerJob = int(math.ceil(float(ntrees)/multFactor))
        if filesPerJob>1: samples[sample]['FilesPerJob'] = filesPerJob
        else: removeFromSplit.append(sample)

for sample in removeFromSplit:
    del samples[sample]['split']

### Cleaning

if opt.sigset.split('-')[0] not in [ 'SM', 'MC', 'Data' ]:

    sampleToRemove = [ ]

    shortset = opt.sigset.split('-')[0]

    for sample in samples:
        if 'Veto' in shortset:
            if sample in shortset:
                sampleToRemove.append(sample)
        elif sample not in shortset: # Be sure this sample's name is not substring of other samples' names
            sampleToRemove.append(sample)

    for sample in sampleToRemove:
        del samples[sample]

### Nasty clean up for eos

if 'cern' in SITE:
    for sample in samples:
        for ifile in range(len(samples[sample]['name'])):
            samples[sample]['name'][ifile] = samples[sample]['name'][ifile].replace('root://eoscms.cern.ch/', '')

### getCampaignParameters for python3

if hasattr(opt, 'getCampaignParameters') and opt.getCampaignParameters:

    opt.minPlotPt = minPlotPt
    opt.maxPlotPt = maxPlotPt
    opt.maxJetEta = float(maxJetEta)
    opt.bTagAlgorithms = bTagAlgorithms
    opt.btagWPs = list(bTagWorkingPoints.keys())
    opt.ptBins = list(jetPtBins.keys())

    opt.Selections = []
    for selection in systematicVariations:
        sel = 'Central' if selection=='' else selection
        if 'vetosel' in opt.option:
            if sel in opt.option: continue
        elif 'sel' in opt.option and sel not in opt.option: continue
        opt.Selections.append(selection)
    opt.systematicNuisances = systematicNuisances

    if opt.action=='ptHatWeights':
        opt.samples = samples
        opt.qcdMuPtHatBins = qcdMuPtHatBins
        opt.qcdPtHatBins = qcdPtHatBins

    elif opt.action=='triggerPrescales':
        opt.campaignRunPeriod = campaignRunPeriod
        opt.triggerInfos = triggerInfos

    elif opt.action=='workingPoints':
        opt.workingPointName = workingPointName
        opt.workingPointLimit = workingPointLimit
        opt.samples = samples
        opt.nJetMax = nJetMax
        opt.bTagWorkingPoints = bTagWorkingPoints
 
    elif opt.action=='frameworkValidation':                     
        opt.samples = list(samples.keys())
        opt.triggerInfos = triggerInfos                                                                                                                                                                              
    elif opt.action=='kinematicWeights': 
        opt.jetPtBins = jetPtBins         
        opt.minJetPt  = minJetPt
        opt.maxJetPt  = maxJetPt

    elif opt.action=='ptRelInput' or opt.action=='shapesForFit':
        opt.templateTreatments = templateTreatments
        opt.bTemplateCorrector = bTemplateCorrector

    elif opt.action=='storeBTagScaleFactors':
        opt.csvCampaign = '2023_'+opt.campaign
        opt.csvMethod = 'ptrel' if opt.method=='PtRel' else 'sys8'
        opt.csvBTagAlgorithms = { 'DeepJet' : 'deepJet', 'ParticleNet' : 'particleNet', 'ParT' : 'robustParticleTransformer' }
        opt.csvSystematics = csvSystematics


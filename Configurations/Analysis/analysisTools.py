import os
import ROOT
import copy
import math
import PlotsConfigurations.Tools.commonTools as commonTools
import PlotsConfigurations.Tools.latinoTools as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools
import PlotsConfigurations.Tools.signalMassPoints as signalMassPoints
from array import array

### Analysis defaults

def setAnalysisDefaults(opt):
   
    opt.baseDir = os.getenv('PWD')
    opt.combineLocation = '/afs/cern.ch/work/s/scodella/SUSY/CMSSW_10_2_14/src'
    opt.isExotics = True

    if opt.year.lower()=='run2split': opt.year = '2016HIPM-2016noHIPM-2017-2018'
    elif '2016split' in opt.year: opt.year = opt.year.replace('2016split','2016HIPM-2016noHIPM')
    elif opt.year.lower()=='run2': opt.year = '2016-2017-2018'

    inputTag = opt.tag

    validationRegionMap = { 'vr1'    : 'HighPtMissValidationRegionVetoesUL',
                            'wzwwvr' : 'WZtoWWValidationRegionVetoesUL' } 

    opt.signalRegionMap, opt.signalSubsets, opt.tableSigset = { }, { }, { }

    opt.signalRegionMap['stopSR'] = { 'tag' : 'StopSignalRegionsVetoesUL',     'signals' : [ 'T2tt_mS-150to800_dm-80to175', 'T2bW_mS-200to1000_mX-1to700' ] }
    opt.signalRegionMap['charSR'] = { 'tag' : 'CharginoSignalRegionsVetoesUL', 'signals' : [ 'TChipmSlepSnu_mC-100to1500_mX-1to750', 'TSlepSlep_mS-100to1000_mX-1to650' ] }
    opt.signalRegionMap['chwwSR'] = { 'tag' : 'TChipmWWSignalRegionsVetoesUL', 'signals' : [ 'TChipmWW_mC-100to700_mX-1to250' ] }

    #opt.tableSigset['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-300_mX-1', 'TChipmSlepSnu_mC-400_mX-225', 'TChipmSlepSnu_mC-500_mX-50', 'TChipmSlepSnu_mC-300_mX-175', 'TChipmSlepSnu_mC-500_mX-300', 'TChipmSlepSnu_mC-650_mX-125', 'TChipmSlepSnu_mC-650_mX-350', 'TChipmSlepSnu_mC-800_mX-200', 'TChipmSlepSnu_mC-950_mX-200', 'TChipmSlepSnu_mC-200_mX-125', 'TChipmSlepSnu_mC-200_mX-150', 'TChipmSlepSnu_mC-250_mX-175', 'TChipmSlepSnu_mC-300_mX-200', 'TChipmSlepSnu_mC-300_mX-225', 'TChipmSlepSnu_mC-350_mX-250', 'TChipmSlepSnu_mC-400_mX-275', 'TChipmSlepSnu_mC-450_mX-325', 'TChipmSlepSnu_mC-500_mX-325', 'TChipmSlepSnu_mC-700_mX-425', 'TChipmSlepSnu_mC-800_mX-450', 'TChipmSlepSnu_mC-900_mX-425', 'TChipmSlepSnu_mC-1000_mX-375', 'TChipmSlepSnu_mC-1100_mX-300', 'TChipmSlepSnu_mC-1150_mX-1' ]
    opt.tableSigset['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-300_mX-1', 'TChipmSlepSnu_mC-400_mX-225', 'TChipmSlepSnu_mC-500_mX-50', 'TChipmSlepSnu_mC-300_mX-175', 'TChipmSlepSnu_mC-500_mX-300', 'TChipmSlepSnu_mC-650_mX-125', 'TChipmSlepSnu_mC-650_mX-350', 'TChipmSlepSnu_mC-800_mX-200', 'TChipmSlepSnu_mC-950_mX-200', 'TChipmSlepSnu_mC-300_mX-200', 'TChipmSlepSnu_mC-300_mX-225', 'TChipmSlepSnu_mC-350_mX-250', 'TChipmSlepSnu_mC-400_mX-275', 'TChipmSlepSnu_mC-450_mX-325', 'TChipmSlepSnu_mC-500_mX-325', 'TChipmSlepSnu_mC-700_mX-425', 'TChipmSlepSnu_mC-800_mX-450', 'TChipmSlepSnu_mC-900_mX-425', 'TChipmSlepSnu_mC-1000_mX-375', 'TChipmSlepSnu_mC-1100_mX-300', 'TChipmSlepSnu_mC-1150_mX-1' ]
    opt.tableSigset['T2tt']          = [ 'T2tt_mS-300_mX-213', 'T2tt_mS-300_mX-175', 'T2tt_mS-350_mX-263', 'T2tt_mS-350_mX-225', 'T2tt_mS-400_mX-275', 'T2tt_mS-300_mX-125', 'T2tt_mS-350_mX-175', 'T2tt_mS-400_mX-225', 'T2tt_mS-400_mX-313', 'T2tt_mS-475_mX-350', 'T2tt_mS-450_mX-275', 'T2tt_mS-450_mX-325', 'T2tt_mS-475_mX-388', 'T2tt_mS-450_mX-363', 'T2tt_mS-475_mX-300', 'T2tt_mS-475_mX-325', 'T2tt_mS-475_mX-375', 'T2tt_mS-500_mX-325', 'T2tt_mS-500_mX-350', 'T2tt_mS-500_mX-375', 'T2tt_mS-500_mX-400', 'T2tt_mS-500_mX-413', 'T2tt_mS-525_mX-350', 'T2tt_mS-525_mX-375', 'T2tt_mS-525_mX-400', 'T2tt_mS-525_mX-425', 'T2tt_mS-525_mX-438', 'T2tt_mS-550_mX-375', 'T2tt_mS-550_mX-400', 'T2tt_mS-550_mX-425', 'T2tt_mS-550_mX-450', 'T2tt_mS-550_mX-463' ]
    opt.tableSigset['TChipmWW']      = [ 'TChipmWW_mC-100_mX-1', 'TChipmWW_mC-150_mX-1', 'TChipmWW_mC-200_mX-1', 'TChipmWW_mC-200_mX-25', 'TChipmWW_mC-200_mX-50', 'TChipmWW_mC-300_mX-75', 'TChipmWW_mC-400_mX-50', 'TChipmWW_mC-350_mX-75' ]    
    opt.tableSigset['Studies']      = [ 'T2tt_mS-525_mX-350','T2tt_mS-525_mX-438','TChipmSlepSnu_mC-1150_mX-1','TChipmSlepSnu_mC-900_mX-475','EOYT2tt_mS-525_mX-350','EOYT2tt_mS-525_mX-438','EOYTChipmSlepSnu_mC-1150_mX-1','EOYTChipmSlepSnu_mC-900_mX-475' ]
    opt.tableSigset['T2bW'] = [ 'T2bW_mS-500_mX-300', 'T2bW_mS-700_mX-350', 'T2bW_mS-750_mX-1' ]

    opt.signalSubsets['T2tt'] = [ 'T2tt_mS-150to800_dm-80to175' ]
    opt.signalSubsets['T2bW'] = ['T2bW_mS-200to600_mX-1to700', 'T2bW_mS-625to800_mX-1to700', 'T2bW_mS-825to1000_mX-1to700']

    if 'SigV6' in inputTag or 'sigv6' in inputTag:
        opt.tableSigset['TSlepSlep'] = [ 'TSlepSlep_mS-200_mX-120', 'TSlepSlep_mS-400_mX-250', 'TSlepSlep_mS-400_mX-300', 'TSlepSlep_mS-600_mX-300', 'TSlepSlep_mS-800_mX-1' ]
        opt.signalSubsets['TChipmSlepSnu'] = [ 'TChipmSlepSnu_mC-100to475_mX-1to750', 'TChipmSlepSnu_mC-500to650_mX-1to750', 'TChipmSlepSnu_mC-675to800_mX-1to750', 'TChipmSlepSnu_mC-825to925_mX-1to750', 'TChipmSlepSnu_mC-950to1050_mX-1to750', 'TChipmSlepSnu_mC-1075to1175_mX-1to750', 'TChipmSlepSnu_mC-1200to1300_mX-1to750', 'TChipmSlepSnu_mC-1325to1425_mX-1to750', 'TChipmSlepSnu_mC-1450to1500_mX-1to750' ]
        opt.signalSubsets['TChipmWW']      = [ 'TChipmWW_mC-100to375_mX-1to250', 'TChipmWW_mC-400to700_mX-1to250' ]
        opt.signalSubsets['TSlepSlep'] = [ 'TSlepSlep_mS-100to275_mX-1to650', 'TSlepSlep_mS-300to400_mX-1to650', 'TSlepSlep_mS-425to600_mX-1to650', 'TSlepSlep_mS-625to900_mX-1to650', 'TSlepSlep_mS-925to1000_mX-1to650' ]
    else:
        opt.tableSigset['TSlepSlep'] = [ 'TSlepSlep_mS-200_mX-125', 'TSlepSlep_mS-200_mX-150', 'TSlepSlep_mS-400_mX-250', 'TSlepSlep_mS-400_mX-275', 'TSlepSlep_mS-400_mX-300', 'TSlepSlep_mS-600_mX-300', 'TSlepSlep_mS-800_mX-1' ]
        opt.signalSubsets['TChipmSlepSnu'] = ['TChipmSlepSnu_mC-100to350_mX-1to750', 'TChipmSlepSnu_mC-375to500_mX-1to750', 'TChipmSlepSnu_mC-525to625_mX-1to750', 'TChipmSlepSnu_mC-650to725_mX-1to750', 'TChipmSlepSnu_mC-750to825_mX-1to750', 'TChipmSlepSnu_mC-850to925_mX-1to750', 'TChipmSlepSnu_mC-950to1025_mX-1to750', 'TChipmSlepSnu_mC-1050to1125_mX-1to750', 'TChipmSlepSnu_mC-1150to1225_mX-1to750', 'TChipmSlepSnu_mC-1250to1325_mX-1to750', 'TChipmSlepSnu_mC-1350to1425_mX-1to750', 'TChipmSlepSnu_mC-1450to1500_mX-1to750']
        opt.signalSubsets['TChipmWW'] = ['TChipmWW_mC-100to275_mX-1to250', 'TChipmWW_mC-300to500_mX-1to250', 'TChipmWW_mC-525to700_mX-1to250']
        opt.signalSubsets['TSlepSlep'] = ['TSlepSlep_mS-100to325_mX-1to650', 'TSlepSlep_mS-350to475_mX-1to650', 'TSlepSlep_mS-500to600_mX-1to650', 'TSlepSlep_mS-625to700_mX-1to650', 'TSlepSlep_mS-725to800_mX-1to650', 'TSlepSlep_mS-825to900_mX-1to650', 'TSlepSlep_mS-925to1000_mX-1to650']

    opt.backgroundsInFit = [ 'ttZ', 'ZZ', 'WZ' ]

    tagList = []

    for vr in validationRegionMap:
        if vr.lower() in inputTag or 'allvr' in inputTag: tagList.append(validationRegionMap[vr])

    for sr in opt.signalRegionMap:
        if sr.lower() in inputTag or 'allsr' in inputTag: tagList.append(opt.signalRegionMap[sr]['tag'])
     
    if 'fitcr' in inputTag:
        fitcrtag = inputTag.replace(inputTag.split('fitcr')[0],'')
        allSR, allFitCR = True, True
        for sr in opt.signalRegionMap:
            if sr.replace('SR','') in fitcrtag: allSR = False
        for backcr in opt.backgroundsInFit:
            if backcr.lower() in fitcrtag: allFitCR = False
        for sr in opt.signalRegionMap:
            if allSR or sr.replace('SR','') in fitcrtag:
                for backcr in opt.backgroundsInFit:
                    if allFitCR or backcr.lower() in fitcrtag:
                        tagList.append(opt.signalRegionMap[sr]['tag'].replace('VetoesUL','FitCR'+backcr+'VetoesUL'))

    elif 'fit' in inputTag:
        for sr in opt.signalRegionMap:
            if 'fit'+sr.replace('SR','') in inputTag:
                tagList.append(opt.signalRegionMap[sr]['tag'].replace('VetoesUL','FitCRVetoesUL'))
     
    if len(tagList)>0: opt.tag = '-'.join( tagList )

    if 'group' in inputTag: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsGroup')
    if 'merge' in inputTag: opt.tag = opt.tag.replace('SignalRegions','SignalRegionsMerge') 
    opt.tag = opt.tag.replace('StopSignalRegionsMerge','StopSignalRegions')
    if 'fast' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesULFast')
    if 'reco' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesULFastReco')
    if 'systwz' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WZbin')
    if 'systww' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WWshape')
    if 'sysbww' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WWShape')
    if 'sysbwz' in inputTag: opt.tag = opt.tag.replace('VetoesUL','VetoesUL_WZBin')

    if opt.action=='shapes':
        for sr in opt.signalRegionMap:
            for signal in opt.signalRegionMap[sr]['signals']:
                if signal.split('_')[0] in opt.sigset:
                    opt.sigset = opt.sigset
 
    if opt.verbose: print opt.year, opt.tag, opt.sigset

### Shapes

# signal

def signalShapes(opt, action='shapes'):

    mergeJobs = { }

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            for signal in getSignalList(opt, opt.sigset, tag):

                opt2 = copy.deepcopy(opt)
                opt2.year, opt2.tag, opt2.action = year, tag, action

                if action=='shapes':

                    if 'split' in opt.option:
                        for massPoint in getMassPointList(signal):
                            opt2.sigset = massPoint
                            latinoTools.shapes(opt2)
                         
                    else:
                        opt2.sigset = signal
                        latinoTools.shapes(opt2)

                elif action=='checkJobs' or action=='killJobs':
                    opt2.sigset = signal if 'mergesig' in opt.logprocess else signal
                    if action=='checkJobs':  commonTools.checkJobs(opt2)
                    elif action=='killJobs': commonTools.killJobs(opt2)

                elif action=='mergeall':
               
                    if opt.recover:
                        if commonTools.isGoodFile(commonTools.getShapeFileName(opt.shapedir, year, tag, signal, '')): continue

                    if opt.reset: 
                        commonTools.resetFile(commonTools.getShapeFileName(opt.shapedir, year, tag, signal, ''))

                    if opt.interactive:
                        opt2.sigset = signal
                        latinoTools.mergeall(opt2)
                  
                    else:
                        if year not in mergeJobs: mergeJobs[year] = {}
                        if tag not in mergeJobs[year]: mergeJobs[year][tag] = {}
                        mergeCommandList = [ 'cd '+os.getenv('PWD'), 'eval `scramv1 runtime -sh`' ]
                        mergeCommandList.append('./runAnalysis.py --action=mergeall --year='+year+' --tag='+tag+' --sigset='+signal)
                        mergeJobs[year][tag][signal] = '\n'.join(mergeCommandList) 

    if len(mergeJobs.keys())>0:
        for year in mergeJobs:
            for tag in mergeJobs[year]:
                if len(mergeJobs[year][tag].keys())>0:
                    latinoTools.submitJobs(opt, 'mergesig', year+tag, mergeJobs[year][tag], 'Targets', True, 1)

def checkSignalJobs(opt):

    signalShapes(opt, action='checkJobs')

def killSignalJobs(opt):

    signalShapes(opt, action='killJobs')

def mergeSignal(opt):

    signalShapes(opt, action='mergeall')

# stuff for 2016  

def merge2016(opt):

    inputNuisances = commonTools.getCfgFileName(opt, 'nuisances') 

    for tag in opt.tag.split('-'):

        outputDir = '/'.join([ opt.shapedir, '2016', tag ])
        outputFile = outputDir+'/plots_'+tag+'_'+opt.sigset+'.root'
        if opt.recover and commonTools.isGoodFile(outputFile): continue
        os.system('rm -r -f '+outputFile)
        commonTools.mergeDataTakingPeriodShapes(opt, '2016HIPM-2016noHIPM', tag, opt.sigset, 'deep', outputDir, inputNuisances, 'None', opt.verbose)

def merge2016SR(opt):

    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):
  
        opt2.tag = tag

        for sigset in getSignalList(opt, opt.sigset, tag):
            opt2.sigset = sigset
            merge2016(opt2)

        if 'SM' in opt.sigset:
 
            opt2.sigset = 'SM'
            merge2016(opt2)

            for backcr in opt.backgroundsInFit:
                opt2.tag = tag.replace('VetoesUL', 'FitCR'+backcr+'VetoesUL')
                merge2016(opt2)

def merge2016CR(opt):

    opt2 = copy.deepcopy(opt)

    for tag in opt.tag.split('-'):

        opt2.tag = tag

        opt2.sigset = 'SM'
        merge2016(opt2)

        for sigset in getSignalList(opt, opt.sigset, tag):
            opt2.sigset = sigset
            merge2016(opt2)

def mergeSignalToSM(opt):

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            smtag = tag.split('VetoesUL')[0]+'VetoesUL'
            signaltag = tag.replace('Group','').replace('WWPol1a','').replace('SmtEU','')

            for sigset in getSignalList(opt, opt.sigset, tag):

                outputDir = commonTools.getShapeDirName(opt.shapedir, year, tag)
                outputFile = outputDir                         + '/plots_' + tag       + '_SM-' + sigset + '.root'
                smFile     = outputDir.replace(tag, smtag)     + '/plots_' + smtag     + '_SM.root' 
                signalFile = outputDir.replace(tag, signaltag) + '/plots_' + signaltag + '_' + sigset + '.root'

                os.system('mkdir -p '+outputDir+' ; rm -r -f '+outputFile+' ; haddfast --compress '+outputFile+' '+smFile+' '+signalFile) 

# groups

def mergeGroupsForDatacards(opt):

    inputnuisances = commonTools.getCfgFileName(opt, 'nuisances')

    groups = { 'ttbar' : [ 'ttbar', 'ttSemilep' ],
               'minor' : [ 'Higgs', 'VVV', 'ttW', 'VZ' ] }

    groupList = []
    for group in groups:
        groupList.append(group+':'+','.join(groups[group]))

    mergeCommandList = [ '--inputDir='+opt.shapedir, '--sigset='+opt.sigset, '--nuisancesFile='+inputnuisances ]
    mergeCommandList.append('--groups='+'-'.join(groupList))
    if opt.verbose: mergeCommandList.append('--verbose')

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            loopMergeCommandList = mergeCommandList
            loopMergeCommandList.extend([ '--year='+year, '--tag='+tag ])
            outputtag = tag.replace('FitCR', 'GroupFitCR') if 'FitCR' in tag else tag.replace('VetoesUL', 'GroupVetoesUL')
            loopMergeCommandList.append('--outputtag='+outputtag)

            os.system('mergeSamplesForDatacards.py '+' '.join( loopMergeCommandList))

# Smoothing JES/JER/UnclusteredEnergy uncertainties

def smoothEnergyUncertainties(opt):
    
    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):
            os.system('./jetUncertaintiesSmoother.py --year='+year+' --tag='+tag)

# merging CRs in the fit

def mergeFitCR(opt):

    if 'merge2016' in opt.option: merge2016SR(opt)

    for year in opt.year.split('-'):
        for tag in opt.tag.split('-'):

            outputTag = tag.replace('VetoesUL', 'FitCRVetoesUL')
            outputDir = commonTools.getShapeDirName(opt.shapedir, year, outputTag)
            os.system('mkdir -p '+outputDir)
            signalTag = tag.split('VetoesUL')[-1] 

            for signal in getSignalList(opt, opt.sigset, tag):

                outputFile = outputDir + '/plots_' + outputTag + '_SM-' + signal + '.root'
                if opt.recover and commonTools.isGoodFile(outputFile): continue
                os.system('rm -r -f '+outputFile)

                filesToMerge = [ outputFile.replace('FitCR','').replace('-'+signal,'').replace('FastReco','').replace(signalTag,'').replace('EventEven','').replace('EventOdd','') ]
                filesToMerge.append(outputFile.replace('FitCR','').replace('SM-','').replace('Group','').replace('WWTails','').replace('WWHighs','').replace('WWPol1a','').replace('SmtEU',''))
                for backcr in opt.backgroundsInFit:
                    filesToMerge.append(outputFile.replace('FitCR','FitCR'+backcr).replace('-'+signal,'').replace('FastReco','').replace(signalTag,'').replace('SmtEU','').replace('EventEven','').replace('EventOdd',''))

                foundFilesToMerge = True
                for fileToMerge in filesToMerge:
                    if not commonTools.isGoodFile(fileToMerge):
                        print 'mergeFitCR error: input file', fileToMerge, 'not found or corrupted' 
                        foundFilesToMerge = False

                if foundFilesToMerge:
                    os.system('haddfast --compress '+outputFile+' '+' '.join(filesToMerge))

# make pseudo-data out of MC shapes

def makePseudoDataShapes(opt):

    for year in opt.year.split('-'):

        signalList = getSignalList(opt, opt.sigset, opt.tag)
        for signal in signalList:
            for pseudodata in [ '', 'WWHighs' ]:

                opt2 = copy.deepcopy(opt)
                opt2.year = year

                if pseudodata=='' or pseudodata not in opt.tag:
                    opt2.sigset = 'SM-PseudoDATA'+pseudodata+'-'+signal
                    reftag = opt.tag.replace('Group', pseudodata+'Group')

                else:
                    opt2.sigset = 'SM-PseudoDATANo'+pseudodata+'-'+signal
                    reftag = opt.tag.replace(pseudodata, '')

                commonTools.mkPseudoData(opt2, reftag)

### Combine with mass points

def signalCombine(opt, action):

    if opt.sigset=='SM': opt.sigset = 'signal'

    smset = opt.sigset.split('_')[0]
    smset = smset.replace(smset.split('-')[-1],'')
    if smset=='': smset = 'SM-'

    for tag in opt.tag.split('-'):

        opt2 = copy.deepcopy(opt)
        opt2.year, opt2.tag = opt.year, tag

        filesetMap = {}
        signalList = getSignalList(opt, opt.sigset, tag)      

        if 'signal' in opt.sigset and 'tabsignal' not in opt.sigset:
            for fileset in signalList:
                filesetMap[smset+fileset] = [ fileset ]

        else:
            for signal in signalList:
                massPoints = getMassPointList(signal)
                for massPoint in massPoints:
                    if opt.fileset!='': signalFileset = opt.fileset.replace('massPoint',massPoint)
                    else: signalFileset = smset+getMassPointSubset(opt, massPoint)
                    if signalFileset!=None:
                        if signalFileset not in filesetMap: filesetMap[signalFileset] = []
                        filesetMap[signalFileset].append(massPoint)

        for fileset in filesetMap:

            opt2.fileset = fileset
            opt2.sigset = smset+','.join(filesetMap[fileset])

            if action=='limits': combineTools.limits(opt2)
            if action=='goodnessOfFit': combineTools.goodnessOfFit(opt2)
            if action=='mlfits': combineTools.mlfits(opt2)
            if action=='impactsPlots': combineTools.impactsPlots(opt2)
            if action=='postFitShapes': latinoTools.postFitShapes(opt2)
            if action=='plots': latinoTools.plots(opt2)
            if action=='fitMatrices': commonTools.fitMatrices(opt2)

def signalLimits(opt):

    signalCombine(opt, 'limits')

def signalGOF(opt):

    signalCombine(opt, 'goodnessOfFit')

def signalMLFits(opt):

    signalCombine(opt, 'mlfits')

def signalImpactsPlots(opt):

    signalCombine(opt, 'impactsPlots')

def signalPostFitShapes(opt):

    signalCombine(opt, 'postFitShapes')

def signalPlots(opt):

    signalCombine(opt, 'plots')

def signalFitMatrices(opt):

    if 'cutsToRemove' not in opt.option and 'allcuts' not in opt.option.lower(): opt.option += 'cutsToRemove:CR:'
    if 'nuisToRemove' not in opt.option and 'allnuis' not in opt.option.lower(): opt.option += 'nuisToRemove:prop:' 
    signalCombine(opt, 'fitMatrices')

### Post fit analysis

# Yields

def yieldsSR(opt):

    yearInDatacard = '-' in opt.year and 'split' not in opt.option and 'merged' not in opt.option

    for tag in opt.tag.split('-'):
        opt2 = copy.deepcopy(opt)
        opt2.tag = tag
        cardNameStructure = latinoTools.getDatacardNameStructure(yearInDatacard, True, 'Merge' in tag)
        if opt.sigset=='SM': opt.sigset += '-tabsignal'
        commonTools.postFitYieldsTables(opt2, cardNameStructure, ','.join(getSignalList(opt, opt.sigset, tag)))

def preFitYieldsSR(opt):
    
    opt.option += 'prefit'
    yieldsSR(opt)

# Limits 

def printLimits(opt):

    signalList = getSignalList(opt, opt.sigset, opt.tag)
    if 'tab' not in opt.sigset: 
        massPointList = []
        for signal in sorted(signalList):
            massPointList.extend(getMassPointList(signal))
        signalList = massPointList

    for signal in sorted(signalList):

        limitResult = {}

        for tags in [ '', '_WWSimm' ]:
            for tagm in [ '', 'WWTails', 'WWHighs', 'WWPol1a', 'SmtEU' ]:
                #if (tags=='' and tagm=='') or (tags!='' and tagm!=''): continue
                if (tags!='' and tagm!=''): continue
                #if 'Stop' in opt.tag and 'Merge' in tagm: continue
                #if 'Stop' not in opt.tag and 'Merge' not in tagm: continue
                #tagopt = (tagm+tags).replace('_WWSimm','')
                tagopt = (tagm+tags)#.replace('WWPol1a','')
                #tag = opt.tag.replace('Group', tagm+'Group')
                tag = opt.tag.replace('Group', 'Group'+tagm)
                tag += tags
                outputDir = '/'.join([ opt.limitdir, opt.year, tag, signal ])
                if not commonTools.isGoodFile(outputDir+'/higgsCombine_Both.AsymptoticLimits.mH120.root', 6000.):
                    if opt.debug: print outputDir+'/higgsCombine_Both.AsymptoticLimits.mH120.root'
                    continue
                inputFile =  commonTools.openRootFile(outputDir+'/higgsCombine_Both.AsymptoticLimits.mH120.root')

                if tagopt=='': limitResult['central'] = []
                else: limitResult[tagopt] = []

                for event in inputFile.limit:
                    if opt.debug: print tagopt, event.limit
                    if tagopt=='': limitResult['central'].append(event.limit)
                    else: limitResult[tagopt].append(event.limit)

        printSignal = True
        signalResult = []
        if 'central' not in limitResult: continue
        availableResultList = [ 'central' ]
        if len(limitResult.keys())==1: printSignal = True
        for evt in range(len(limitResult['central'])):
            resultList = [ str(limitResult['central'][evt]) ]
            for tags in [ '', 'WWTails', 'WWHighs', 'WWPol1a', 'SmtEU' ]:
                for tagm in [ '' ]:
                    tagopt = tagm+tags
                    if tagopt!='' and tagopt in limitResult:
                        diff = abs(1. - limitResult[tagopt][evt]/limitResult['central'][evt])
                        if diff>0.0: printSignal = True
                        if tagopt not in availableResultList: availableResultList.append(tagopt)
                        #resultList.append(str(limitResult[tagopt][evt]/limitResult['central'][evt]))
                        resultList.append(str(limitResult[tagopt][evt]))
                        
            signalResult.append(' '.join(resultList)) 
        availableResult = ' '.join(availableResultList)

        if printSignal:
            print '####', signal
            print '    ', availableResult
            for evt in range(len(signalResult)):
                print signalResult[evt]
            if len(signalResult)==6:
                ccc = []
                obs = signalResult[5].split(' ')
                cen = signalResult[2].split(' ')
                pus = signalResult[3].split(' ')
                pds = signalResult[4].split(' ')
                mus = signalResult[1].split(' ')
                mds = signalResult[0].split(' ')
                for rr in range(len(obs)):
                    if float(obs[rr])<float(cen[rr]) and float(obs[rr])>float(mus[rr]):
                        ccc.append((float(obs[rr])-float(cen[rr]))/(float(cen[rr])-float(mus[rr])))
                    elif float(obs[rr])<float(mus[rr]) and float(obs[rr])>float(mds[rr]):
                        ccc.append(-1.+(float(obs[rr])-float(mus[rr]))/(float(mus[rr])-float(mds[rr])))
                    elif float(obs[rr])<float(mds[rr]):
                        ccc.append(-2.5)
                    elif float(obs[rr])>float(cen[rr]) and float(obs[rr])<float(pus[rr]):
                        ccc.append((float(obs[rr])-float(cen[rr]))/(float(pus[rr])-float(cen[rr])))
                    elif float(obs[rr])>float(pus[rr]) and float(obs[rr])<float(pds[rr]):
                        ccc.append(1.+(float(obs[rr])-float(pus[rr]))/(float(pds[rr])-float(pus[rr])))
                    elif float(obs[rr])>float(pds[rr]):
                        ccc.append(+2.5)
                print ccc
            print '\n\n'

def makeContours(opt, plotoption='2', fitOption='Blind'):

    sigset = ','.join(getSignalList(opt, opt.sigset, opt.tag))

    histogramDir = '/'.join([ opt.limitdir, opt.year, opt.tag, 'Histograms' ])
    contourDir   = '/'.join([ opt.limitdir, opt.year, opt.tag, 'Contours' ])

    histogramFileNoFillEmptyBins = histogramDir + '_'.join([ '/massScan', opt.tag, sigset, fitOption, 'noFillEmptyBins' ]) + '.root'
    histogramFile                = histogramDir + '_'.join([ '/massScan', opt.tag, sigset, fitOption ]) + '.root'
    contourFile                  = contourDir   + '_'.join([ '/massScan', opt.tag, sigset, fitOption ]) + '.root' 

    if opt.reset:
        os.system('rm -f '+' '.join([ histogramFileNoFillEmptyBins, histogramFile, contourFile ]))
 
    commandList = [ '--years='+opt.year, '--tag='+opt.tag, '--sigset='+sigset, '--limitoption='+fitOption ]

    if not os.path.isfile(histogramFileNoFillEmptyBins):
        os.system('analyzeLimits.py '+' '.join(commandList + [ '--nofillempties' ]))

    if plotoption!='0':
        if not os.path.isfile(contourFile):
            os.system('analyzeLimits.py '+' '.join(commandList + [ '--makecontours' ])) 

def exclusionPlot(opt, plotoption='2'):

    tagList = opt.tag.split('-')

    if len(tagList)>2: 
        print 'Comparison of more than two tags not supported'  
        exit()

    fitOption = 'Blind'
    if opt.unblind:
        fitOption = 'Both'
        if plotoption!='2' and (len(tagList)==1 or tagList[0]!=tagList[1]) and 'significance' not in opt.option.lower():
            fitOption = 'Expected' if 'expected' in opt.option.lower() else 'Observed'

    sigset = ','.join(getSignalList(opt, opt.sigset, tagList[0]))
 
    opt2 = copy.deepcopy(opt)
    for tag in tagList:
        opt2.tag = tag
        makeContours(opt2, plotoption, fitOption)

    plotCommandList = [ '--years='+opt.year, '--tag='+tagList[0], '--sigset='+sigset, '--limitoption='+fitOption, '--plotoption='+plotoption, '--limitdir='+opt.limitdir ]
    if opt.reset: plotCommandList.extend([ '--remakehistos', '--remakecontours' ])
    else: plotCommandList.append('--nomakehistos')
    if len(tagList)>1: 
        refTags = '-'.join([ tagList[x] for x in range(1,len(tagList)) ])
        plotCommandList.append('--compareto='+refTags)
    if plotoption=='0': plotCommandList.append('--nofillempties')
    if 'significance' in opt.option.lower(): 
        plotCommandList.append('--dosignificance')
        plotCommandList.append('--add2sigma')
        if len(tagList)==1: plotCommandList.append('--compareto='+tagList[0])
    elif '2sigma' in opt.option.lower(): plotCommandList.append('--add2sigma')

    os.system('analyzeLimits.py '+' '.join(plotCommandList))

def plotLimits(opt):

    exclusionPlot(opt, '0')

def plotContours(opt):

    exclusionPlot(opt, '1')
 
def checkTChipmSlepSnuMasses(opt):

    chain = ROOT.TChain('Events')

    if opt.year=='2018':
        chain.Add('/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21UL18FS_106X_nAODv9_Full2018v8/susyGen__susyW__FSSusy2018v8__FSSusyCorr2018v8__hadd__FSSusyNomin2018v8__susyMT2fastSmear/nanoLatino_TChipmSlepSnu_*.root')
    elif opt.year=='2017':
        chain.Add('/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21UL17FS_106X_nAODv9_Full2017v8/susyGen__susyW__FSSusy2017v8__FSSusyCorr2017v8__hadd__FSSusyNomin2017v8__susyMT2fastSmear/nanoLatino_TChipmSlepSnu_*.root')
    elif opt.year=='2016':
        chain.Add('/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21UL16FS_106X_nAODv9_Full2016v8/susyGen__susyW__FSSusy2016v8__FSSusyCorr2016v8HIPM__hadd__FSSusyNomin2016v8HIPM__susyMT2fastSmear/nanoLatino_TChipmSlepSnu_*.root')
        chain.Add('/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21UL16FS_106X_nAODv9_Full2016v8/susyGen__susyW__FSSusy2016v8__FSSusyCorr2016v8noHIPM__hadd__FSSusyNomin2016v8noHIPM__susyMT2fastSmear/nanoLatino_TChipmSlepSnu_*.root')

    totalEvents = commonTools.bookHistogram('totalEvents', (57, 87.5, 1512.5), (33, -12.5, 812.5))
    goodEvents  = commonTools.bookHistogram('goodEvents',  (57, 87.5, 1512.5), (33, -12.5, 812.5)) 
    sleptonMass = commonTools.bookHistogram('sleptonMass',  (57, 87.5, 1512.5), (33, -12.5, 812.5))

    totalEvents.GetYaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}}} [GeV]')
    totalEvents.GetXaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}}}} [GeV]')

    goodEvents.GetYaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}}} [GeV]')
    goodEvents.GetXaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}}}} [GeV]')

    chain.Draw('susyMLSP:susyMChargino>>totalEvents')
    chain.Draw('susyMLSP:susyMChargino>>goodEvents' ,'fabs(susyMSlepton-(susyMLSP+susyMChargino)/2)<5')

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    plotCanvas.cd()

    pad = commonTools.bookPad('pad', 0.0, 0.0, 0.9, 0.9)
    pad.Draw()
    pad.cd()

    outputDir = '/'.join([ opt.plotsdir, opt.year, 'Limits', ''])
    os.system('mkdir -p '+outputDir)

    NRGBs = 5
    NCont = 255
    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    ROOT.gStyle.SetNumberContours(NCont)
    ROOT.gStyle.SetPaintTextFormat('4.0f')

    refBin = totalEvents.FindBin(1150., 1.)
    print totalEvents.GetBinContent(refBin), goodEvents.GetBinContent(refBin)

    totalEvents.Draw('textcolz')
    plotName = '_'.join([ 'TChipmSlepSnuMasses_Total' ])
    plotCanvas.Print(outputDir+plotName+'.png')

    goodEvents.GetZaxis().SetLabelFont(42)
    goodEvents.GetZaxis().SetTitleFont(42)
    goodEvents.GetZaxis().SetLabelSize(0.035)
    goodEvents.GetZaxis().SetTitleSize(0.035)
    goodEvents.GetZaxis().SetTitleOffset(1.2)

    goodEvents.Draw('textcolz')
    plotName = '_'.join([ 'TChipmSlepSnuMasses_Good' ])
    plotCanvas.Print(outputDir+plotName+'.png')

    goodEvents.Scale(100)
    goodEvents.Divide(totalEvents)

    sleptonMassList = []
    for xb in range(1, goodEvents.GetNbinsX()+1):
        mx = goodEvents.GetXaxis().GetBinCenter(xb)
        for yb in range(1, goodEvents.GetNbinsY()+1):
            my = goodEvents.GetYaxis().GetBinCenter(yb)
            if mx-my<20 or my>750.: 
                goodEvents.SetBinContent(xb, yb, -1)
            else:
                sleptonMass.SetBinContent(xb, yb, (mx+my)/2.)
                if (mx+my)/2. not in sleptonMassList: sleptonMassList.append((mx+my)/2.)
                if goodEvents.GetBinContent(xb, yb)==0: goodEvents.SetBinContent(xb, yb, 0.1)

    print 'nSleptonMasses', len(sleptonMassList)

    goodEvents.SetMinimum(-0.01)
    goodEvents.SetMaximum(100.01)

    goodEvents.Draw('textcolz')

    contourFile = commonTools.openRootFile('Limits/2016-2017-2018/CharginoSignalRegionsMergeWWPol1aGroupSmtEUFitCRVetoesULSigV6_NewBond3_WWcorrYear/Contours/massScan_CharginoSignalRegionsMergeWWPol1aGroupSmtEUFitCRVetoesULSigV6_NewBond3_WWcorrYear_TChipmSlepSnu_mC-100to1500_Both.root')

    expectedExclusion = contourFile.Get('graph_r_expected')
    observedExclusion = contourFile.Get('graph_r_observed')
    expectedExclusion.SetLineWidth(2) 
    observedExclusion.SetLineWidth(2)
    expectedExclusion.SetLineColor(2)
    observedExclusion.SetLineColor(1)
    #expectedExclusion.Draw('same')
    #observedExclusion.Draw('same')

    plotName = '_'.join([ 'TChipmSlepSnuMasses' ])
    plotCanvas.Print(outputDir+plotName+'.png')

    sleptonMass.Draw('textcolz')
    plotName = '_'.join([ 'TChipmSlepSnu_SleptonMass' ])
    plotCanvas.Print(outputDir+plotName+'.png')

    if 'mcmtest' in opt.option:

        chain = ROOT.TChain('Events')
        chain.Add('/afs/cern.ch/work/s/scodella/MonteCarlo/SUS-RunIISpring21UL18FSGSPremixLLPBugFix-00011.root')
        
        charginoMass     = commonTools.bookHistogram('charginoMass', (1400, 100, 1500))
        neutralinoMass   = commonTools.bookHistogram('neutralinoMass', (1400, 100, 1500))
        sleptonMass     = commonTools.bookHistogram('sleptonMass', (800, 100, 900))
        sleptonMassDiff = commonTools.bookHistogram('sleptonMassDiff', (1000, -500, 500))

        chain.Draw('recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM>>charginoMass', 'abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000024')

        charginoMass.Draw()
        plotName = '_'.join([ 'TChipmSlepSnuMcM_CharginoMass' ])
        plotCanvas.Print(outputDir+plotName+'.png')

        chain.Draw('recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM>>neutralinoMass', 'abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000022')

        neutralinoMass.Draw()
        plotName = '_'.join([ 'TChipmSlepSnuMcM_NeutralinoMass' ])
        plotCanvas.Print(outputDir+plotName+'.png')

        chain.Draw('recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM>>sleptonMass', 'abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)>=1000010 && abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)<=1000020')

        sleptonMass.Draw()
        plotName = '_'.join([ 'TChipmSlepSnuMcM_SleptonMass' ])
        plotCanvas.Print(outputDir+plotName+'.png')

        chain.Draw('recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000024))/Sum$((abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000024))+Sum$(recoGenParticles_genParticles__GEN.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)==1000022)))/2.>>sleptonMassDiff', 'abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)>=1000010 && abs(recoGenParticles_genParticles__GEN.obj.m_state.pdgId_)<=1000020')

        sleptonMassDiff.SetXTitle('M_{slepton}-0.5*(M_{chargino}+M_{LSP})/2 [Gev]')
        sleptonMassDiff.Draw()
        plotName = '_'.join([ 'TChipmSlepSnuMcM_SleptonMassDiff' ])
        plotCanvas.Print(outputDir+plotName+'.png')

def testMCM(opt):

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    plotCanvas.cd()

    pad = commonTools.bookPad('pad', 0.0, 0.0, 0.9, 0.9)
    pad.Draw()
    pad.cd()

    outputDir = '/'.join([ opt.plotsdir, opt.year, 'Limits', ''])
    os.system('mkdir -p '+outputDir)

    if opt.option=='T2bW':

        chain = ROOT.TChain('Events')
        chain.Add('/afs/cern.ch/user/f/fiorendi/public/forSUS23002/SUS-RunIISpring21UL16FSGSPremixLLPBugFix-00016_T2bW.root')

        massDiff = commonTools.bookHistogram('massDiff', (1000, -500, 500))

        #chain.Scan('recoGenParticles_genParticles__RECO.obj.m_state.pdgId_:recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM', 'abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)>=1000000')

        #chain.Scan('recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.', 'abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024')

        chain.Scan('recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM:(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.:Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006)):Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))', '(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.)>1. && abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024')

        #chain.Scan('recoGenParticles_genParticles__RECO.obj.m_state.pdgId_:recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM:(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.:Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006)):Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)):(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.)>1.', 'abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024')

        #chain.Draw('recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000006))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.>>massDiff', 'abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024')

        massDiff.SetXTitle('M_{chargino}-0.5*(M_{stop}+M_{LSP})/2 [Gev]')
        massDiff.Draw()
        plotName = '_'.join([ 'T2bWMcM_CharginoMassDiff' ])
        plotCanvas.Print(outputDir+plotName+'.png')

    elif opt.option=='TChipmSlepSnu':

        chain = ROOT.TChain('Events')
        chain.Add('/afs/cern.ch/user/f/fiorendi/public/forSUS23002/SUS-RunIISpring21UL16FSGSPremixLLPBugFix-00012_TChiSlepSnu_825to1500.root')

        chain.Scan('recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM:(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.:Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024)):Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))', '(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM-(Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000024))+Sum$(recoGenParticles_genParticles__RECO.obj.m_state.p4Polar_.fCoordinates.fM*(abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022))/Sum$((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)==1000022)))/2.)>1. && ((abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)>=1000010 && abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)<=1000020) || (abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)>=2000010 && abs(recoGenParticles_genParticles__RECO.obj.m_state.pdgId_)<=2000020))')

def plotTChipmSlepSnuExtensions(opt):

    opt.sigset = 'TChipmSlepSnu'
    opt.unblind = True

    histos = {}
    histos['ExtensionLimExp'] = commonTools.bookHistogram('ExtensionLimExp', (141, 97.5, 802.5), (151, -2.5, 752.5))
    histos['ExtensionLimits'] = commonTools.bookHistogram('ExtensionLimits', (141, 97.5, 802.5), (151, -2.5, 752.5))
    histos['ExtensionLim100'] = commonTools.bookHistogram('ExtensionLim100', (141, 97.5, 802.5), (151, -2.5, 752.5))
    histos['ExtensionRawFac'] = commonTools.bookHistogram('ExtensionRawFac', (141, 97.5, 802.5), (151, -2.5, 752.5))
    histos['ExtensionFactor'] = commonTools.bookHistogram('ExtensionFactor', (141, 97.5, 802.5), (151, -2.5, 752.5))
    histos['ExtensionEvents'] = commonTools.bookHistogram('ExtensionEvents', (141, 97.5, 802.5), (151, -2.5, 752.5))

    for charginoMass in range(100, 801, 25):

        neutralinoMasses = [ 1 ]
        neutralinoMasses.extend([ x for x in range(25, 751, 25) if charginoMass-x>=25 ])

        for neutralinoMass in neutralinoMasses:

            tollerance = 0.05
            if charginoMass-neutralinoMass<50.: tollerance = 0.1
            if charginoMass-neutralinoMass<31.: tollerance = 10.

            minimumScale = 10 #100

            refLimit = 999.
            refFileName = commonTools.getCombineOutputFileName(opt, 'TChipmSlepSnu_mC-'+str(charginoMass)+'_mX-'+str(neutralinoMass), combineAction='limits')
            if not commonTools.isGoodFile(refFileName, 6000.):
                if opt.verbose: print 'Missing reference file', refFileName
                if charginoMass-neutralinoMass==25:
                    ibin = histos['ExtensionRawFac'].FindBin(charginoMass, neutralinoMass)
                    histos['ExtensionRawFac'].SetBinContent(ibin, 1.)
                continue

            refFile = commonTools.openRootFile(refFileName)
            refTree = refFile.Get('limit')
            for event in refTree:
                if refTree.quantileExpected==-1.: refLimit = refTree.limit

            if refLimit<999. and refLimit>10.:
                minimumScale = 1

            elif refLimit<999.:
                for scale in [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10' ]: #, '25', '50' ]:

                    inputFileName = refFileName.replace('F100R', 'F'+scale+'R') if scale!='1' else refFileName.replace('_SigStatF100R','')

                    if not commonTools.isGoodFile(inputFileName, 6000.):
                        if opt.verbose: print 'Missing input file', inputFileName
                        minimumScale = 999
                        break

                    inputFile = commonTools.openRootFile(inputFileName)
                    inputTree = inputFile.Get('limit')
                    limex = 999.
                    limit = 999.
                    for event in inputTree:
                        if inputTree.quantileExpected==0.5: limex = inputTree.limit
                        if inputTree.quantileExpected==-1.: limit = inputTree.limit

                    if scale=='1':
                        ibin = histos['ExtensionLimits'].FindBin(charginoMass, neutralinoMass)
                        histos['ExtensionLimExp'].SetBinContent(ibin, 100*limex)
                        histos['ExtensionLimits'].SetBinContent(ibin, 100*limit)
                        histos['ExtensionLim100'].SetBinContent(ibin, 100*refLimit)
                        if limit<0.5 or refLimit>2.: 
                            minimumScale = 1
                            break 

                    if scale=='1' and limit>1000000000.:
                        minimumScale = 1
                        break

                    elif limit<999.:

                        if opt.verbose and charginoMass==125 and neutralinoMass==1:
                            print scale, limit/refLimit

                        if abs(limit/refLimit-1)<tollerance:
                           minimumScale = int(scale)
                           break

            if minimumScale<999:

                if opt.verbose:
                    print charginoMass, neutralinoMass, minimumScale

                ibin = histos['ExtensionRawFac'].FindBin(charginoMass, neutralinoMass)
                histos['ExtensionRawFac'].SetBinContent(ibin, minimumScale)
    
    for xb in range(1, histos['ExtensionRawFac'].GetNbinsX()+1):
        ybList = []
        for yb in range(1, histos['ExtensionRawFac'].GetNbinsY()+1):
            if histos['ExtensionRawFac'].GetBinContent(xb, yb)>1:
                ybList.append(yb)
        weightS, weightA = 0., 0.
        for yb in ybList:
            weightS += 1./pow(histos['ExtensionLimits'].GetBinContent(xb,yb)-100.,2)
            weightA += histos['ExtensionRawFac'].GetBinContent(xb,yb)/pow(histos['ExtensionLimits'].GetBinContent(xb,yb)-100.,2)
        if len(ybList)>0 and opt.verbose: print xb, ybList, round(weightA/weightS,0)
        for yb in range(1, histos['ExtensionRawFac'].GetNbinsY()+1):
            if histos['ExtensionRawFac'].GetBinContent(xb, yb)>0.:
                if len(ybList)>0 and yb>=ybList[0] and yb<=ybList[len(ybList)-1]:
                    histos['ExtensionFactor'].SetBinContent(xb, yb, round(weightA/weightS,0))
                else:
                    histos['ExtensionFactor'].SetBinContent(xb, yb, histos['ExtensionRawFac'].GetBinContent(xb, yb))

    for xb in range(1, histos['ExtensionFactor'].GetNbinsX()+1):
        mx = histos['ExtensionFactor'].GetXaxis().GetBinCenter(xb)
        for yb in range(1, histos['ExtensionFactor'].GetNbinsY()+1):
            if histos['ExtensionFactor'].GetBinContent(xb, yb)>0:
                my = histos['ExtensionFactor'].GetYaxis().GetBinCenter(yb)

                nevt_mass = 10
                if mx-my<=175:
                    nevt_mass *= max((int((175.-(mx-my))/25.)-max(int((my-250.)/25.),0)+4),1)

                extEvents = nevt_mass #*histos['ExtensionFactor'].GetBinContent(xb, yb)
                histos['ExtensionEvents'].SetBinContent(xb, yb, extEvents)
                mygrid = int(my) if my!=0 else 1
                nevt_grid = int(extEvents)
                if histos['ExtensionFactor'].GetBinContent(xb, yb)>1.:
                    print 'mpoints.append([',int(mx),',',mygrid,',',nevt_grid,'])'

    print 'Total events =', 1000.*histos['ExtensionEvents'].Integral()
    print 1000.*histos['ExtensionEvents'].Integral(), 1000.*histos['ExtensionEvents'].Integral()*9548000./8680000., 1000.*histos['ExtensionEvents'].Integral()*14322000./8680000.
    print 1000.*histos['ExtensionEvents'].Integral(), 1000.*histos['ExtensionEvents'].Integral()*1.1, 1000.*histos['ExtensionEvents'].Integral()*1.1*1.5, 1000.*histos['ExtensionEvents'].Integral()*(1.+1.1+1.1*1.5)

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    plotCanvas.cd()

    pad = commonTools.bookPad('pad', 0.0, 0.0, 0.9, 0.9)
    pad.Draw()
    pad.cd()

    outputDir = '/'.join([ opt.plotsdir, opt.year, 'Limits', ''])
    os.system('mkdir -p '+outputDir)

    NRGBs = 5
    NCont = 255
    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    ROOT.gStyle.SetNumberContours(NCont)
    ROOT.gStyle.SetPaintTextFormat("4.0f")

    contourFile = commonTools.openRootFile('Limits/2016-2017-2018/CharginoSignalRegionsMergeWWPol1aGroupSmtEUFitCRVetoesULSigV6_NewBond3_WWcorrYear/Contours/massScan_CharginoSignalRegionsMergeWWPol1aGroupSmtEUFitCRVetoesULSigV6_NewBond3_WWcorrYear_TChipmSlepSnu_mC-100to1500_Both.root')

    expectedExclusion = contourFile.Get('graph_r_expected')
    observedExclusion = contourFile.Get('graph_r_observed')
    expectedExclusion.SetLineWidth(2)
    observedExclusion.SetLineWidth(2)
    expectedExclusion.SetLineColor(2)
    observedExclusion.SetLineColor(1)

    for histo in histos:

        histos[histo].GetXaxis().SetLabelFont(42)
        histos[histo].GetXaxis().SetTitleFont(42)
        histos[histo].GetXaxis().SetLabelSize(0.035)
        histos[histo].GetXaxis().SetTitleSize(0.035)
        histos[histo].GetXaxis().SetTitleOffset(1.2)
        histos[histo].GetYaxis().SetLabelFont(42)
        histos[histo].GetYaxis().SetTitleFont(42)
        histos[histo].GetYaxis().SetLabelSize(0.035)
        histos[histo].GetYaxis().SetTitleSize(0.035)

        histos[histo].GetYaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}}} [GeV]')
        histos[histo].GetXaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}}}} [GeV]')

        histos[histo].GetZaxis().SetTitleSize(0.035)
        histos[histo].GetZaxis().SetLabelFont(42)
        histos[histo].GetZaxis().SetTitleFont(42)
        histos[histo].GetZaxis().SetLabelOffset(2)
        histos[histo].GetZaxis().SetLabelSize(0.035)
        histos[histo].GetZaxis().SetTitleSize(0.035)

        histos[histo].Draw('textcolz')

        expectedExclusion.Draw('same')
        observedExclusion.Draw('same')

        plotName = '_'.join([ histo, opt.tag, opt.sigset ])
        plotCanvas.Print(outputDir+plotName+'.png')

def plotTChipmWWExtensions(opt):

    opt.sigset = 'TChipmWW'
    opt.unblind = True

    histos = {}
    histos['ExtensionRawFac'] = commonTools.bookHistogram('ExtensionRawFac', (81, 97.5, 502.5), (61, -2.5, 302.5))
    histos['ExtensionFactor'] = commonTools.bookHistogram('ExtensionFactor', (81, 97.5, 502.5), (61, -2.5, 302.5))
    histos['ExtensionEvents'] = commonTools.bookHistogram('ExtensionEvents', (81, 97.5, 502.5), (61, -2.5, 302.5))

    for charginoMass in range(100, 501, 25):

        neutralinoMasses = [ 1 ]
        neutralinoMasses.extend([ x for x in range(25, 251, 25) if x<charginoMass-100 ])
        neutralinoMasses.extend([ charginoMass-x for x in range(100, 9, -10) if charginoMass-x>0 and charginoMass-x<=250 ])
        for neutralinoMass in neutralinoMasses:

            tollerance = 0.05
            if charginoMass-neutralinoMass<50.: tollerance = 0.1
            if charginoMass-neutralinoMass<31.: tollerance = 10.

            minimumScale = 100

            refLimit = 999.
            refFileName = commonTools.getCombineOutputFileName(opt, 'TChipmWW_mC-'+str(charginoMass)+'_mX-'+str(neutralinoMass), combineAction='limits')
            if not commonTools.isGoodFile(refFileName, 6000.): 
                if opt.verbose: print 'Missing reference file', refFileName
                continue
            refFile = commonTools.openRootFile(refFileName)
            refTree = refFile.Get('limit')
            for event in refTree:
                if refTree.quantileExpected==-1.: refLimit = refTree.limit

            if refLimit<999. and refLimit>10.: 
                minimumScale = 1

            elif refLimit<999.:
                for scale in [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '25', '50' ]:

                    inputFileName = refFileName.replace('F100R', 'F'+scale+'R') if scale!='1' else refFileName.replace('_SigStatF100R','')

                    if not commonTools.isGoodFile(inputFileName, 6000.): 
                        if opt.verbose: print 'Missing input file', inputFileName
                        minimumScale = 999
                        break

                    inputFile = commonTools.openRootFile(inputFileName)
                    inputTree = inputFile.Get('limit')
                    limit = 999.
                    for event in inputTree:
                        if inputTree.quantileExpected==-1.: limit = inputTree.limit
                    
                    if scale=='1' and limit>1000000000.: 
                        minimumScale = 1
                        break

                    elif limit<999.:
 
                        if opt.verbose and charginoMass==125 and neutralinoMass==1:
                            print scale, limit/refLimit 

                        if abs(limit/refLimit-1)<tollerance:
                           minimumScale = int(scale)
                           break

            if minimumScale<999:

                if opt.verbose: 
                    print charginoMass, neutralinoMass, minimumScale
  
                ibin = histos['ExtensionRawFac'].FindBin(charginoMass, neutralinoMass) 
                histos['ExtensionRawFac'].SetBinContent(ibin, minimumScale)

    strategy = 'deg'

    for yb in range(histos['ExtensionRawFac'].GetNbinsY(), 0, -1):
        if histos['ExtensionRawFac'].GetBinContent(1, yb)>0:
            if strategy=='uniform':
                maxScale = histos['ExtensionRawFac'].GetBinContent(1, yb)
                for xb in range(1, histos['ExtensionRawFac'].GetNbinsX()+1):  
                    if histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1)>maxScale:
                        maxScale = histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1)        
                for xb in range(1, histos['ExtensionRawFac'].GetNbinsX()+1):
                    if histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1)>0:
                        histos['ExtensionFactor'].SetBinContent(xb, yb+xb-1, maxScale)
            elif strategy=='deg':
                previousScale = -1
                for xb in range(histos['ExtensionRawFac'].GetNbinsX(),0,-1):
                    if histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1)>0: 
                        if histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1)<previousScale:
                            histos['ExtensionFactor'].SetBinContent(xb, yb+xb-1, previousScale)
                        else:
                            histos['ExtensionFactor'].SetBinContent(xb, yb+xb-1, histos['ExtensionRawFac'].GetBinContent(xb, yb+xb-1))
                        previousScale = histos['ExtensionFactor'].GetBinContent(xb, yb+xb-1)
    for xb in range(2, histos['ExtensionRawFac'].GetNbinsX()+1):
        if histos['ExtensionRawFac'].GetBinContent(xb, 1)>0:
            if strategy=='uniform':
                maxScale = histos['ExtensionRawFac'].GetBinContent(xb, 1)
                for yb in range(1, histos['ExtensionRawFac'].GetNbinsY()+1):
                    if histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb)>maxScale:
                        maxScale = histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb)
                for yb in range(1, histos['ExtensionRawFac'].GetNbinsY()+1):
                    if histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb)>0:
                        histos['ExtensionFactor'].SetBinContent(xb+yb-1, yb, maxScale)
            elif strategy=='deg':
                previousScale = -1
                for yb in range(histos['ExtensionRawFac'].GetNbinsY(),0,-1):
                    if histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb)>0:
                        if histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb)<previousScale:
                            histos['ExtensionFactor'].SetBinContent(xb+yb-1, yb, previousScale)
                        else:
                            histos['ExtensionFactor'].SetBinContent(xb+yb-1, yb, histos['ExtensionRawFac'].GetBinContent(xb+yb-1, yb))
                        previousScale = histos['ExtensionFactor'].GetBinContent(xb+yb-1, yb)

    for xb in range(1, histos['ExtensionFactor'].GetNbinsX()+1):
        mx = histos['ExtensionFactor'].GetXaxis().GetBinCenter(xb)
        for yb in range(1, histos['ExtensionFactor'].GetNbinsY()+1):
            if histos['ExtensionFactor'].GetBinContent(xb, yb)>0:
                my = histos['ExtensionFactor'].GetYaxis().GetBinCenter(yb)

                nevt_mass = 20
                if mx-my<=150:
                    fk = min(int((225.-(mx-my))/25.), 5)
                    if mx>=350.-25.*fk:
                        fk = max(fk-int((mx-(350.-25.*fk))/25.+1),2)
                    nevt_mass = 10*fk

                if my>=200: histos['ExtensionFactor'].SetBinContent(xb, yb, 1.)
                if mx-my>100:
                    if mx<=450 and my<=150:
                        if histos['ExtensionFactor'].GetBinContent(xb, yb)<2.: histos['ExtensionFactor'].SetBinContent(xb, yb, 2.)
                        if mx<=400 and my<=100:
                            if histos['ExtensionFactor'].GetBinContent(xb, yb)<3.: histos['ExtensionFactor'].SetBinContent(xb, yb, 3.)
                   
                if histos['ExtensionFactor'].GetBinContent(xb, yb)>1:
                    extEvents = nevt_mass*histos['ExtensionFactor'].GetBinContent(xb, yb)
                    histos['ExtensionEvents'].SetBinContent(xb, yb, extEvents)
                    mygrid = int(my) if my!=0 else 1
                    nevt_grid = int(extEvents)
                    print 'mpoints.append([',int(mx),',',mygrid,',',nevt_grid,'])'

    print 'Total events =', 1000.*histos['ExtensionEvents'].Integral()

    # https://scodella.web.cern.ch/scodella/Work/CMS/SUSY/SUS-19-XXX/V9/2016-2017-2018/Limits/ExtensionGrid_TChipmWW.pdf
    # https://cms-pdmv-prod.web.cern.ch/mcm/requests?dataset_name=SMS-TChipmSlepSnu_mC1-825to1500_TuneCP5_13TeV-madgraphMLM-pythia8&member_of_chain=*Spring21UL1*FS*&prepid=*FS*Premix*-*&page=0&shown=8796093022207
    # https://docs.google.com/spreadsheets/d/1ahxcIY6eu0scOViuIsQs6vbzM05T48Nv6Yd3p787_Gc/edit#gid=0
    # 7900000	8690000	13035000
    print 1000.*histos['ExtensionEvents'].Integral(), 1000.*histos['ExtensionEvents'].Integral()*9548000./8680000., 1000.*histos['ExtensionEvents'].Integral()*14322000./8680000.
    print 1000.*histos['ExtensionEvents'].Integral(), 1000.*histos['ExtensionEvents'].Integral()*1.1, 1000.*histos['ExtensionEvents'].Integral()*1.1*1.5, 1000.*histos['ExtensionEvents'].Integral()*(1.+1.1+1.1*1.5)

    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 1200, 900)
    plotCanvas.cd()

    pad = commonTools.bookPad('pad', 0.0, 0.0, 0.9, 0.9)
    pad.Draw()
    pad.cd()

    outputDir = '/'.join([ opt.plotsdir, opt.year, 'Limits', ''])
    os.system('mkdir -p '+outputDir)

    NRGBs = 5
    NCont = 255
    stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
    green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
    blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
    ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    ROOT.gStyle.SetNumberContours(NCont)
    ROOT.gStyle.SetPaintTextFormat("4.0f")

    for histo in histos:

        histos[histo].GetXaxis().SetLabelFont(42)
        histos[histo].GetXaxis().SetTitleFont(42)
        histos[histo].GetXaxis().SetLabelSize(0.035)
        histos[histo].GetXaxis().SetTitleSize(0.035)
        histos[histo].GetXaxis().SetTitleOffset(1.2)
        histos[histo].GetYaxis().SetLabelFont(42)
        histos[histo].GetYaxis().SetTitleFont(42)
        histos[histo].GetYaxis().SetLabelSize(0.035)
        histos[histo].GetYaxis().SetTitleSize(0.035)

        histos[histo].GetYaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}}} [GeV]')
        histos[histo].GetXaxis().SetTitle('m#kern[0.1]{_{#lower[-0.12]{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}}}} [GeV]')

        histos[histo].GetZaxis().SetTitleSize(0.035)
        histos[histo].GetZaxis().SetLabelFont(42)
        histos[histo].GetZaxis().SetTitleFont(42)
        histos[histo].GetZaxis().SetLabelOffset(2)
        histos[histo].GetZaxis().SetLabelSize(0.035)
        histos[histo].GetZaxis().SetTitleSize(0.035) 
       
        histos[histo].Draw('textcolz')  

        plotName = '_'.join([ histo, opt.tag, opt.sigset ])
        plotCanvas.Print(outputDir+plotName+'.png')

def plotTChipmWWLimits1D(opt):

    limitValues = {}
    for limit in [ 'Mass', 'Observed', 'Expected', 'p1sigma', 'p2sigma', 'm1sigma', 'm2sigma' ]:
        limitValues[limit] = [] 

    opt.sigset = 'TChipmWW'
    opt.unblind = True

    for mass in range(100, 501, 25):

        limitFile = commonTools.openRootFile(commonTools.getCombineOutputFileName(opt, 'TChipmWW_mC-'+str(mass)+'_mX-1', combineAction='limits'))
        inputTree = limitFile.Get('limit')

        if inputTree:
            if inputTree.GetEntries()==6:

                limitValues['Mass'].append(mass)

                for event in inputTree:
                    if inputTree.quantileExpected==-1.: limitValues['Observed'].append(inputTree.limit)
                    elif inputTree.quantileExpected==0.5: limitValues['Expected'].append(inputTree.limit)
                    elif round(inputTree.quantileExpected, 2)==0.84: limitValues['p1sigma'].append(inputTree.limit)
                    elif round(inputTree.quantileExpected, 2)==0.16: limitValues['m1sigma'].append(inputTree.limit)
                    elif round(inputTree.quantileExpected, 3)==0.975: limitValues['p2sigma'].append(inputTree.limit)
                    elif round(inputTree.quantileExpected, 3)==0.025: limitValues['m2sigma'].append(inputTree.limit)

    canvas = commonTools.bookCanvas('canvas', 1200, 800)
    canvas.cd()

    pad = commonTools.bookPad('pad', 0.02, 0.02, 0.98, 0.98)
    pad.Draw()
    pad.cd()

    histo = commonTools.bookHistogram('roc', (1000,90.,510.))
    histo.SetXTitle('m#kern[0.1]{_{#lower[-0.12]{#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}}}} [GeV]')
    if 'xs' in opt.option: 
        CHRP = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{+}}}#kern[-1.3]{#scale[0.85]{_{1}}}' 
        CHRM = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{-}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
        histo.SetYTitle('95% CL upper limit on #sigma(pp#rightarrow '+CHRP+CHRM+') [pb]')
        histo.SetMaximum(35.)
        histo.SetMinimum(0.01)
        pad.SetLogy()
    else: 
        histo.SetYTitle('95% CL upper limit on the signal strength')
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05) 
    histo.Draw()

    ob, ex = ROOT.TGraph(), ROOT.TGraph()
    e1, e2 = ROOT.TGraphAsymmErrors(), ROOT.TGraphAsymmErrors()

    from LatinoAnalysis.NanoGardener.framework.samples.susyCrossSections import SUSYCrossSections

    maxYhisto = -999.

    for point in range(len(limitValues['Mass'])):
        XS = 1. if 'xs' not in opt.option else float(SUSYCrossSections['WinoC1C1']['massPoints'][str(limitValues['Mass'][point])]['value'])/1000.
        maxYhisto = max(maxYhisto, XS*limitValues['Observed'][point])
        maxYhisto = max(maxYhisto, XS*limitValues['p2sigma'][point])
        ob.SetPoint(point, limitValues['Mass'][point], limitValues['Observed'][point]*XS)
        ex.SetPoint(point, limitValues['Mass'][point], limitValues['Expected'][point]*XS)
        e1.SetPoint(point, limitValues['Mass'][point], limitValues['Expected'][point]*XS)
        e1.SetPointError(point, 12.5, 12.5, XS*(limitValues['Expected'][point]-limitValues['m1sigma'][point]), XS*(limitValues['p1sigma'][point]-limitValues['Expected'][point])) 
        e2.SetPoint(point, limitValues['Mass'][point], limitValues['Expected'][point]*XS)
        e2.SetPointError(point, 12.5, 12.5, XS*(limitValues['Expected'][point]-limitValues['m2sigma'][point]), XS*(limitValues['p2sigma'][point]-limitValues['Expected'][point]))      

    histo.SetMaximum(1.1*maxYhisto)
    histo.Draw()
   
    e2.SetFillColor(5)
    e2.Draw('e3')

    e1.SetFillColor(3)
    e1.Draw('e3')

    ex.SetLineColor(1)
    ex.SetLineWidth(2)
    ex.Draw('l')

    ob.SetLineColor(2)
    ob.SetLineWidth(2)
    ob.SetMarkerStyle(20)
    ob.SetMarkerColor(2)
    ob.Draw('lp')

    outputDir = '/'.join([ opt.plotsdir, opt.year, 'Limits', ''])
    os.system('mkdir -p '+outputDir)

    plotName = '_'.join([ 'Limits1D', opt.tag, opt.sigset ]) + '_mX-1'
    if 'xs' in opt.option: plotName += '_XS'
    canvas.Print(outputDir+plotName+'.png')

### Tools for handling signal mass points

def getMassPointSubset(opt, massPoint):

    for subset in opt.signalSubsets[massPoint.split('_')[0]]:
        if signalMassPoints.massPointInSignalSet(massPoint, subset):
            return subset

    return None
          
def getSignalList(opt, sigset, tag):

    if sigset=='SM': return []

    for sr in opt.signalRegionMap:
       if opt.signalRegionMap[sr]['tag'].replace('VetoesUL','') in tag:
            if 'all' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if signal.split('_')[0] in sigset:
                        signalList.append(signal)
                if len(signalList)==0: return opt.signalRegionMap[sr]['signals']
                else: return signalList
            elif 'tabsignal' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if sigset.split('-')[-1]=='tabsignal' or sigset.split('-')[-1]=='tabsignalset' or signal.split('_')[0] in sigset:
                        if signal.split('_')[0] in opt.tableSigset:
                            signalList.extend(opt.tableSigset[signal.split('_')[0]])
                if 'tabsignalset' in sigset: return [ ','.join(signalList) ]
                else: return signalList

            elif 'signal' in sigset:
                signalList = []
                for signal in opt.signalRegionMap[sr]['signals']:
                    if sigset.split('-')[-1]=='signal' or signal.split('_')[0] in sigset:
                        signalList.extend(opt.signalSubsets[signal.split('_')[0]])
                return signalList

            else:
                setToRemove = sigset.split('_')[0].split('-')
                for st in range(len(setToRemove)-1): sigset = sigset.replace(setToRemove[st]+'-', '')
                return sigset.split(',')

    if 'SignalRegion' not in tag:
        if 'tabsignal' in sigset:
            for signal in opt.tableSigset:
                if signal in sigset:
                   if 'tabsignalset' in sigset: return [ ','.join(opt.tableSigset[signal]) ]
                   else: return opt.tableSigset[signal]
        else:
            setToRemove = sigset.split('_')[0].split('-')
            for st in range(len(setToRemove)-1): sigset = sigset.replace(setToRemove[st]+'-', '')
            return sigset.split(',')

def splitSignalMassPoints(opt, massPointForSubset=100):

    promptMassStep = 25
    signalSubsets = { }

    for sr in opt.signalRegionMap:
        for signal in opt.signalRegionMap[sr]['signals']:

            baseSignal = signal.split('_')[0]
            signalSubsets[baseSignal] = [ ]  

            if opt.verbose: print 'Splitting mass points for', baseSignal          

            massPoints = getMassPointList(signal)

            nMassPoints = len(massPoints) 
            minPromptMass = int(signal.split('_')[1].split('-')[1].split('to')[0])
            maxPromptMass = int(signal.split('_')[1].split('to')[1])
            
            nDivisions = max(1, int(round(float(nMassPoints)/massPointForSubset)))

            if nDivisions==1:
                signalSubsets[baseSignal].append(signal)
                continue

            signalMmassPointForSubset = nMassPoints/nDivisions

            promptMassRangeDraft = signal.split('_')[1].split('-')[0]+'-minPromptMasstomaxPromptMass'
            signalDraft = '_'.join([ baseSignal, promptMassRangeDraft, signal.split('_')[2] ])

            minSubsetPromptMass = minPromptMass

            for division in range(nDivisions):
                for promptMass in range(minSubsetPromptMass, maxPromptMass+1, promptMassStep):
                    
                    signalSubset = signalDraft.replace('minPromptMass', str(minSubsetPromptMass)).replace('maxPromptMass', str(promptMass))
                    massPointSubsets = getMassPointList(signalSubset)

                    if len(massPointSubsets)>=signalMmassPointForSubset or promptMass==maxPromptMass:

                        signalSubsets[baseSignal].append(signalSubset)
                        minSubsetPromptMass = promptMass + promptMassStep
                        break

    for signal in signalSubsets:
        print 'signalSubsets[\''+signal+'\'] = '+repr(signalSubsets[signal])+'\n'               

def getMassPointList(signal):

    massPointList = []
    for massPoint in signalMassPoints.signalMassPoints[signal.split('_')[0]]:
        if signalMassPoints.massPointInSignalSet(massPoint, signal):
            massPointList.append(massPoint)

    return massPointList

### Analysis specific weights, efficiencies, scale factors, etc.

def makeFastSimLeptonEfficiencies(opt):

    cdWorkDir = 'cd '+os.getenv('PWD')+'; eval `scramv1 runtime -sh`;'   
 
    for year in opt.year.split('-'): 
        mergeJobs = {}
        sampleList = []
        if opt.sigset=='SM' or 'DY' in opt.sigset: sampleList.append('DY')
        if 'ttbar' in opt.sigset: sampleList.append('ttbar')
        if 'signal' in opt.sigset or 'TChipm' in opt.sigset: sampleList.extend([ 'TChipmSlepSnu_mC-1150_mX-1', 'TChipmSlepSnu_mC-900_mX-475', 'TChipmSlepSnu_mX-1', 'TChipmSlepSnu_dm-425' ])
        if 'signal' in opt.sigset or 'T2tt' in opt.sigset: sampleList.extend([ 'T2tt_mStop-525_mLSP-350', 'T2tt_mStop-525_mLSP-438', 'T2tt_dm-87', 'T2tt_dm-175' ])
        for reco in [ 'fullsim', 'fastsim' ]:
            if reco=='fullsim' and 'fastsim' in opt.option: continue
            if reco=='fastsim' and 'fullsim' in opt.option: continue
            for sample in sampleList:
                if 'split' in opt.option:
                    for part in range(10): mergeJobs[reco+'_'+sample+'_'+str(part)] = ' '.join([ cdWorkDir, './mkFastSimDYEfficienciesJobs.py', year, reco, sample , str(part) ])
                else:
                    mergeJobs[reco+'_'+sample] = ' '.join([ cdWorkDir, './mkFastSimDYEfficienciesJobs.py', year, reco, sample , '-1' ])      
        if len(mergeJobs.keys())>0:
            latinoTools.submitJobs(opt, 'fastsimlep', year+'EfficiencyJobs', mergeJobs, 'Targets', True, 1) 

def plotFastSimLeptonEfficiencies(opt):

    for year in opt.year.split('-'):
        if opt.sigset=='SM' or opt.sigset=='DY':
            os.system('./mkFastSimDYMorePlots.py '+year+' DY')
        else:                                                 
            for signal in [ 'T2tt_mStop-525_mLSP-350', 'T2tt_mStop-525_mLSP-438' ]:
	        os.system('./mkFastSimDYMorePlots.py '+year+' '+signal)

### Miscellanea

def mergeSearchRegionKinematics(opt):

    if 'SearchRegionKinematics' not in opt.tag:
        print 'Please choose a tag with SearchRegionKinematics'
        exit()

    for year in opt.year.split('-'):
        
        outtag = opt.tag.replace('Kinematics', 'KinematicsMerged')

        samples, cuts, variables, nuisances = commonTools.getDictionariesInLoop(opt.configuration, year, opt.tag, opt.sigset, 'nuisances')

        inputFile  = commonTools.openShapeFile(opt.shapedir, year, opt.tag, opt.sigset, opt.fileset)
        outputFile = commonTools.openShapeFile(opt.shapedir, year, outtag,  opt.sigset, opt.fileset, 'recreate')
 
        for cut in cuts:

            outputFile.mkdir(cut)

            mergedShapes = {}

            for variable in variables:
                if 'cuts' not in variables[variable] or cut in variables[variable]['cuts']:

                    if 'MET_T1' in variables[variable]['name']: continue

                    shapeName = '_'.join([ variableString for variableString in variable.replace('nbjets','nbjets_').split('_') if not variableString.isdigit() ])
                    if shapeName not in mergedShapes:
                        mergedShapes[shapeName] = {}

                    for sample in samples:

                        histoList = [ 'histo_'+sample ]

                        for nuisance in nuisances:
                            if nuisances[nuisance]['type']=='shape':
                                if sample in nuisances[nuisance]['samples']:
                                    if 'cuts' not in nuisances[nuisance] or cut in nuisances[nuisance]['cuts']:
                                        for variation in [ 'Up', 'Down' ]:
                                            histoList.append('_'.join([ 'histo', sample, nuisances[nuisance]['name']+variation ]))

                        for histo in histoList:
 
                            histoName = '/'.join([ cut, variable, histo ])
                            for jeuncert in [ 'jesTotal', 'jer', 'unclustEn' ]:
                                if jeuncert in histo:
                                   histoVariable = histo.replace('histo_','').replace(sample,variable)
                                   if histoVariable in variables:
                                       if 'cuts' not in variables[histoVariable] or cut in variables[histoVariable]['cuts']:
                                           histoName = '/'.join([ cut, histoVariable, 'histo_'+sample ])

                            if histo not in mergedShapes[shapeName]:
                                mergedShapes[shapeName][histo] = inputFile.Get(histoName)
                            else:
                                mergedShapes[shapeName][histo].Add(inputFile.Get(histoName))

            for variable in mergedShapes:

                 outputFile.mkdir(cut+'/'+variable)
                 outputFile.cd(cut+'/'+variable)

                 for histo in mergedShapes[variable]:
                     mergedShapes[variable][histo].Write(histo)

        inputFile.Close()
        outputFile.Close()



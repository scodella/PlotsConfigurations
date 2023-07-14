#!/usr/bin/env python
import os
import sys
import ROOT
import math
import argparse
from array import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

Zmass = 91.1876

treeLevel = '' #'DY' #old version
treeDir   = { 'EOY'   : 'XXX_102X_nAODv6_Full201Yv6loose/SFSusy201Y'+treeLevel+'v6loose/',
              'Sig'   : 'XXX_106X_nAODv9_Full201Yv8/susyGen__susyW__SFSusySig/'}
eosusr    = { 'UL'    : '/eos/home-p/pmatorra/SUS_SF/',
              'EOY'   : '/eos/cms/store/user/scodella/SUSY/Nano/',
              'Sig'   : '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'}
eoscaf    = { 'UL'    : '/eos/home-p/pmatorra/SUS_SF/',
              'EOY'   : '/eos/cms/store/caf/user/scodella/BTV/Nano/',
              'Sig'   : '/gpfs/projects/tier3data/LatinosSkims/RunII/Nano/'}
treeName  = { 'UL'    : 'nanoLatino_DYJetsToLL_M-50-LO__part*root',
              'EOY'   : 'nanoLatino_TTJetsDilep__part*root',
              'SigFS' : 'nanoLatino_TChipmSlepSnu_mC1-825to1500__part*.root',
              'Sig'   : 'nanoLatino_TChipmSlepSnu_mC-900_mX-475__part*.root'}

years     = { 'UL'    : {'2016HIPM'   : { 'fastsim' : eosusr['UL']+'Spring21UL16FS_106X_nAODv9_Full2016v8/SFSusyDY/',
                                          'fullsim' : eosusr['UL']+'Summer20UL16_106X_nAODv9_HIPM_Full2016v8/SFSusyDY/',    } ,
                         '2016noHIPM' : { 'fastsim' : eosusr['UL']+'Spring21UL16FS_106X_nAODv9_Full2016v8/SFSusyDY/',
                                          'fullsim' : eosusr['UL']+'Summer20UL16_106X_nAODv9_noHIPM_Full2016v8/SFSusyDY/',    } ,
                         '2017'       : { 'fastsim' : eosusr['UL']+'Spring21UL17FS_106X_nAODv9_Full2017v8/SFSusyDY/',
                                          'fullsim' : eosusr['UL']+'Summer20UL17_106X_nAODv9_Full2017v8/SFSusyDY/',    } ,
                         '2018'       : { 'fastsim' : eosusr['UL']+'Spring21UL18FS_106X_nAODv9_Full2018v8/SFSusyDY/',
                                          'fullsim' : eosusr['UL']+'Summer20UL18_106X_nAODv9_Full2018v8/SFSusyDY/',    }, 
              },
              'EOY'   : { '2016' : { 'fastsim' : eosusr['EOY']+treeDir['EOY'].replace('XXX', 'Summer16FS').replace('201Y', '2016'), 
                                     'fullsim' : eosusr['EOY']+treeDir['EOY'].replace('XXX', 'Summer16').replace('201Y', '2016')    } ,  
                          '2017' : { 'fastsim' : eosusr['EOY']+treeDir['EOY'].replace('XXX', 'Fall2017FS').replace('201Y', '2017'), 
                                     'fullsim' : eoscaf['EOY']+treeDir['EOY'].replace('XXX', 'Fall2017').replace('201Y', '2017')    } ,  
                          '2018' : { 'fastsim' : eoscaf['EOY']+treeDir['EOY'].replace('XXX', 'Autumn18FS').replace('201Y', '2018'),  
                                     'fullsim' : eoscaf['EOY']+treeDir['EOY'].replace('XXX', 'Autumn18').replace('201Y', '2018')    } 
                },
              'Sig'   : { '2016' : { 'fastsim' : eosusr['Sig']+treeDir['Sig'].replace('XXX', 'Spring21UL16FS').replace('201Y', '2016'), 
                                     'fullsim' : eosusr['Sig']+treeDir['Sig'].replace('XXX', 'Summer20UL16').replace('201Y', '2016')    } ,  
                          '2017' : { 'fastsim' : eosusr['Sig']+treeDir['Sig'].replace('XXX', 'Spring21UL17FS').replace('201Y', '2017'), 
                                     'fullsim' : eoscaf['Sig']+treeDir['Sig'].replace('XXX', 'Summer20UL17').replace('201Y', '2017')    } ,  
                          '2018' : { 'fastsim' : eoscaf['Sig']+treeDir['Sig'].replace('XXX', 'Spring21UL18FS').replace('201Y', '2018'),  
                                     'fullsim' : eoscaf['Sig']+treeDir['Sig'].replace('XXX', 'Summer20UL18').replace('201Y', '2018')    } 
                }

}

def getLeptonMass(pdgId) :

    if abs(pdgId)==11 :
        return 0.000511
    elif abs(pdgId)==13 :
        return 0.105658
    else:
        print 'mt2llProducer: WARNING: unsupported lepton pdgId'
        return -1

def isTightMuon(muon):
    if muon.mediumId==1 and abs(muon.sip3d)<4. and abs(muon.dxy)<0.05 and abs(muon.dz)<0.10 and muon.pfRelIso04_all<0.15:
        return True
    return False

def isTightElectron(electron): 
    if electron.cutBased>=3 and abs(electron.sip3d)<4. and abs(electron.dxy)<0.05 and abs(electron.dz)<0.10 and electron.lostHits==0:
        return True    
    return False

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('--campaign', '-c'   , dest='campaign'         , help='campaign to run options: (UL, EOY, Sig)'
                      , default = 'UL'
                        , choices = ['UL', 'EOY', 'Sig'])
#    args = parser.parse_args()
    parser.add_argument('--year', '-y'      , dest='year'            , help='year'
                      , default  = 'test')
#                      , choices  = years[args.campaign])
    parser.add_argument('--prodset', '-p'   , dest='prodset'         , help='full or fastsim'
                      , default  = ''
                      , required = True
                      , choices  = ['fastsim','fullsim'])
    parser.add_argument('--binning', '-b'   , dest='binning'         , help='want new or old binning'
                        , type     = str.lower
                        , default  = '')
    parser.add_argument('--lepton', '-l'    , dest='lepton'         , help='Run electron, muon or both'
                      , required = True
                      , type     = str.lower    
                      , choices  = ['electron','e', 'muon','m', 'both','b'])
    parser.add_argument('--maxentries', '-m', dest='maxentries'            , help='maximum number of entries to run to (if -1 all ran)'
                      , default  = -1
                      , type     = int)
    parser.add_argument('--sigset', '-s', dest='sigset'            , help='masspoint'
                        , default  = 'TChipmSlepSnu_mC-900_mX-475'
                        , type     = str)
    args = parser.parse_args()
    campaign   = args.campaign
    yearset    = args.year
    prodset    = args.prodset
    maxentries = args.maxentries
    oldbinning = False
    doEle      = False
    doMuo      = False
    lepnm      = ''
    if 'e' in args.lepton:
        leptons = ['Ele']
        doEle   = True
        lepnm   = '_Ele'
    if 'm' in args.lepton:
        leptons = ['Muo']
        doMuo   = True
        doEle   = '_Muo'
    if 'b' in args.lepton:
        leptons = ['Ele', 'Muo']
        doMuo   = True
        doEle   = True
    for year in yearset.split('-'):
        if year not in years[campaign].keys(): 
            print "year not found, please choose one of the following", years[campaign].keys()
            exit()
    print 'Arguments', args
    if 'old' in args.binning: oldbinning=True
    doSignal   = True if 'Sig'     in args.campaign else False
    isFastSim  = True if 'fastsim' in args.prodset  else False
    doSignalFS = bool(doSignal * isFastSim) 
    campaign_nm = campaign
    
                
    if doSignal:
        if isFastSim: 
            mChargino   = args.sigset.split('mC-')[-1].split('_mX')[0]
            mLSP        = args.sigset.split('mX-')[-1]
            campaign_nm = campaign+'FS' 
            print 'Chosen masses', mChargino, mLSP
        else:
            treeName[campaign] = 'nanoLatino_'+args.sigset+'__part*.root'
        #nanoLatino_TChipmSlepSnu_mC-900_mX-475__part1.root
    #matchedLepton = '(LeptonGen_isPrompt[abs(Lepton_genIdx)]==1 || LeptonGen_isDirectPromptTauDecayProduct[abs(Lepton_genIdx)]==1)'
    #matchedGenLepton = '(LeptonGen_isPrompt==1 || LeptonGen_isDirectPromptTauDecayProduct==1)'
    #matchedElectron = '((GenPart_statusFlags[abs(Electron_genPartIdx)] & 1) || (GenPart_statusFlags[abs(Electron_genPartIdx)] >> 5 & 1))'
    #matchedMuon = '((GenPart_statusFlags[abs(Muon_genPartIdx)] & 1) || (GenPart_statusFlags[abs(Muon_genPartIdx)] >> 5 & 1))'
    #matchedLepton = '(LeptonGen_isPrompt[abs(Lepton_genIdx)]==1)'
    #matchedGenLepton = '(LeptonGen_isPrompt==1)'
    #matchedElectron = '((GenPart_statusFlags[abs(Electron_genPartIdx)] & 1))'
    #matchedMuon = '((GenPart_statusFlags[abs(Muon_genPartIdx)] & 1))'    
    #matchedParton = '((GenPart_statusFlags & 1))'

    #leptons = { 'Ele' : 'isTightElectron_cutBasedMediumPOG',
    #            #'Ele' : '(Lepton_electronIdx)' 
    #            'Muo' : 'isTightMuon_mediumRelIsoTight'
    #          }
    if oldbinning:
        binsx = { 'Muo' : [ 10., 20., 35., 50., 100., 200., 500. ],
                  'Ele' : [ -2.400, -1.444, -0.800,  0.000, 0.800, 1.444, 2.400 ] }
        binsy = { 'Muo' : [ 0., 0.9, 1.2, 2.1, 2.4 ],
                  'Ele' : [ 10., 20., 35., 50., 100., 500. ] }
    else:
        binsx = { 'Muo' : [ 10., 20., 35., 50., 100., 200., 500. ],
                  'Ele' : [ -2.4, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.4] }
        binsy = { 'Muo' : [ 0., 0.9, 1.2, 2.1, 2.4 ],
                  'Ele' : [ 10., 20., 35., 50., 100., 500. ] }

    levels = [ 'reco', 'tight' ]
    
    if 'DY' not in treeLevel:
        levels.append('gen')
        levels.append('recogen')
        levels.append('tightgen')

    print "start processing"
    for year in yearset.split('-'):
        outputDir = './Data/'+year+'/'
        os.system('mkdir -p '+outputDir)

        histos = { }

        for sim in prodset.split('-'):
            events = ROOT.TChain('Events') 
            events.Add(years[campaign][year][sim]+treeName[campaign_nm])
            histos[sim] = { }
            for lepton in leptons:
                histos[sim][lepton] = { }
                for level in levels: 
                    histos[sim][lepton][level] = ROOT.TH2F(lepton+'_'+level+'_'+sim, '', len(binsx[lepton])-1, array('d',binsx[lepton]), len(binsy[lepton])-1, array('d',binsy[lepton]))                                                                                            
            nentries = events.GetEntries()            
            if maxentries>0. and maxentries<nentries:
                nentries = maxentries
            progress_threshold = nentries // 20
            print year, sim, nentries 
            for entry in range(nentries):
                if (entry + 1) % progress_threshold == 0:
                    progress_percent = ((entry + 1.) / nentries) * 100
                    print'Progress:', int(progress_percent),'%'
                events.GetEntry(entry)
                if doSignalFS and events.susyMChargino != mChargino and events.susyMLSP!=mLSP  : continue #might have to be refined in the future 
                    
                #print entry, events.GetEntry(entry)

                electrons = Collection(events, 'Electron')
                muons = Collection(events, 'Muon')
                genparticles = Collection(events, 'GenPart')
                if doSignalFS:
                    genModel = 1#Collection(events, 'susy')
                                    
                if 'DY' not in treeLevel:

                    # gen
                    genLep = [ ]
                    genLepPdgId = [ ]
                    genLepReco = [ ]
                    #genLepTight = [ ] 
                    genVec = ROOT.vector('TLorentzVector')()
                    #for glep in range(events.nLeptonGen):
                    #    if genleptons[glep].isPrompt and genleptons[glep].pt>10. and abs(genleptons[glep].eta)<2.4 and (abs(genleptons[glep].pdgId)==11 or abs(genleptons[glep].pdgId)==13):
                    for glep in range(events.nGenPart):
                        if genparticles[glep].pt>10. and abs(genparticles[glep].eta)<2.4 and ((abs(genparticles[glep].pdgId)==11 and doEle) or (abs(genparticles[glep].pdgId)==13 and doMuo)):
                            lepMotherPdgId, lepMotherIdx = -1, genparticles[glep].genPartIdxMother                        
                            if lepMotherIdx>=0:
                                lepMotherPdgId = genparticles[lepMotherIdx].pdgId
                            #print "im in the loop", glep, lepMotherPdgId
                            if abs(lepMotherPdgId)!=23: continue
                            genLepId = genparticles[glep].pdgId # genleptons[glep].pdgId
                            genLep.append(glep)
                            genLepPdgId.append(genLepId)
                            genlepton = ROOT.TLorentzVector()
                            #genlepton.SetPtEtaPhiM(genleptons[glep].pt, genleptons[glep].eta, genleptons[glep].phi, getLeptonMass(genleptons[glep].pdgId))
                            genlepton.SetPtEtaPhiM(genparticles[glep].pt, genparticles[glep].eta, genparticles[glep].phi, getLeptonMass(genparticles[glep].pdgId))
                            genVec.push_back(genlepton)

                            #tidx, ridx = -1, -1
                            ridx = -1
                          
                            ##for tlep in range(events.nLepton):
                            ##    if recoleptons[tlep].genIdx==glep: 
                            ##        tidx = tlep

                            if abs(genLepId)==11:
                                for rlep in range(events.nElectron):
                                    if electrons[rlep].genPartIdx>=0.:
                                        if abs(genparticles[electrons[rlep].genPartIdx].phi-genlepton.Phi())<0.01 and abs(genparticles[electrons[rlep].genPartIdx].eta-genlepton.Eta())<0.01:
                                            ridx = rlep
                                            #for tlep in range(events.nLepton):
                                            #    if recoleptons[tlep].electronIdx==rlep:
                                            #        tidx = tlep 
  
                            elif abs(genLepId)==13:
                                for rlep in range(events.nMuon):
                                    if muons[rlep].genPartIdx>=0.:
                                        if abs(genparticles[muons[rlep].genPartIdx].phi-genlepton.Phi())<0.01 and abs(genparticles[muons[rlep].genPartIdx].eta-genlepton.Eta())<0.01:          
                                            ridx = rlep
                                            #for tlep in range(events.nLepton):
                                            #    if recoleptons[tlep].muonIdx==rlep:
                                            #        tidx = tlep
                            genLepReco.append(ridx)
                            #genLepTight.append(tidx)

                    if len(genLep)==2:
                        #if abs(genleptons[genLep[0]].pdgId)==abs(genleptons[genLep[1]].pdgId):
                        #    if (genleptons[genLep[0]].pdgId*genleptons[genLep[1]].pdgId)<0.:
                        if abs(genLepPdgId[0])==abs(genLepPdgId[1]):
                            if (genLepPdgId[0]*genLepPdgId[1])<0.: 
                                if abs((genVec[0] + genVec[1]).M() - Zmass)<30.:
               
                                    #lepton = 'Ele' if abs(genleptons[genLep[0]].pdgId)==11 else 'Muo'
                                    lepton = 'Ele' if abs(genLepPdgId[0])==11 else 'Muo'
                                    isLeptonTight = []
                                    for glep in range(len(genLep)):
                                        if genLepReco[glep]>=0:
                                            if lepton=='Ele': isLeptonTight.append(isTightElectron(electrons[genLepReco[glep]]))
                                            if lepton=='Muo': isLeptonTight.append(isTightMuon(muons[genLepReco[glep]]))
                                        else: isLeptonTight.append(False)

                                    for glep in range(len(genLep)):
                                        #if genLepTight[1-glep]>=0:
                                        #if (lepton=='Ele' and isTightElectron(electrons[])) or (lepton=='Muo' and ):
                                        if isLeptonTight[1-glep]:

                                            if lepton=='Ele':
                                                obsx = genVec[glep].Eta()
                                                obsy = genVec[glep].Pt()
                                            else:
                                                obsx = genVec[glep].Pt()
                                                obsy = abs(genVec[glep].Eta())
                                     
                                            
                                            histos[sim][lepton]['gen'].Fill(obsx, obsy)
                        
                                            #if genLepTight[glep]>=0: 
                                            #    if (getattr(recoleptons[genLepTight[glep]], leptons[lepton]))==1:
                                            #        histos[sim][lepton]['tightgen'].Fill(obsx, obsy)

                                            if genLepReco[glep]>=0:
                                                histos[sim][lepton]['recogen'].Fill(obsx, obsy)
                                                if isLeptonTight[glep]:
                                                    histos[sim][lepton]['tightgen'].Fill(obsx, obsy)

                # muon
                if doMuo:
                    recoMuo = [ ]
                    #recoMuoTight = [ ]
                    muoVec = ROOT.vector('TLorentzVector')()
                    for muo in range(events.nMuon):
                        if muons[muo].genPartIdx>=0.:
                            if (genparticles[muons[muo].genPartIdx].statusFlags & 1) and muons[muo].pt>10. and abs(muons[muo].eta)<2.4:

                                recoMuo.append(muo)
                                recomuon = ROOT.TLorentzVector()
                                recomuon.SetPtEtaPhiM(muons[muo].pt, muons[muo].eta, muons[muo].phi, getLeptonMass(13))
                                muoVec.push_back(recomuon)

                                #tidx = -1

                                #for tlep in range(events.nLepton): 
                                #    if recoleptons[tlep].muonIdx==muo:  
                                #        tidx = tlep 

                                #recoMuoTight.append(tidx)

                    if len(recoMuo)==2:  
                        if (muons[recoMuo[0]].charge*muons[recoMuo[1]].charge)<0.:
                            if abs((muoVec[0] + muoVec[1]).M() - Zmass)<30.: 

                                for muo in range(len(recoMuo)):   
                                    #if recoMuoTight[1-muo]>=0:
                                    if isTightMuon(muons[recoMuo[1-muo]]):             

                                        histos[sim]['Muo']['reco'].Fill(muoVec[muo].Pt(), abs(muoVec[muo].Eta()))

                                        #if recoMuoTight[muo]>=0:   
                                        if isTightMuon(muons[recoMuo[muo]]):
                                            histos[sim]['Muo']['tight'].Fill(muoVec[muo].Pt(), abs(muoVec[muo].Eta()))    
                # electron
                if doEle:
                    recoEle = [ ]
                    #recoEleTight = [ ]
                    eleVec = ROOT.vector('TLorentzVector')()
                    for ele in range(events.nElectron):
                        if electrons[ele].genPartIdx>=0.:
                            if (genparticles[electrons[ele].genPartIdx].statusFlags & 1) and electrons[ele].pt>10. and abs(electrons[ele].eta)<2.4:

                                recoEle.append(ele) 
                                recoelectron = ROOT.TLorentzVector()
                                recoelectron.SetPtEtaPhiM(electrons[ele].pt, electrons[ele].eta, electrons[ele].phi, getLeptonMass(11))
                                eleVec.push_back(recoelectron)

                                #tidx = -1

                                #for tlep in range(events.nLepton): 
                                #    if recoleptons[tlep].electronIdx==ele:
                                #        tidx = tlep

                                #recoEleTight.append(tidx)

                    if len(recoEle)==2:  
                        if (electrons[recoEle[0]].charge*electrons[recoEle[1]].charge)<0.:                          
                            if abs((eleVec[0] + eleVec[1]).M() - Zmass)<30.:

                                for ele in range(len(recoEle)): 
                                    #if recoEleTight[1-ele]>=0:
                                    if isTightElectron(electrons[recoEle[1-ele]]):

                                        etaSC = eleVec[ele].Eta() #+ electrons[recoEle[ele]].deltaEtaSC

                                        histos[sim]['Ele']['reco'].Fill(etaSC, eleVec[ele].Pt())

                                        #if recoEleTight[ele]>=0: 
                                        if isTightElectron(electrons[recoEle[ele]]):
                                            histos[sim]['Ele']['tight'].Fill(etaSC, eleVec[ele].Pt())

            f = ROOT.TFile.Open(outputDir+'/HistoLeptons_'+campaign+'_'+sim+lepnm+'.root','recreate')
            print "writing information in:", outputDir+'/HistoLeptons_'+campaign+'_'+sim+lepnm+'.root'
            for lepton in leptons:
                for level in levels:
                    histos[sim][lepton][level].Write()
            
            f.Close()



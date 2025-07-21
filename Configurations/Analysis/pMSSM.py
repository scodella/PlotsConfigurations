#!/usr/bin/env python3
import ROOT
import optparse
import numpy
import os
import math 

massZ = 91.1876
btagwp = "btagWeight_1tag_deepcsv_M_1c"

#Binning for pMSSM IDs
pMSSMid1_nbins = 600
pMSSMid1_low = 0.5
pMSSMid1_up = 600.5

pMSSMid2_nbins = 144855
pMSSMid2_low = 0.5
pMSSMid2_up = 144855.5

# Srbin as an integer from 0 to 9
region_to_srbin = {
        "SR10jet": 0,
        "SR1jets": 1,
        "SR1tags": 2,
        "SR20jet": 3,
        "SR2jets": 4,
        "SR2tags": 5,
        "SR30tag": 6,
        "SR3tags": 7,
        "SR40tag": 8,
        "SR4tags": 9,
}


def mt2bin(mt2ll, region):


    #SR1 bins
    if mt2ll < 20:
        return 0
    elif mt2ll >= 20 and mt2ll < 40:
        return 1
    elif mt2ll >= 40 and mt2ll < 60:
        return 2
    elif mt2ll >= 60 and mt2ll < 80:
        return 3
    elif mt2ll >= 80 and mt2ll < 100:
        return 4
    elif mt2ll >= 100 and mt2ll < 160:
        return 5
    elif "SR1" in region:
        return 6


    #SR2 and SR3 bins
    if mt2ll >= 160 and mt2ll < 240:
        return 6
    elif "SR2" in region or "SR3" in region:
        return 7


    #SR1 bins
    if mt2ll < 20:
        return 0
    elif mt2ll >= 20 and mt2ll < 40:
        return 1
    elif mt2ll >= 40 and mt2ll < 60:
        return 2
    elif mt2ll >= 60 and mt2ll < 80:
        return 3
    elif mt2ll >= 80 and mt2ll < 100:
        return 4
    elif mt2ll >= 100 and mt2ll < 160:
        return 5
    elif "SR1" in region:
        return 6


    #SR2 and SR3 bins
    if mt2ll >= 160 and mt2ll < 240:
        return 6
    elif "SR2" in region or "SR3" in region:
        return 7


    #SR4 bins
    if mt2ll >= 240 and mt2ll < 370:
        return 7
    elif mt2ll >= 370:
        return 8

    return -1

    

def get_srmt2bin(region, mt2llbin, srbin):
    if "SR1" in region:
        offset = srbin * 7
    
    
    elif "SR2" in region or "SR3" in region:
        offset = 6 * 7 + (srbin - 6) * 8


    elif "SR4" in region:
        offset = 6 * 7 + (srbin - 16) * 9 + (10 * 8)


    return offset + mt2llbin


def get_srbin(region, isDF, mt2ll):
    srbase = region_to_srbin.get(region, -1)
    if srbase == -1:
        return -1
    srbin = 2 * srbase
    if isDF:
        srbin += 1
    if mt2ll== -1:
        return srbin
    else:
        mt2llbin=mt2bin(mt2ll, region)
        srmt2bin=get_srmt2bin(region, mt2llbin, srbin)

        return srmt2bin 

def get_CRbin(ptmiss, njets):

    ptmiss_bin = 3

    for ptmiss_cut in [ 380., 280., 220., 160. ]:
        if ptmiss>=ptmiss_cut: break
        else: ptmiss_bin -= 1

    if ptmiss_bin<0 or njets==-1: return ptmiss_bin
    if ptmiss_bin>=2: return ptmiss_bin+2
    return 2*ptmiss_bin+(njets>0)

def getBinContent4Weight(histo, valx, valy, sys="unknown", var=0):

  xmin = histo.GetXaxis().GetXmin()
  xmax = histo.GetXaxis().GetXmax()
  ymin = histo.GetYaxis().GetXmin()
  ymax = histo.GetYaxis().GetXmax()

  if xmin>=0: valx = abs(valx)
  if valx<xmin: valx = xmin + 0.001
  if valx>xmax: valx = xmax - 0.001
  if ymin>=0: valy = abs(valy)
  if valy<ymin: valy = ymin + 0.001
  if valy>ymax: valy = ymax - 0.001

  this_weight = histo.GetBinContent(histo.FindBin(valx,valy))

  if var!=0:
      histoError = histo.GetBinError(histo.FindBin(valx,valy))
      if sys=="trigger" or sys=="fastsim":
          weightError = math.sqrt( (0.02*this_weight)*(0.02*this_weight) + (histoError*histoError) )
      else:
          weightError = histoError
      this_weight += sys*weightError
  
  return this_weight

def printEvent(pmssid1, pmssid2, region, srbin, weight, lepton_flavor, njets): 

    print( 
        f"pmssid1: {pmssid1}, "
        f"pmssid2: {pmssid2}, "
        f"Region: {region}, "
        f"srbin: {srbin}, "
        f"Weight: {weight}, "
        f"Flavor: {lepton_flavor}, "
        f"jets: {njets}"
    )

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--year'    , dest='year'       , help='year'  , default="")
    parser.add_option('--sample'  , dest='sample'     , help='sample'  , default="")
    parser.add_option('--syst'    , dest='syst'       , help='syst'  , default="Nominal")
    parser.add_option('--events'  , dest='events'     , help='events to scan'  , default=-1, type=int)
    parser.add_option('--ptmiss'  , dest='ptmiss'     , help='ptmiss cut'  , default=100, type=float)
    parser.add_option("--level"   , dest='level' , default="Full", help="Level")
    parser.add_option("--splitmtll", dest='splitmtll' , default=False, help="Split SRs in mtll bins", action='store_true')
    parser.add_option("--addcr"   , dest='addcr' , default=False, help="Add CRs", action='store_true')
    parser.add_option("--verbose" , dest='verbose' , default=False, help="Verbose", action='store_true')
    parser.add_option("--job"     , dest='job' , default="all", help="Sample tree")
    parser.add_option("--debug"   , dest='debug' , default=False, help="Debug", action='store_true')
    parser.add_option("--debugcr"   , dest='debugcr' , default=False, help="Debug CR", action='store_true')
    parser.add_option("--noweight"   , dest='noweight' , default=False, help="No weight", action='store_true')
    (opt, args) = parser.parse_args()

    #if opt.total:
    #    bins = numpy.intc([pMSSMid1_nbins, pMSSMid2_nbins])
    #    lowedges = numpy.float64([pMSSMid1_low, pMSSMid2_low])
    #    upedges = numpy.float64([pMSSMid1_up, pMSSMid2_up])
    #    thnsparse = ROOT.THnSparseD("Total","Total",2,bins,lowedges,upedges)

    # Binning for signal regionssr_nbins
    sr_nbins = 20 if not opt.splitmtll else (6*7+(6+4)*8+4*9)
    cr_nbins = 16 if opt.addcr else 0
    total_nbins = 1 + sr_nbins + cr_nbins
    sr_low = -0.5
    sr_up = sr_low + total_nbins

    # Binning into arrays for THnSparse
    bins = numpy.intc([pMSSMid1_nbins, pMSSMid2_nbins, total_nbins])
    lowedges = numpy.float64([pMSSMid1_low, pMSSMid2_low, sr_low])
    upedges = numpy.float64([pMSSMid1_up, pMSSMid2_up, sr_up])
    thnsparse = ROOT.THnSparseD(opt.syst,opt.syst,3,bins,lowedges,upedges)  

    thnsparse.Sumw2()

    totalDir = "/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21ULYEARFS_106X_nAODv9_FullYEARv8/susyGen__susyW"
    totalDir = totalDir.replace('YEAR', opt.year).replace('UL20', 'UL').replace('noHIPM','').replace('HIPM','')
    srDir = totalDir + "__FSSusyYEARv8__FSSusyCorrYEARv8__FSSusyNominYEARv8__susyMT2fastSmear"
    srDir = srDir.replace('YEAR', opt.year).replace('noHIPM','').replace('HIPM','')
    if opt.year=='2016noHIPM': 
            srDir = srDir.replace('Corr2016v8','Corr2016v8noHIPM').replace('__susyMT2','noHIPM__susyMT2')
        elif opt.year=='2016HIPM':
            srDir = srDir.replace('Corr2016v8','Corr2016v8HIPM').replace('__susyMT2','HIPM__susyMT2')
    crDir = srDir.replace('fast','crfs')

    samplePart = '__part*' if opt.job=='all' else '__part'+opt.job

    if not opt.debugcr and (opt.level=="total" or opt.level=="full"):

        chainTT = ROOT.TChain('Events')
        print('Opening input file', totalDir+'/nanoLatino_'+opt.sample+samplePart+'.root')
        chainTT.Add(totalDir+'/nanoLatino_'+opt.sample+samplePart+'.root')

    if not opt.debugcr (opt.level=="sr" or opt.level=="full"):

        chain = ROOT.TChain('Events')
        print('Opening input file', srDir+'/nanoLatino_'+opt.sample+samplePart+'.root')
        chain.Add(srDir+'/nanoLatino_'+opt.sample+samplePart+'.root')

    if not opt.level=="total" and opt.addcr:
        print('Opening input file', crDir+'/nanoLatino_'+opt.sample+samplePart+'.root')
        chain.Add(crDir+'/nanoLatino_'+opt.sample+samplePart+'.root')

    count = 0  # number of events passing the ptmiss cut
    
    if not opt.debugcr and (opt.level=="total" or opt.level=="full"):

        for ev in range(chainTT.GetEntries()):

            chain.GetEntry(ev)

            coordinates = numpy.float64([ chain.pMSSMid1, chain.pMSSMid2, 0 ])
            thnsparse.Fill(coordinates, 1.)

    count = 0  # number of events passing the ptmiss cut

    results = []

    summary = {
    "SR10jet": {"SF": 0, "DF": 0},
    "SR1jets": {"SF": 0, "DF": 0},
    "CR1tags": {"SF": 0, "DF": 0},
    "SR20jet": {"SF": 0, "DF": 0},
    "SR2jets": {"SF": 0, "DF": 0},
    "CR2tags": {"SF": 0, "DF": 0},
    "SR30tag": {"SF": 0, "DF": 0},
    "CR3tags": {"SF": 0, "DF": 0},
    "SR40tag": {"SF": 0, "DF": 0},
    "CR4tags": {"SF": 0, "DF": 0}
    }
     
    if   '2016HIPM'   in opt.year: nonpromptLep = { 'rate' : 1.18, 'rateUp' : 0.88, 'rateDown' : 1.48 }
    elif '2016noHIPM' in opt.year: nonpromptLep = { 'rate' : 1.10, 'rateUp' : 0.70, 'rateDown' : 1.50 }
    elif '2017'       in opt.year: nonpromptLep = { 'rate' : 1.38, 'rateUp' : 1.09, 'rateDown' : 1.67 }
    elif '2018'       in opt.year: nonpromptLep = { 'rate' : 1.36, 'rateUp' : 1.11, 'rateDown' : 1.61 }
    else:
        print("pMSSM: year "+opt.year+" unknown")
        exit()

    localDir = "/afs/cern.ch/work/s/scodella/SUSY/CMSSW_13_3_1/src/PlotsConfigurations/Configurations/Analysis/"

    triggerFile = ROOT.TFile.Open(localDir+"Data/"+opt.year+"/TriggerEfficiencies_UL"+opt.year+".root","read")
    triggerEfficiency = { "121" : triggerFile.Get("Leptonpt1pt2/ee/efficiency_MET_full_met_both"),
                          "143" : triggerFile.Get("Leptonpt1pt2/em/efficiency_MET_full_met_both"),
                          "169" : triggerFile.Get("Leptonpt1pt2/mm/efficiency_MET_full_met_both") }

    fastsimFile = ROOT.TFile.Open(localDir+"Data/"+opt.year+"/fastsimLeptonWeights_UL_DY.root","read")
    fastsimScaleFactor = { "11" : fastsimFile.Get("Ele_tight_fullsim"), "13" : fastsimFile.Get("Muo_tight_fullsim") }

    additionalSFDir = localDir+"../../../LatinoAnalysis/NanoGardener/python/data/scale_factor/Full"+opt.year.replace("noHIPM","").replace("HIPM","")+"v8/"
    AdditionalElectronScaleFactorFile = ROOT.TFile.Open(additionalSFDir+"AdditionalSF_"+opt.year.replace("2016","2016_")+"Ele_v2.root","read")
    AdditionalMuonScaleFactorFile     = ROOT.TFile.Open(additionalSFDir+"AdditionalSF_"+opt.year.replace("2016","2016_")+"Muon.root","read")
    additionalScaleFactor = { "11" : AdditionalElectronScaleFactorFile.Get("hSFDataMC_central"), "13" : AdditionalMuonScaleFactorFile.Get("hSFDataMC_central") }

    
    srEntries = chain.GetEntries() if opt.level!="total" else -1
    for ev in range(srEntries): 

        if count >= opt.events and opt.events>0:
            break

        chain.GetEntry(ev)

        if opt.addcr or chain.nLepton == 2:
        
            # Extract pMSSM IDs
            pmssid1 = chain.pMSSMid1
            pmssid2 = chain.pMSSMid2

            #Region area
            njets = chain.nCleanJet
            btagweight = getattr(chain,btagwp)
            nobtagweight=1-btagweight

            # Weights
            if opt.year=="2017":
                sumPtEENoise = 0
                for ijet in range(chain.nJet):
                    if abs(chain.Jet_eta[ijet])>2.650 and abs(chain.Jet_eta[ijet])<3.139 and chain.Jet_pt[ijet]*(1.-chain.Jet_rawFactor[ijet])<50.:
                        sumPtEENoise += chain.Jet_pt[ijet]
                if sumPtEENoise>=60.: continue

            weight = ((chain.MET_T1Smear_pt-chain.MET_pt)<10000.)*chain.puWeight*chain.Flag_goodVertices*chain.Flag_globalSuperTightHalo2016Filter*chain.Flag_HBHENoiseFilter*chain.Flag_HBHENoiseIsoFilter*chain.Flag_EcalDeadCellTriggerPrimitiveFilter*chain.Flag_BadPFMuonFilter*chain.Flag_BadPFMuonDzFilter
            if opt.year=="2017" or opt.year=="2018": weight *= chain.Flag_ecalBadCalibFilter

            if opt.year!="2018":
                weight *= chain.PrefireWeight
            else:
                failHEMVeto = False
                for iele in range(chain.nElectron):
                    if chain.Electron_pt[iele]>30. and chain.Electron_eta[iele]>-3.0 and chain.Electron_eta[iele]<-1.4 and chain.Electron_phi[iele]>-1.57 and chain.Electron_phi[iele]<-0.87:
                        failHEMVeto = True
                        break
                if not failHEMVeto:
                    for ijet in range(chain.nJet):
                        if chain.Jet_pt[ijet]>30. and  chain.Jet_eta[ijet]>-3.2 and chain.Jet_eta[ijet]<-1.2 and chain.Jet_phi[ijet]>-1.77 and chain.Jet_phi[ijet]<-0.67: 
                            failHEMVeto = True
                            break
                if failHEMVeto: weight *= 0.35225285

            if chain.nLepton==2:

                ptmiss = chain.ptmiss_reco
                mt2ll = chain.mt2ll_reco if opt.splitmtll else -1

                # Lepton flavors
                pdg0 = chain.Lepton_pdgId[0]
                pdg1 = chain.Lepton_pdgId[1]
                is_sf = (abs(pdg0) == abs(pdg1))
            
                lepton_flavor = "other"
                region = "other"

                # Lepton flavor tagging for SF/DF
                #def get_flavor(pdg0, pdg1):
                if abs(pdg0) == 11 and abs(pdg1) == 11:
                    lepton_flavor = "ee"
                elif abs(pdg0) == 13 and abs(pdg1) == 13:
                    lepton_flavor = "mumu"
                elif (abs(pdg0) == 11 and abs(pdg1) == 13) or (abs(pdg0) == 13 and abs(pdg1) == 11):
                    lepton_flavor = "emu"
                else:
                    lepton_flavor = "other"

                isDF = lepton_flavor == "emu"
                isSF = lepton_flavor in ["ee", "mumu"]
            
                #Tight cuts
                #electron tight -> Lepton_isTightElectron_cutBasedMediumPOG
                #moun tight -> Lepton_isTightMuon_mediumRelIsoTight

                #Tight cuts
                is_tight0 = (abs(pdg0) == 11 and chain.Lepton_isTightElectron_cutBasedMediumPOG[0]) or \
                (abs(pdg0) == 13 and chain.Lepton_isTightMuon_mediumRelIsoTight[0])
    
                is_tight1 = (abs(pdg1) == 11 and chain.Lepton_isTightElectron_cutBasedMediumPOG[1]) or \
                (abs(pdg1) == 13 and chain.Lepton_isTightMuon_mediumRelIsoTight[1])

                # All events cuts
                selection_cuts = (
                    chain.Lepton_pt[0] >= 25 and abs(chain.Lepton_eta[0]) < 2.4 and
                    chain.Lepton_pt[1] >= 20 and abs(chain.Lepton_eta[1]) < 2.4 and
                    ptmiss > 160 and
                    chain.mll > 20 and
                
                    #cuts values
                    is_tight0 and is_tight1
                )

                #pass_mll = (not is_sf) or (abs(chain.mll - massZ) > 15)
                # Z-veto: only applied for SF (ee or mumu)
                pass_mll = isDF or abs(chain.mll - massZ) > 15.

                if selection_cuts and pass_mll:
                    #flavor = get_flavor(chain.Lepton_pdgId[0], chain.Lepton_pdgId[1])
                    #channel_summary[lepton_flavor] += 1

                    #Region
                    if 160 <= ptmiss < 220:
                        region = "SR10jet" if njets == 0 else "SR1jets"

                    elif 220 <= ptmiss < 280:
                        region = "SR20jet" if njets == 0 else "SR2jets"

                    elif 280 <= ptmiss < 380:
                        region = "SR30tag"

                    elif ptmiss >= 380:
                        region = "SR40tag"
                    
                if region == "other":
                    continue

                isNonPrompt = False
                for ilep in range(2): # Here we selected nLepton==2 and nTightLepton==2
                    thisLepSF = chain.Lepton_RecoSF[ilep]
                    if abs(chain.Lepton_pdgId[ilep])==11:
                        thisLepSF *= chain.Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[ilep]
                        thisLepSF *= getBinContent4Weight(fastsimScaleFactor["11"], chain.Lepton_eta[ilep], chain.Lepton_pt[ilep],  "fastsim", 0)
                    elif abs(chain.Lepton_pdgId[ilep])==13:
                        thisLepSF *= chain.Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[ilep]
                        thisLepSF *= getBinContent4Weight(fastsimScaleFactor["13"], chain.Lepton_pt[ilep],  chain.Lepton_eta[ilep], "fastsim", 0)
                    thisLepSF *= getBinContent4Weight(additionalScaleFactor[str(abs(chain.Lepton_pdgId[ilep]))], chain.Lepton_eta[ilep], chain.Lepton_pt[ilep],  "additional", 0)
                    weight *= thisLepSF
                    if chain.Lepton_promptgenmatched[ilep]!=1: isNonPrompt = True
                if isNonPrompt: weight *= nonpromptLep["rate"]

                weight *= getBinContent4Weight(triggerEfficiency[str(abs(pdg0)*abs(pdg1))], chain.Lepton_pt[0], chain.Lepton_pt[1], "trigger", 0)

                if opt.noweight: weight = 1.

                srbin = get_srbin(region, isDF, mt2ll)

                if srbin >= 0:
                    if njets == 0:
                        coordinates = numpy.float64([pmssid1, pmssid2, srbin+1])
                        thnsparse.Fill(coordinates, weight)
                        if opt.verbose: printEvent(pmssid1, pmssid2, region, srbin, weight * nobtagweight, lepton_flavor, njets)

                    else:
                        # CASE 1: For no btag in jets
                        coordinates_jets = numpy.float64([pmssid1, pmssid2, srbin+1])
                        thnsparse.Fill(coordinates_jets, weight * nobtagweight)
                        if opt.verbose: printEvent(pmssid1, pmssid2, region, srbin, weight * nobtagweight, lepton_flavor, njets)

                        # CASE 2: Btag found
                        if btagweight>0.:
                            if "jets" in region:
                                region_tag = region.replace("jets", "tags")
                                srbin_tag = get_srbin(region_tag, isDF, mt2ll)

                                if srbin_tag >= 0:
                                    coordinates = numpy.float64([pmssid1, pmssid2, srbin_tag+1])
                                    thnsparse.Fill(coordinates, weight * btagweight)
                                    if opt.verbose: printEvent(pmssid1, pmssid2, region_tag, srbin_tag, weight * btagweight, lepton_flavor, njets)
    
                            elif "0tag" in region:
                                region_tag = region.replace("0tag", "tags")
                                srbin_tag = get_srbin(region_tag, isDF, mt2ll)

                                if srbin_tag >= 0:
                                    coordinates = numpy.float64([pmssid1, pmssid2, srbin_tag+1])
                                    thnsparse.Fill(coordinates, weight * btagweight)
                                    if opt.verbose: printEvent(pmssid1, pmssid2, region_tag, srbin_tag, weight * btagweight, lepton_flavor, njets)

                if opt.verbose:

                    #Store event result in the SF/DF channel
                    if lepton_flavor in ["ee", "mumu", "emu"]:
                        results.append({
                            "channel": lepton_flavor,
                            "ptmiss": ptmiss,
                            "njets": chain.nJet,
                            "region": region,
                            "pMSSMid1": chain.pMSSMid1,
                            "pMSSMid2": chain.pMSSMid2
                        })

                    #flavor = "SF" if is_sf else "DF"
                    #summary[region][flavor] += 1

                count += 1

            elif opt.addcr and chain.nLepton>=3:

                if chain.ptmiss_WZ>=160. or chain.ptmiss_WZ>=160. or chain.ptmiss_WZ>=0. or chain.ptmiss_ttZ>=0:

                    nTightLepton = 0
                    for ilep in range(chain.nLepton):
                        if chain.Lepton_isTightElectron_cutBasedMediumPOG[ilep] or chain.Lepton_isTightMuon_mediumRelIsoTight[ilep]: 
                            nTightLepton += 1

                    if nTightLepton>=3:

                        isNonPrompt = False
                        allTightWeight = 1.
                        totalLeptonScaleFactor = []
                        for ilep in range(chain.nLepton):
                            thisLepSF = chain.Lepton_RecoSF[ilep]
                            if chain.Lepton_isTightElectron_cutBasedMediumPOG[ilep]:
                                thisLepSF *= chain.Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[ilep]
                                thisLepSF *= getBinContent4Weight(fastsimScaleFactor["11"], chain.Lepton_eta[ilep], chain.Lepton_pt[ilep],  "fastsim", 0)
                                thisLepSF *= getBinContent4Weight(additionalScaleFactor["11"], chain.Lepton_eta[ilep], chain.Lepton_pt[ilep],  "additional", 0)
                            elif chain.Lepton_isTightMuon_mediumRelIsoTight[ilep]:
                                thisLepSF *= chain.Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[ilep]
                                thisLepSF *= getBinContent4Weight(fastsimScaleFactor["13"], chain.Lepton_pt[ilep],  chain.Lepton_eta[ilep], "fastsim", 0)
                                thisLepSF *= getBinContent4Weight(additionalScaleFactor["13"], chain.Lepton_eta[ilep], chain.Lepton_pt[ilep],  "additional", 0)
                            totalLeptonScaleFactor.append(thisLepSF)
                            allTightWeight *= thisLepSF
                            if chain.Lepton_promptgenmatched[ilep]!=1: isNonPrompt = True

                        if isNonPrompt: weight *= nonpromptLep["rate"]

                        if nTightLepton==3: 
                            weight *= allTightWeight
                        elif nTightLepton==4:
                            minusOneTightWeight = 0.
                            for ilep in range(chain.nLepton):
                                if chain.Lepton_isTightElectron_cutBasedMediumPOG[ilep] or chain.Lepton_isTightMuon_mediumRelIsoTight[ilep]:
                                    minusOneTightWeight += allTightWeight*(1.-totalLeptonScaleFactor[ilep])/totalLeptonScaleFactor[ilep]
                            weight *= (allTightWeight+minusOneTightWeight)

                        if opt.noweight: weight = 1.

                        crbin = -1

                        if chain.nLepton==3 and nTightLepton==3 and chain.deltaMassZ_WZ<999. and chain.ptmiss_WZ>=160.:

                            crbin = get_CRbin(chain.ptmiss_WZ, njets)
                            if crbin>=0:
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+crbin+1])
                                thnsparse.Fill(coordinates_cr, weight * nobtagweight)

                        if chain.nLepton==4 and nTightLepton>=3 and chain.deltaMassZ_ZZ<15.  and chain.ptmiss_ZZ>=160.:

                            crbin = get_CRbin(chain.ptmiss_ZZ, njets)
                            if crbin>=0:
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+6+crbin+1])
                                thnsparse.Fill(coordinates_cr, weight * nobtagweight)

                        if chain.nLepton>=3 and nTightLepton>=3 and njets>=2 and (chain.ptmiss_WZ>=0. or chain.ptmiss_ttZ>=0):

                            crbin = -1

                            if chain.nLepton==4 and chain.deltaMassZ_ttZ<15. and chain.deltaMassZ_ttZ>=0. and chain.ptmiss_ttZ>160.: 
                                crbin = get_CRbin(chain.ptmiss_ttZ, -1)

                            if chain.nLepton==3 and chain.deltaMassZ_WZ<15. and chain.deltaMassZ_WZ>=0. and chain.ptmiss_WZ>=0.:
                                ptxGhost = chain.ptmiss_WZ*math.cos(chain.ptmiss_phi_WZ)
                                ptyGhost = chain.ptmiss_WZ*math.sin(chain.ptmiss_phi_WZ)
                                for ilep in [ chain.lep0idx_WZ, chain.lep1idx_WZ, chain.lep2idx_WZ ]:
                                    if (chain.Lepton_pdgId[ilep]*chain.Lepton_pdgId[chain.lep2idx_WZ])<0 or ilep==chain.lep2idx_WZ:
                                        ptxGhost += chain.Lepton_pt[ilep]*math.cos(chain.Lepton_phi[ilep])
                                        ptyGhost += chain.Lepton_pt[ilep]*math.sin(chain.Lepton_phi[ilep])
                                ptmiss_ttZ3Lep = math.sqrt(ptxGhost*ptxGhost + ptyGhost*ptyGhost)  
                                crbin = get_CRbin(ptmiss_ttZ3Lep, -1)

                            if crbin>=0:
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+12+crbin+1])
                                thnsparse.Fill(coordinates_cr, weight * btagweight)

                        if crbin>=0: count += 1

    if not opt.debug:

        outputDirectory = '/'.join([ './THnSparse', opt.year, opt.sample, 'split/' ])
        outputFileNameList = [ opt.sample, opt.year ]
        if opt.level=="total": outputFileNameList.append('Total')
        elif opt.level=="full": outputFileNameList.append('Full')
        else: outputFileNameList.append('SR')
        if opt.addcr: outputFileNameList.append('CR')
        if opt.splitmtll: outputFileNameList.append('mt2ll')
        if opt.noweight: outputFileNameList.append('noweight')
        if opt.events>0: outputFileNameList.append('evt'+str(opt.events))
        if opt.job!='all': outputFileNameList.append('part'+opt.job)
        outputFileName = outputDirectory+"_".join(outputFileNameList)+".root"

        os.system("mkdir -p "+outputDirectory)

        outputFile = ROOT.TFile.Open(outputFileName, "recreate")
        outputFile.cd()

        thnsparse.Write()

        outputFile.Close()



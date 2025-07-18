#!/usr/bin/env python3
import ROOT
import optparse
import numpy
import os
import math 

massZ = 91.1876
btagwp = "btagWeight_1tag_deepjet_M_1c"

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

if __name__ == '__main__':

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--year'    , dest='year'       , help='year'  , default=-1)
    parser.add_option('--sample'  , dest='sample'     , help='sample'  , default=-1)
    parser.add_option('--events'  , dest='events'     , help='events to scan'  , default=-1, type=int)
    parser.add_option('--ptmiss'  , dest='ptmiss'     , help='ptmiss cut'  , default=100, type=float)
    parser.add_option("--total"   , dest='total' , default=False, help="Total", action='store_true')
    parser.add_option("--splitmtll", dest='splitmtll' , default=False, help="Split SRs in mtll bins", action='store_true')
    parser.add_option("--addcr"   , dest='addcr' , default=False, help="Add CRs", action='store_true')
    parser.add_option("--verbose" , dest='verbose' , default=False, help="Verbose", action='store_true')
    parser.add_option("--job"     , dest='job' , default="all", help="Sample tree")
    parser.add_option("--debug"   , dest='debug' , default=False, help="Debug", action='store_true')
    (opt, args) = parser.parse_args()

    if opt.total:

        bins = numpy.intc([pMSSMid1_nbins, pMSSMid2_nbins])
        lowedges = numpy.float64([pMSSMid1_low, pMSSMid2_low])
        upedges = numpy.float64([pMSSMid1_up, pMSSMid2_up])
        thnsparse = ROOT.THnSparseD("Total","Total",2,bins,lowedges,upedges)

    else:

        # Binning for signal regionssr_nbins
        sr_nbins = 20 if not opt.splitmtll else (6*7+(6+4)*8+4*9)
        cr_nbins = 16 if opt.addcr else 0
        sr_low = 0.5
        sr_up = sr_low + sr_nbins + cr_nbins

        # Binning into arrays for THnSparse
        bins = numpy.intc([pMSSMid1_nbins, pMSSMid2_nbins, sr_nbins+cr_nbins])
        lowedges = numpy.float64([pMSSMid1_low, pMSSMid2_low, sr_low])
        upedges = numpy.float64([pMSSMid1_up, pMSSMid2_up, sr_up])
        thnsparse = ROOT.THnSparseD("Selected","Selected",3,bins,lowedges,upedges)  

    chain = ROOT.TChain('Events')

    signalDir = '/eos/cms/store/group/phys_susy/Chargino/Nano/Spring21ULYEARFS_106X_nAODv9_FullYEARv8/'
    if opt.total: signalDir += 'susyGen__susyW/'
    else: signalDir += 'susyGen__susyW__FSSusyYEARv8__FSSusyCorrYEARv8__FSSusyNominYEARv8__susyMT2fastSmear/'
    signalDir = signalDir.replace('YEAR', opt.year).replace('UL20', 'UL').replace('noHIPM','').replace('HIPM','')
    if not opt.total:
        if opt.year=='2016noHIPM': 
            signalDir = signalDir.replace('Corr2016v8','Corr2016v8noHIPM').replace('__susyMT2','noHIPM__susyMT2')
        elif opt.year=='2016HIPM':
            signalDir = signalDir.replace('Corr2016v8','Corr2016v8HIPM').replace('__susyMT2','HIPM__susyMT2')

    samplePart = '__part*' if opt.job=='all' else '__part'+opt.job

    print('Opening input file', signalDir+'nanoLatino_'+opt.sample+samplePart+'.root')

    chain.Add(signalDir+'nanoLatino_'+opt.sample+samplePart+'.root')

    if not opt.total and opt.addcr:
        chain.Add(signalDir.replace('fast','crfs')+'nanoLatino_'+opt.sample+samplePart+'.root')

    outputDirectory = '/'.join([ './THnSparse', opt.year, opt.sample, 'split/' ])
    outputFileNameList = [ opt.sample, opt.year ]
    if opt.total: outputFileNameList.append('Total')
    else: outputFileNameList.append('SR')
    if opt.addcr: outputFileNameList.append('CR')
    if opt.splitmtll: outputFileNameList.append('mt2ll')
    if opt.job!='all': outputFileNameList.append('part'+opt.job)
    outputFileName = outputDirectory+"_".join(outputFileNameList)+".root"

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

    for ev in range(chain.GetEntries()): 

        if count >= opt.events and opt.events>0:
            break

        chain.GetEntry(ev)

        if opt.total:

            coordinates = numpy.float64([ chain.pMSSMid1, chain.pMSSMid2 ])
            thnsparse.Fill(coordinates, 1.)
            count += 1

        elif opt.addcr or chain.nLepton == 2:
        
            # Extract pMSSM IDs
            pmssid1 = chain.pMSSMid1
            pmssid2 = chain.pMSSMid2

            #Region area
            njets = chain.nCleanJet
            btagweight = getattr(chain,btagwp)
            nobtagweight=1-btagweight

            # Weights
            weight = ((chain.MET_T1Smear_pt-chain.MET_pt)<10000.)*chain.puWeight*chain.Flag_goodVertices*chain.Flag_globalSuperTightHalo2016Filter*chain.Flag_HBHENoiseFilter*chain.Flag_HBHENoiseIsoFilter*chain.Flag_EcalDeadCellTriggerPrimitiveFilter*chain.Flag_BadPFMuonFilter*chain.Flag_BadPFMuonDzFilter
            if opt.year=="2017" or opt.year=="2018": weight *= chain.Flag_ecalBadCalibFilter

            Lepton_RecoSF[0]*Lepton_RecoSF[1]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[0]*Lepton_tightElectron_cutBasedMediumPOG_IdIsoSF[1]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[0]*Lepton_tightMuon_mediumRelIsoTight_IdIsoSF[1]

            ( Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1] + (1. - Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1])*1.36)

            (((Sum$(Electron_pt>30. && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0) && (Sum$(Jet_pt>30. && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)) + (1.-((Sum$(Electron_pt>30. && Electron_eta>-3.0 && Electron_eta<-1.4 && Electron_phi>-1.57 && Electron_phi<-0.87)==0) && (Sum$(Jet_pt>30. && Jet_eta>-3.2 && Jet_eta<-1.2 && Jet_phi>-1.77 && Jet_phi<-0.67)==0)))*0.35225285)

            triggerWeight[1]
            fastsimLeptonWeight
            additionalLeptonWeight[1]             

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
                pass_mll = isDF or abs(chain.mll - massZ) > 15

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

                weight = 1.0
                srbin = get_srbin(region, isDF, mt2ll)

                if srbin >= 0:
                    if njets == 0:
                        coordinates = numpy.float64([pmssid1, pmssid2, srbin])
                        thnsparse.Fill(coordinates, weight)

                    else:
                        # CASE 1: For no btag in jets
                        coordinates_jets = numpy.float64([pmssid1, pmssid2, srbin])
                        thnsparse.Fill(coordinates_jets, weight * nobtagweight)

                        # CASE 2: Btag found
                        if "jets" in region:
                            region_tag = region.replace("jets", "tags")
                            srbin_tag = get_srbin(region_tag, isDF, mt2ll)

                            if srbin_tag >= 0:
                                coordinates = numpy.float64([pmssid1, pmssid2, srbin_tag])
                                thnsparse.Fill(coordinates, weight * btagweight)
    
                        elif "0tag" in region:
                            region_tag = region.replace("0tag", "tags")
                            srbin_tag = get_srbin(region_tag, isDF, mt2ll)

                            if srbin_tag >= 0:
                                coordinates = numpy.float64([pmssid1, pmssid2, srbin_tag])
                                thnsparse.Fill(coordinates, weight * btagweight)

                        if opt.verbose:
                            print(
                                    f"Region: {region_tag}, "
                                    f"srbin: {srbin_tag}, "
                                    f"Weight: {btagweight}, "
                                    f"Flavor: {lepton_flavor}, "
                                    f"jets: {njets}"
                            )



                if opt.verbose:

                    #Store even:wqt result in the SF/DF channel
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

                        weight = 1.0
                        crbin = -1.

                        if chain.nLepton==3 and nTightLepton==3 and chain.deltaMassZ_WZ<999. and chain.ptmiss_WZ>=160.:

                            crbin = get_CRbin(chain.ptmiss_WZ, njets)
                            if crbin>=0:
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+crbin])
                                thnsparse.Fill(coordinates_cr, weight * nobtagweight)

                        if chain.nLepton==4 and nTightLepton>=3 and chain.deltaMassZ_ZZ<15.  and chain.ptmiss_ZZ>=160.:

                            crbin = get_CRbin(chain.ptmiss_ZZ, njets)
                            if crbin>=0:
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+6+crbin])
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
                                coordinates_cr = numpy.float64([pmssid1, pmssid2, sr_nbins+12+crbin])
                                thnsparse.Fill(coordinates_cr, weight * btagweight)

                        if crbin>=0: count += 1

    if not opt.debug and opt.events<0:

        os.system("mkdir -p "+outputDirectory)

        outputFile = ROOT.TFile.Open(outputFileName, "recreate")
        outputFile.cd()

        thnsparse.Write()

        outputFile.Close()



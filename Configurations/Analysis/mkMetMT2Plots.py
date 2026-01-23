#!/usr/bin/env python
import os
import sys
import ROOT
import math
import optparse
from array import *

import LatinoAnalysis.ShapeAnalysis.CMS_lumi as CMS_lumi
CMS_lumi.lumi_13TeV = "138 fb^{-1}"
isPreliminary=False
CMS_lumi.writeExtraText = 1
if isPreliminary:
    CMS_lumi.extraText = "Preliminary"
else:
    CMS_lumi.extraText = "Simulation"
    CMS_lumi.relPosX = 0.14
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.lumiTextSize     = 0.4
CMS_lumi.lumiTextOffset   = 0.1
CMS_lumi.cmsTextSize      = 0.5

signals  = sys.argv[1]
cut      = sys.argv[2]
variable = sys.argv[3]

smProcesses = [ "ttbar", "STtW", "WW", "WZ", "ZZTo2L2Nu", "DY", "ttZ", "ttW", "Higgs", "VVV", "VZ" ]

ptmissBins = { "flat" : [ 10.*x for x in range(51) ], "bins" : [ 0, 100, 160, 220, 280, 380, 500 ] }
mt2llBins  = { "flat" : [ 10.*x for x in range(51) ], "bins" : [ 0, 20, 40, 60, 80, 100, 160, 240, 370, 500 ] }

def Pad2TAxis(hist, scale=1., scaleoffsetx=1., scaleoffsety=1., scaleofftitlex=1., scaleofftitley=1.):
         xaxis = hist.GetXaxis()
         xaxis.SetLabelFont ( 42)
         xaxis.SetLabelOffset( 0.025*scaleoffsetx)
         xaxis.SetLabelSize ( 0.1*scale)
         xaxis.SetNdivisions ( 505)
         xaxis.SetTitleFont ( 42)
         xaxis.SetTitleOffset( 1.35*scaleofftitlex)
         xaxis.SetTitleSize ( 0.11*scale)

         yaxis = hist.GetYaxis()
         #yaxis.CenterTitle ( )
         yaxis.SetLabelFont ( 42)
         yaxis.SetLabelOffset( 0.02*scaleoffsety)
         yaxis.SetLabelSize ( 0.1*scale)
         yaxis.SetNdivisions ( 505)
         yaxis.SetTitleFont ( 42)
         if '#frac' in yaxis.GetTitle(): yaxis.SetTitleOffset( .5*scaleofftitley)
         else: yaxis.SetTitleOffset( .6*scaleofftitley)
         yaxis.SetTitleSize ( 0.11*scale)

def makeHisto(sample, processList, histoName, binning):

    firstHisto = True
    for year in [ "2016", "2017", "2018" ]:
        inputFile = ROOT.TFile.Open("./Shapes/"+year+"/MetMTVetoesUL/plots_MetMTVetoesUL_"+sample+".root", "read")
        for process in processList:
            if firstHisto:
                histo = inputFile.Get(histoName+process)
                histo.SetDirectory(0)
                firstHisto = False
            else:
                histo.Add(inputFile.Get(histoName+process))

    if "_vs_" not in histoName:
        histo.SetTitle("")
        histo.Scale(1./histo.Integral(-1,-1))
        return histo

    scatter = ROOT.TH2F("scatter", "", len(ptmissBins[binning])-1, array('d',ptmissBins[binning]), len(mt2llBins[binning])-1, array('d',mt2llBins[binning]))
    scatter.SetDirectory(0)
    for ptmb in range(len(ptmissBins[binning])-1):
        ptmv = (ptmissBins[binning][ptmb]+ptmissBins[binning][ptmb+1])/2.
        for mt2b in range(1, len(mt2llBins[binning])-1):
            mt2v = (mt2llBins[binning][mt2b]+mt2llBins[binning][mt2b+1])/2.
            ptmmt2b = scatter.FindBin(ptmv, mt2v)
            scatter.SetBinContent(ptmmt2b, histo.GetBinContent(ptmb*(len(mt2llBins[binning])-1)+mt2b+1))

    scatter.Scale(1./scatter.Integral())
    return scatter

LSP = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
CHR = '#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}'
CHP = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{+}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
CHM = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{-}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
STP = '#tilde{t}_{1}'
STB = "#bar{#kern[0.1]{"+STP+"}}"
SLE = '#tilde{#font[12]{l}}'

def getSignalLegend(signal):

    massPointName = signal.replace(signal.replace('EOY','').split('_')[0],'')
    massPointName = signal.replace('_mS-', '($m_{\\text{'+STP+'}}=').replace('_mC-', '($m_{\\text{'+CHR+'}}=').replace('_mX-', 'GeV$ m_{'+LSP+'}=')+'GeV)'
    mX = signal.split('_mX-')[1]
    if '_mS-' in signal:
        mS = signal.split('_mS-')[1].split('_')[0]
        massPointName = STP+'#kern[0.15]{'+STB+'},#kern[1.2]{'+STP+'}#kern[0.3]{#rightarrow}#kern[0.8]{t}#kern[0.3]{'+LSP+'},  (#font[50]{m}#kern[0.1]{_{#lower[-0.12]{'+STP+'}}}#kern[0.3]{=}#kern[0.1]{'+mS+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'
    if '_mC-' in signal:
        mC = signal.split('_mC-')[1].split('_')[0]
        if 'SlepSnu' in signal:
            massPointName = CHP+'#kern[0.3]{'+CHM+'}, '+CHR+'#kern[0.15]{#rightarrow}#kern[0.15]{#tilde{#font[12]{l}}#nu/#font[12]{l}#tilde{#nu}}#kern[0.15]{#rightarrow}#kern[0.15]{#font[12]{l}}#nu'+LSP+', (#font[50]{m}_{'+CHR+'}#kern[0.3]{=}#kern[0.1]{'+mC+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'
        elif 'pmWW' in signal:
            massPointName = CHP+'#kern[0.3]{'+CHM+'}, '+CHR+'#kern[0.15]{#rightarrow}#kern[0.15]{W}'+LSP+', (#font[50]{m}_{'+CHR+'}#kern[0.3]{=}#kern[0.1]{'+mC+'}#kern[0.1]{GeV},#kern[0.15]{#font[50]{m}_{'+LSP+'}}#kern[0.3]{=}#kern[0.1]{'+mX+'}#kern[0.1]{GeV})'

    return massPointName

if __name__ == '__main__':

    histoName = "/".join([ cut, variable, "histo_" ])
    binning = "bins" if "bins" in variable else "flat"
    bkgHisto = makeHisto("SM", smProcesses, histoName, binning)
    sigHisto = {}
    for signal in signals.split(","):
        sigHisto[signal] = makeHisto("tab"+signal.split("_")[0], [ signal ], histoName, binning)

    ROOT.gStyle.SetOptStat(0)

    plotCanvas = ROOT.TCanvas( 'plotCanvas', '', 800, 800)
    CMS_lumi.CMS_lumi(plotCanvas, 4, 0.)

    signalColor = [ 2, 4, 8, 6, 7 ]
    signalColor = [ '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581' ]
    bkgColor = "#3f90da"

    if "_vs_" in histoName:

        bkgHisto.Draw("scat")
        plotCanvas.Print("./Plots/MetMT2/bkg.png")

        col = 0
        for signal in sigHisto:
            sigHisto[signal].SetMarkerColor(signalColor[col])
            sigHisto[signal].SetLineColor(signalColor[col])
            sigHisto[signal].Draw("scat")
            plotCanvas.Print("./Plots/MetMT2/sig_"+signal+".png")
            col += 1

        bkgHisto.Draw("scat")
        for signal in sigHisto:
            sigHisto[signal].Draw("scatsame")
        plotCanvas.Print("./Plots/MetMT2/scat_"+signals+".png")

    else:

        plotCanvas.Divide(1, 1)
        CMS_lumi.CMS_lumi(plotCanvas, 4, 0)
        gPad = plotCanvas.GetPad(1)
        gPad.cd()
        gPad.SetLogy(1)
        gPad.SetBottomMargin(0.11)
        #gPad.SetLeftMargin(0.12)
        #gPad.SetRightMargin(0.05)
        CMS_lumi.CMS_lumi(gPad, 4, 0)
        Pad2TAxis(bkgHisto, 0.37, 0.3, 0.28, 0.9, 2.1)
        bkgHisto.SetXTitle("#font[50]{p}_{T}^{miss} [GeV]")
        bkgHisto.SetYTitle("Fraction of events / 10 GeV")
        bkgHisto.SetLineWidth(2)
        if type(bkgColor)==int:
            bkgHisto.SetFillColor(bkgColor) 
        else:
            bkgHisto.SetFillColor(ROOT.TColor.GetColor(bkgColor))
        bkgHisto.SetMaximum(100*bkgHisto.GetMaximum())
        bkgHisto.Draw("histo")

        tlegend = ROOT.TLegend(0.15, 0.7, 0.88, 0.88)
        tlegend.SetFillColor(0)
        tlegend.SetTextFont(42)
        tlegend.SetTextSize(0.025)
        tlegend.SetLineColor(0)
        tlegend.SetShadowColor(0)
        tlegend.AddEntry(bkgHisto, "SM processes", "F")
        tlegend.Draw()

        #sigHisto.Scale(100)
        col = 0
        for signal in sigHisto:
            sigHisto[signal].SetLineWidth(2)
            if type(signalColor[col])==int:
                sigHisto[signal].SetLineColor(signalColor[col])
            else:
                sigHisto[signal].SetLineColor(ROOT.TColor.GetColor(signalColor[col]))
            sigHisto[signal].Draw("histosame")
            tlegend.AddEntry(sigHisto[signal], getSignalLegend(signal), "L")
            col += 1

        tlegend.Draw()

        plotCanvas.Print("./Plots/MetMT2/"+variable+"_"+signals+".png")



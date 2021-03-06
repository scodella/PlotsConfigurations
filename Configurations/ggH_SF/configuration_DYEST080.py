# example of configuration file

tag = 'BG_DY_NOHR_MVA080'

# used by mkShape to define output directory for root files
outputDir = 'rootFile'


# file with list of variables
variablesFile = 'variables_DYEST.py'

# file with list of cuts
cutsFile = 'cuts_DYEST080.py' 

# file with list of samples
samplesFile = 'samples_DYEST.py' 

# file with list of samples
plotFile = 'plot.py' 



# luminosity to normalize to (in 1/fb)
# lumi = 2.264
#lumi = 2.318
lumi = 12.2950

# used by mkPlot to define output directory for plots
# different from "outputDir" to do things more tidy
outputDirPlots = 'plotGGH'


# used by mkDatacards to define output directory for datacards
outputDirDatacard = 'datacards'


# structure file for datacard
structureFile = 'structure.py'


# nuisances file for mkDatacards and for mkShape
#nuisancesFile = 'nuisances.py'


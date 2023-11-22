#!/usr/bin/env python
import optparse, types

import PlotsConfigurations.Tools.commonTools as commonTools
import PlotsConfigurations.Tools.latinoTools as latinoTools
import PlotsConfigurations.Tools.combineTools as combineTools
import analysisTools


def allfunctions(toolList):
    all_fns= []
    for tool_i in toolList:
        for attr_name in dir(tool_i):
            attr_value = getattr(tool_i, attr_name)
            if isinstance(attr_value, types.FunctionType):
                all_fns.append(attr_name)
    return all_fns

def sim_strings(str1, str2):
    #Find similar strings by using the Jaro-Winkler coefficients
    str1 = str1.lower()
    str2 = str2.lower()

    len1 = len(str1)
    len2 = len(str2)

    if len1 == 0 and len2 == 0:
        return 1.0

    match_distance = max(len1, len2) // 2 - 1

    matches = 0
    transpositions = 0

    flagged_1 = []
    flagged_2 = []

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if str2[j] == str1[i] and j not in flagged_2:
                matches += 1
                flagged_1.append(i)
                flagged_2.append(j)
                break

    flagged_2.sort()

    for i, index in enumerate(sorted(flagged_1)):
        if str1[index] != str2[flagged_2[i]]:
            transpositions += 1

    transpositions //= 2

    if matches == 0:
        return 0.0

    sim = ((matches / float(len1)) +
            (matches / float(len2)) +
            ((matches - transpositions) / float(matches))) / 3

    # Jaro-Winkler distance
    prefix = 0
    for i in range(min(len(str1), len(str2))):
        if str1[i] == str2[i]:
            prefix += 1
        else:
            break
    prefix = min(4, prefix)  # maximum prefix length is 4

    string_similarity = sim + (0.1 * prefix * (1 - sim))
    return string_similarity
if __name__ == '__main__':

    # Input parameters
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--action'          , dest='action'          , help='Action to be performed'         , default='shapes')
    parser.add_option('--configuration'   , dest='configuration'   , help='Configuration file'             , default='configuration.py')
    parser.add_option('--lepton'          , dest='lepton'          , help='Only check one lepton?'         , default='e')
    parser.add_option('--campaign'        , dest='campaign'        , help='Campaign for Fast/FullSim SF'   , default='UL')
    parser.add_option('--tag'             , dest='tag'             , help='Tag'                            , default='test')
    parser.add_option('--year'            , dest='year'            , help='year'                           , default='test')
    parser.add_option('--sigset'          , dest='sigset'          , help='Sample to run on'               , default='SM')
    parser.add_option('--fileset'         , dest='fileset'         , help='Input shape file'               , default='')
    parser.add_option('--option'          , dest='option'          , help='Options for the action'         , default='')
    parser.add_option('--minLogC'         , dest='minLogC'         , help='MinLog value for plotting'      , default='0.1')
    parser.add_option('--treeName'        , dest='treeName'        , help='Name of the input tree'         , default='Events')
    parser.add_option('--keepallplots'    , dest='keepallplots'    , help='Keep all plots'                 , default=False, action='store_true')
    parser.add_option('--shapedir'        , dest='shapedir'        , help='Directory to store shapes'      , default='./Shapes')
    parser.add_option('--plotsdir'        , dest='plotsdir'        , help='Directory to store plots'       , default='./Plots')
    parser.add_option('--cardsdir'        , dest='cardsdir'        , help='Directory to store datacards'   , default='./Datacards')
    parser.add_option('--limitdir'        , dest='limitdir'        , help='Directory to store limits'      , default='./Limits')
    parser.add_option('--gofitdir'        , dest='gofitdir'        , help='Directory to store GOF results' , default='./GoodnessOfFits')
    parser.add_option('--mlfitdir'        , dest='mlfitdir'        , help='Directory to store ML fits'     , default='./MaxLikelihoodFits')
    parser.add_option('--impactdir'       , dest='impactdir'       , help='Directory to store impacts'     , default='./Impacts')
    parser.add_option('--tabledir'        , dest='tabledir'        , help='Directory to store tables'      , default='./Tables')
    parser.add_option('--datadir'         , dest='datadir'         , help='Directory to store input data'  , default='./Data')
    parser.add_option('--batchQueue'      , dest='batchQueue'      , help='Queue for the batch jobs'       , default='cms_high')
    parser.add_option('--logs'            , dest='logs'            , help='Directory with log files'       , default='./logs')
    parser.add_option('--logprocess'      , dest='logprocess'      , help='Process for log inspection'     , default='mkShapes')
    parser.add_option('--dryRun'          , dest='dryRun'          , help='do not submit jobs'             , default=False, action='store_true')
    parser.add_option('--interactive'     , dest='interactive'     , help='Run jobs in interactive'        , default=False, action='store_true')
    parser.add_option('--debug'           , dest='debug'           , help='Print command (no execute it)'  , default=False, action='store_true')
    parser.add_option('--unblind'         , dest='unblind'         , help='Unblind data in limits'         , default=False, action='store_true')
    parser.add_option('--verbose'         , dest='verbose'         , help='Activate debug printing'        , default=False, action='store_true')
    parser.add_option('--reset'           , dest='reset'           , help='Reset existing shapes'          , default=False, action='store_true')
    parser.add_option('--recover'         , dest='recover'         , help='Recover missing shapes'         , default=False, action='store_true')
    parser.add_option('--deepMerge'       , dest='deepMerge'       , help='Merge shepes in deep mode'      , default=None)
    parser.add_option('--combineLocation' , dest='combineLocation' , help='Combine CMSSW Directory'        , default='COMBINE')
    parser.add_option('--iihe-wall-time'  , dest='IiheWallTime'    , help='Requested IIHE queue Wall Time' , default='168:00:00')
    (opt, args) = parser.parse_args()

    analysisTools.setAnalysisDefaults(opt)
    noModule=True
    for tool in [ commonTools, latinoTools, combineTools, analysisTools ]:
        #print "this is tool",tool
        if hasattr(tool, opt.action):
            noModule=False
            module = getattr(tool, opt.action)
            print 'Running', opt.action
            module(opt)





    
    if noModule:
        print 'no action named '+opt.action
        allTools = [ commonTools, latinoTools, combineTools, analysisTools ]
        allActions =  allfunctions([commonTools, latinoTools, combineTools, analysisTools])

        similarity_threshold = 0.9
        similaractions = []
        for action in allActions:
            similarity = sim_strings(action, opt.action)
            if similarity >= similarity_threshold:
                similaractions.append(action)

        print "No action named "+opt.action+",did you mean: "+','.join(similaractions)+" ?"

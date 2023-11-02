###
# Adds category number as a separate branch
###
from __future__ import print_function
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from ROOT import LeptonSFHelper

#from functools import cmp_to_key
#from ROOT import Mela, SimpleParticle_t, SimpleParticleCollection_t, TVar, TLorentzVector
#from ctypes import c_float



class catFiller(Module):

    def __init__(self, debug=False):
        self.writeHistFile = False
        self.DEBUG = debug
        # unused yet
        #self.leptonPresel = (lambda l : (abs(l.pdgId)==13 and l.pt>5 and abs(l.eta) < 2.4) or (abs(l.pdgId)==11 and l.ZZFullId))


    def endJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nCategory", "I")


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        eventId='{}:{}:{}'.format(event.run,event.luminosityBlock,event.event)
        if self.DEBUG : print ('Event '+eventId)
 
        # Collections
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, 'Jet')
        njet = len(jets)
        #fsrPhotons = Collection(event, "FsrPhoton")
        leps = list(electrons) + list(muons)
        nlep = len(leps)
        nCategory = 0
        
        if nlep == 2:
            if njet == 4:
                nCategory = 1
            elif njet == 6:
                nCategory = 2
        elif nlep == 3:
            if njet == 4:
                nCategory = 3
        elif nlep == 4:
            if njet == 2:
                nCategory = 4
            elif njet == 4:
                nCategory = 5
        elif nlep == 5: 
            if njet == 2:
                nCategory = 6
        elif nlep == 6:
            if njet == 0:
                nCategory = 7

        if nCategory==0:
            return False

        self.out.fillBranch("nCategory", nCategory)
        return True

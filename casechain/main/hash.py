from . import models
import hashlib
from .models import Verdict
from .models import Fact
from .models import Consenus
from .models import View
from .models import StatementOfFacts


def calculateHash (case_id):

    # get a specific case
    case = models.Case.objects.get(id=case_id)

    # create sha256 object
    hash = hashlib.sha256()
    # insert hash of data
    hash.update(bytes(caseToString(case), "utf-8"))


    return hash.hexdigest()

def calculateHashNoId (case, verdicts, facts, consensuses, views):
    # create sha256 object
    hash = hashlib.sha256()
    # insert hash of data
    hash.update(bytes(caseToStringNoId(case, verdicts, facts, consensuses, views), "utf-8"))


    return hash.hexdigest()

def caseToString (case):

    case_as_string = repr(case.date) + repr(case.court) + repr(case.plaintiff) + repr(case.defendant) + repr(case.nonce) + repr(case.prevHashValue) + repr(case.caseFile) \
                     + factsToString(case) + consensusesToString(case) + viewsToString(case) \
                     + verdictsToString(case)

    with open('withid.txt'+repr(case.court),'w') as f:
        f.write(case_as_string)

    return case_as_string

def caseToStringNoId (case, verdicts, facts, consensuses, views):

    case_as_string = repr(case.date) + repr(case.court) + repr(case.plaintiff) + repr(case.defendant) + repr(case.nonce) + repr(case.prevHashValue) + repr(case.caseFile)\
                     + factsToStringNoId(facts) + consensusesToStringNoId(consensuses) + viewsToStringNoId(views) +\
                     verdictsToStringNoId(verdicts)
    print(case_as_string)

    with open('withoutid.txt','w') as f:
        f.write(case_as_string)

    return case_as_string

def factsToString (case):
    sof = StatementOfFacts.objects.get(case=case.id)
    facts = Fact.objects.filter(statementOfFacts=sof.id)
    fact_string = ""
    for fact in facts:
        fact_string= fact_string + fact.fact +'\n'

    return fact_string

def factsToStringNoId (facts):
    fact_string = ""
    for fact in facts:
        fact_string= fact_string + fact.fact +'\n'

    return fact_string

def consensusesToString (case):
    sof = StatementOfFacts.objects.get(case=case.id)
    consensuses = Consenus.objects.filter(statementOfFacts=sof.id)
    consensus_string = ""
    for consensus in consensuses:
        consensus_string= consensus_string + consensus.opinion +'\n'

    return consensus_string

def consensusesToStringNoId (consensuses):
    consensus_string = ""
    for consensus in consensuses:
        consensus_string= consensus_string + consensus.opinion +'\n'

    return consensus_string

def viewsToString (case):
    sof = StatementOfFacts.objects.get(case=case.id)
    views = View.objects.filter(statementOfFacts=sof.id)
    view_string = ""
    for view in views:
        view_string = view_string+view.viewer + view.view +'\n'

    return view_string

def viewsToStringNoId (views):
    view_string = ""
    for view in views:
        view_string = view_string+view.viewer + view.view +'\n'


    return view_string

def verdictsToString (case):
    verdicts = Verdict.objects.filter(case=case.id)
    verdict_string = ""
    for verdict in verdicts:
        if verdict.verdict_type == "intermediate":
            verdict_string = verdict_string + verdict.text +'\n'
        else:
            end = verdict.text

    verdict_string = verdict_string + end
    return verdict_string

def verdictsToStringNoId (verdicts):
    verdict_string = ""
    for verdict in verdicts:
        if verdict.verdict_type == "intermediate":
            verdict_string = verdict_string + verdict.text +'\n'
        else:
            end = verdict.text

    verdict_string = verdict_string + end
    return verdict_string

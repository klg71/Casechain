from . import models
from .models import Verdict
from .models import Fact
from .models import Consenus
from .models import View
from .models import StatementOfFacts
import json

def exportCase(case_id):
    case = models.Case.objects.get(id=case_id)
    sof = StatementOfFacts.objects.get(case=case.id)
    facts = Fact.objects.filter(statementOfFacts=sof.id)
    consensuses = Consenus.objects.filter(statementOfFacts=sof.id)
    views = View.objects.filter(statementOfFacts=sof.id)
    verdicts = Verdict.objects.filter(case=case.id)

    case_export = {}
    case_export["date"] = str(case.date)
    case_export["court"] = case.court
    case_export["plaintiff"] = case.plaintiff
    case_export["dependent"] = case.defendant
    case_export["hash"] = case.hashValue
    case_export["case_file"]=case.caseFile
    case_export["prevhash"] = case.prevHashValue
    case_export["nonce"] = case.nonce
    case_export["id"]=case.id

    case_export["statementOfFacts"] = {"case" : sof.case.id}

    case_export["facts"] = []
    for fact_ in facts:
        fact={}
        fact["fact"] = fact_.fact
        fact["statementOfFacts"] = fact_.statementOfFacts.id
        case_export["facts"].append(fact)

    case_export["views"] = []
    for view_ in views:
        view={}
        view["viewer"] = view_.viewer
        view["view"] = view_.view
        view["statementOfFacts"] = view_.statementOfFacts.id
        case_export["views"].append(view)

    case_export["consensuses"] = []
    consensus = {}
    for consensus_ in consensuses:
        consensus["opinion"] = consensus_.opinion
        consensus["statementOfFacts"] = consensus_.statementOfFacts.id
        case_export["consensuses"].append(consensus)

    case_export ["verdicts"] = []
    verdict = {}
    for verdict_ in verdicts:
        verdict["type"] = verdict_.verdict_type
        verdict["text"] = verdict_.text
        verdict["case"] = verdict_.case.id
        case_export ["verdicts"].append(verdict)

    return json.dumps(case_export)

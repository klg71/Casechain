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
    views = View.objects.filter(statementOfFacts=case.id)
    verdicts = Verdict.objects.filter(case=case.id)

    case_export = {}
    case_export["date"] = str(case.date)
    case_export["court"] = case.court
    case_export["plaintiff"] = case.plaintiff
    case_export["dependent"] = case.defendant
    case_export["hash"] = case.hashValue
    case_export["prevhash"] = case.prevHashValue
    case_export["nonce"] = case.nonce


    case_export["facts"] = []
    fact = {}
    for fact_ in facts:
        fact["fact"] = fact_.fact
        case_export["facts"].append(fact)

    case_export["views"] = []
    view = {}
    for view_ in views:
        view ["viewer"] = view_.viewer
        view ["view"] = view_.view
        case_export ["views"].append(view)

    case_export["consensuses"] = []
    consensus = {}
    for consensus_ in consensuses:
        consensus["opinion"] = consensus_.opinion
        case_export["consensuses"].append(consensus)

    case_export ["verdicts"] = []
    verdict = {}
    for verdict_ in verdicts:
        verdict ["type"] = verdict_.verdict_type
        verdict ["text"] = verdict_.text
        case_export ["verdicts"].append(verdict)

    return json.dumps(case_export)

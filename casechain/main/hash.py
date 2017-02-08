from . import models
import hashlib
from .models import Verdict

def calculateHash (case_id):

    # get a specific case
    case = models.Case.objects.get(id=case_id)

    # create sha256 object
    hash = hashlib.sha256()
    # insert hash of data
    hash.update(bytes(repr(case.date), "utf-8"))

    print(hash.hexdigest())

    return hash.hexdigest()

def caseToString (case):

    case_as_string = repr(case.date) + repr(case.court) + repr(case.plaintiff) + repr(case.defendant) + repr(case.hash)\
                     + repr(case.nonce)


    return case_as_string

def verdictToString (case):
    verdicts = Verdict.objects.filter(case=case.id)
    #for verdict in verdicts:
        #if verdict.verdict_type


    string="test"
    return string
from django.shortcuts import render
from . import models
from . import hash
import hashlib
import json
from django.http.response import HttpResponse


# Create your views here.

class CaseViews:

    def viewCases(self,request):
        cases = models.Case.objects.filter()
        return render(request, 'main/index.html', {'cases': cases})

    def viewCase(self,request,case_id=None):
        case = models.Case.objects.get(id=case_id)
        verdictList = models.Verdict.objects.filter(case_id=case_id)
        statementOfFactsId = models.StatementOfFacts.objects.filter(case_id=case_id).values('id')
        factList = models.Fact.objects.filter(statementOfFacts_id=statementOfFactsId)
        viewList = models.View.objects.filter(statementOfFacts_id=statementOfFactsId)
        consensusList = models.Consenus.objects.filter(statementOfFacts_id=statementOfFactsId)
        return render(request,'main/test.html',{
            'case': case,
            'verdicts': verdictList,
            'views': viewList,
            'facts': factList
        })

    def addText(self,request):
        """
        Adds a Text to a case
        """
        pass


    def addCase(self,request):
        case = models.Case(
            date=request.POST['date'],
            court=request.POST['court'],
            plaintiff=request.POST['plaintiff'],
            defendant=request.POST['defendant'],
        #   hashValue= get that shit
        #   preHashValue= get that shit as well
        #   nonce = get that shit also
        )
        pass

    def receiveCase(self,request):
        """
        Method to receive a case from other nodes
        """
        if 'case' in request.POST:
            caseJson=json.loads(request.POST['case'])
            case=models.Case(date=caseJson['date'],
                             court=caseJson['court'],
                             plaintiff=caseJson['plaintiff'],
                             defendant=caseJson['defendant'],
                             hashValue=caseJson['hashValue'],
                             prevHashValue=caseJson['prevHashValue'],
                             nonce=caseJson['nonce']
                             )
            if string(hashLib.calculateHash(case)) != string(caseJson['hashValue']):
                error="sha256 hash incorrect"
                return HttpResponse(json.dumps({'error':error}))
    

    def __checkCase(self,case_id):
        cases=Case.objects.filter(id<=case_id)
        for case in cases:
            if case.hash != hash.calculateHash(case_id):
                return False



    def __createHashValue(self,caseId):
        """
        Calculates Hash Value for given case
        """
        hashSha265=hashlib.sha256()
        case=Case.objects.get(id=caseId)
        hashSha265.update(bytes(case.nonce,"utf-8"))
        texts=Text.objects.filter(case=case.id)
        for text in texts:
            hashSha265.update(text.text)


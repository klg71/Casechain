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
        return render(request,'main/item.html',{
            'case': case,
            'verdicts': verdictList,
            'views': viewList,
            'facts': factList
        })


    def getCaseForm(self,request):
        return render(request, 'main/new.html')


    def addCase(self,request):
        # case = models.Case(
        #     date=request.POST['date'],
        #     court=request.POST['court'],
        #     plaintiff=request.POST['plaintiff'],
        #     defendant=request.POST['defendant'],
        #   hashValue= get that shit
        #   preHashValue= get that shit as well
        #   nonce = get that shit also
        # )
        return render(request,'main/item.html')

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
            verdicts=[]
            for verdictJson in caseJson['verdicts']:
                verdict=Verdict(text=verdictJson['text'],
                                case=verdictJson['case'],
                                verdict_type=verdictJson['verdict_type'])
                verdicts.append(verdict)
            StatementOfFacts=StatementOfFacts(case=caseJson['sof']['case'],id=caseJson['sof']['id'])

            if string(hashLib.calculateHash(case)) != string(caseJson['hashValue']):
                error="sha256 hash incorrect"
                return HttpResponse(json.dumps({'error':error}))
    

    def __checkNewCase(self,CaseObj,Verdicts,StatementOfFacts,Facts,Consenuses,Views):
        if CaseObj.hash!=hash.calculateHashNoId(CaseObj,Verdicts,StatementOfFacts,Facts,Consenuses,Views):
            return False
        return __checkCase(CaseObj.id-1)

    def __checkCase(self,case_id):
        cases=Case.objects.filter(id<=case_id)
        for case in cases:
            if case.id!=Case.objects.get(id=case_id-1).id:
                return False
            if case.hash != hash.calculateHash(case_id):
                return False
        return True




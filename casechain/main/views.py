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
        return render(request,'main/item.html',{'case': case})

    def addText(self,request):
        """
        Adds a Text to a case
        """
        pass


    def addCase(self,request):
        """
        Adds a new case to the chain
        """
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
    

    def __checkNewCase(self,CaseObj,Verdicts,StatementOfFacts,Facts,Consenus,Views):
        if CaseObj.hash!=hash.calculateHashNoId(CaseObj,Verdicts,StatementOfFacts,Facts,Consenus,Views):
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


from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from .models import Verdict,Case,Fact,View,Consenus,StatementOfFacts
from . import hash
from . import json_export
import hashlib
import json
from django.http.response import HttpResponse
import random
import string
from django.forms.models import model_to_dict
import requests
import socket

# Create your views here.

class CaseViews:

    def viewCases(self,request):
        cases = models.Case.objects.filter()
        isChainHealthy = False
        casesDict=[model_to_dict(x) for x in cases]
        for case,origCase in zip(casesDict,cases):
            case['date']=origCase.date
            case['status']=self.__checkCase(case['id'])
            case['hashValue']=case['hashValue'][:5]
            if self.__checkCase(case['id']):
                isChainHealthy = True
            else:
                isChainHealthy = False


        return render(request, 'main/index.html', {
            'cases': casesDict,
            'isChainHealthy': isChainHealthy
        })

    def viewCase(self,request,case_id=None):
        case = models.Case.objects.get(id=case_id)
        intVerdictList = models.Verdict.objects.filter(case_id=case_id,verdict_type='in')
        endVerdict=models.Verdict.objects.get(case_id=case_id,verdict_type="end")
        statementOfFactsId = models.StatementOfFacts.objects.get(case_id=case_id).id
        factList = models.Fact.objects.filter(statementOfFacts_id=statementOfFactsId)
        viewList = models.View.objects.filter(statementOfFacts_id=statementOfFactsId)
        consensusList = models.Consenus.objects.filter(statementOfFacts_id=statementOfFactsId)
        isChainHealthy = self.__checkCase(case.id)
        
        return render(request,'main/item.html',{
            'case': case,
            'intVerdicts': intVerdictList,
            'endVerdict':endVerdict,
            'consensusList': consensusList,
            'views': viewList,
            'facts': factList,
            'isChainHealthy': isChainHealthy
        })


    def getCaseForm(self,request):
        return render(request, 'main/new.html')

    def searchCase(self,request):
        queryString = request.GET.__getitem__('query')
        resultlist = []
        print(queryString)
        cases = models.Case.objects.all()
        casesDict = [model_to_dict(x) for x in cases]
        for case in casesDict:
            for key,value in case.items():
                if queryString in str(value):
                    resultlist.append(case)


        return render(request, 'main/searchResults.html', {
            'results': resultlist,
            'queryString': queryString
        })

    def addCase(self,request):
        if 'submit' in request.POST:
            endVerdict=Verdict(verdict_type="end")
            endVerdict.text=request.POST['verdictEnd']
            verdicts=[endVerdict]
            for i in range(1,int(request.POST['int_verdict_len'])):
                intVerdict=Verdict(verdict_type="in")
                intVerdict.text=request.POST['verdictInt'+str(i)]
                verdicts.append(intVerdict)

            viewPlaintiff=View(viewer='pl')
            viewPlaintiff.view=request.POST['viewPlaintiff']
            
            viewDefendant=View(viewer='df')
            viewDefendant.view=request.POST['viewDefendant']
            views=[viewPlaintiff,viewDefendant]

            facts=[]
            for i in range(1,int(request.POST['fact_len'])+1):
                fact=Fact()
                fact.fact=request.POST['fact'+str(i)]
                facts.append(fact)

            consenuses=[]
            for i in range(1,int(request.POST['consenus_len'])+1):
                consenus=Consenus()
                consenus.opinion=request.POST['consenus'+str(i)]
                consenuses.append(consenus)
            
            case = models.Case(
                 date=request.POST['date'],
                 court=request.POST['court'],
                 plaintiff=request.POST['plaintiff'],
                 defendant=request.POST['defendant'],
                 caseFile=request.POST['caseFile']
            )
            prevHashCase=Case.objects.filter().last()
            prevHash=""
            if prevHashCase==None:
                prevHash="0000000000000000000000000000000000000000000000000000000000000000"
            else:
                prevHash=prevHashCase.hashValue
            case.prevHashValue=prevHash
            case.nonce=''.join(random.choice(string.digits) for  _ in range(5))
            caseHash=hash.calculateHashNoId(case,verdicts,facts,consenuses,views)
            case.hashValue=caseHash
            case.save()
            for verdict in verdicts:
                verdict.case=case
                verdict.save()
            sof=StatementOfFacts(case=case)
            sof.save()
            for view in views:
                view.statementOfFacts=sof
                view.save()
            for fact in facts:
                fact.statementOfFacts=sof
                fact.save()
            for consenus in consenuses:
                consenus.statementOfFacts=sof
                consenus.save()
            
            jsonCase=json_export.exportCase(case.id)

            with open("clients.txt","r") as f:
                for client in f.readlines():
                    if not request.get_host() in socket.gethostname():
                        new_client=client
                        if '\n' in client:
                            new_client=client.replace('\r','')
                            new_client=client.replace('\n','')
                        print("send to: "+client)
                        r = requests.post("http://"+new_client+"/test/import", data={'case':json_export.exportCase(case.id)}) 
            
            return redirect('/test')

    def receiveCase(self,request):
        """
        Method to receive a case from other nodes
        """
        #if True:
        if 'case' in request.POST:
            caseJson=None
            #with open("export.json","r") as f:
            #    caseJson=json.loads(f.read())
            caseJson=json.loads(request.POST['case'])
            case=models.Case(date=caseJson['date'],
                             court=caseJson['court'],
                             plaintiff=caseJson['plaintiff'],
                             caseFile=caseJson['case_file'],
                             defendant=caseJson['dependent'],
                             hashValue=caseJson['hash'],
                             prevHashValue=caseJson['prevhash'],
                             nonce=caseJson['nonce']
                             )
            verdicts=[]
            for verdictJson in caseJson['verdicts']:
                verdict=Verdict(text=verdictJson['text'],
                                verdict_type=verdictJson['type'])
                verdicts.append(verdict)
            views=[]
            for viewJson in caseJson['views']:
                view=View(
                            viewer=viewJson['viewer'],
                            view=viewJson['view'],
                            )
                views.append(view)
            facts=[]
            for factJson in caseJson['facts']:
                fact=Fact(
                            fact=factJson['fact'],
                            )
                facts.append(fact)
                            
            statementOfFacts=StatementOfFacts()
            
            consenuses = []
            for consenusJson in caseJson['consensuses']:
                consenus=Consenus(
                            opinion=consenusJson['opinion'],
                        )
                consenuses.append(consenus)

            if str(hash.calculateHashNoId(case,verdicts,facts,consenuses,views)) != str(caseJson['hash']):
                error="sha256 hash incorrect"
                return HttpResponse(json.dumps({'error':error}))
            case.save()
            for verdict in verdicts:
                verdict.case=case
                verdict.save()
            statementOfFacts.case=case
            statementOfFacts.save()
            for fact in facts:
                fact.statementOfFacts=statementOfFacts
                fact.save()
            for view in views:
                view.statementOfFacts=statementOfFacts
                view.save()
            for consenus in consenuses:
                consenus.statementOfFacts=statementOfFacts
                consenus.save()

            return redirect ("/test")

    def __checkNewCase(self,CaseObj,Verdicts,StatementOfFacts,Facts,Consenuses,Views):
        if CaseObj.hash!=hash.calculateHashNoId(CaseObj,Verdicts,StatementOfFacts,Facts,Consenuses,Views):
            return False
        return __checkCase(CaseObj.id-1)

    def __checkCase(self,case_id):
        caseObj=Case.objects.get(id=case_id)
        if caseObj.hashValue != hash.calculateHash(case_id):
            return False
        cases=list(Case.objects.filter(id__lt=case_id))
        for case in cases:

            print(case.id)
            if case.hashValue != hash.calculateHash(case.id):
                print(case.hashValue)
                print(hash.calculateHash(case_id))
                return False
        return True




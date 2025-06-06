from datetime import datetime

from app.api.error.exceptions import NoQuestionnaire, SameIp
from app.extensions import db

from app.models.questionnaire import Questionnaire
from app.models.resolution import Resolution
from app.utils.dataCalculate import DataCalculate


class Complete(db.Document):

    completeTime = db.DateTimeField(default=datetime.utcnow)

    completeData = db.ListField()

    ipCondition = db.DictField()

    targetQuestionnaireId = db.IntField()

    def createCompleteData(self, data, qid, ip=None):
        q = Questionnaire.objects.filter(questionnaireId=qid).first()
        if not q:
            raise NoQuestionnaire
        if q.ipControl and ip in q.questionnaireIP:
            raise SameIp
        if ip is not None:
            q.questionnaireIP.append(ip)
        completes = data['completeData']
        self.completeData = completes
        self.makeResolution(completes)
        self.ipCondition = DataCalculate.getPlace(ip)
        self.targetQuestionnaireId = qid
        self.save()

    @staticmethod
    def makeResolution(completes):
        for c in completes:
            Resolution(
                targetProblemId=c['targetProblemId'],
                type=c['type'],
                resolution=c['resolution']
            ).save()

    @staticmethod
    def addCompleteNumber(qid, completes):
        from app.models.problem import Problem
        ps = Problem.objects.filter(
            targetQuestionnaireId=qid).order_by('problemId')
        for index, p in enumerate(ps):
            p.addCompletes(completes[index])
            p.save()

    @staticmethod
    def getCompleteAmount(qid):
        cs = Complete.objects.filter(targetQuestionnaireId=qid)
        return len(cs)

    def getIpProvince(self):
        return self.ipCondition['pro'][:-1]

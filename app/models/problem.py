from app.api.error.exceptions import NoQuestionnaire, NoProblem
from app.extensions import db
from app.models.questionnaire import Questionnaire
from app.utils.timeHelper.timeHelper import getUniqueId


class Problem(db.Document):

    title = db.StringField()

    type = db.StringField()

    options = db.ListField()

    isRequire = db.BooleanField(default=False)

    problemId = db.IntField()

    targetQuestionnaireId = db.IntField()

    ownerId = db.StringField()

    def appendOneProblem(self, ownerId, form):
        q = Questionnaire.objects.filter(
            ownerId=ownerId, questionnaireId=form.targetQuestionnaireId.data).first()
        if not q:
            raise NoQuestionnaire
        self.targetQuestionnaireId = form.targetQuestionnaireId.data
        self.title = form.title.data
        self.type = form.type.data
        self.ownerId = ownerId
        self.problemId = getUniqueId()
        self.save()
        return self.problemId

    def getProblemJson(self):
        payLoad = {
            "title": self.title,
            "type": self.type,
            "options": self.options,
            "isRequire": self.isRequire,
            "problemId": self.problemId,
            "targetQuestionnaireId": self.targetQuestionnaireId,
        }
        return payLoad

    def getResolution(self):
        from app.models.resolution import Resolution
        optionRes = []
        res = Resolution.getResolutionByPid(self.problemId)

        if self.type == "BLANK_FILL":
            for r in res:
                if len(r.resolution) is 0:
                    continue
                optionRes.append(r.resolution[0])

        if self.type == "SINGLE_SELECT" or self.type == "DROP_DOWN":
            optionRes = self.options
            for r in res:
                if len(r.resolution) is 0:
                    continue
                pos = int(r.resolution[0])
                if 'resolution' not in optionRes[pos]:
                    optionRes[pos]['resolution'] = 1
                else:
                    optionRes[pos]['resolution'] += 1

        if self.type == "MULTIPLY_SELECT":
            optionRes = self.options
            for r in res:
                if len(r.resolution) is 0:
                    continue
                for pos in r.resolution:
                    pos = int(pos)
                    if 'resolution' not in optionRes[pos]:
                        optionRes[pos]['resolution'] = 1
                    else:
                        optionRes[pos]['resolution'] += 1

        if self.type == "SCORE":
            optionRes = []
            for i in range(1, 6):
                optionRes.append({
                    "title": i,
                    "resolution": 0
                })
            for r in res:
                if len(r.resolution) is 0:
                    continue
                score = r.resolution[0]
                optionRes[score]["resolution"] += 1

        return {
            "title": self.title,
            "resolution": optionRes,
            "type": self.type,
            "problemId": self.problemId
        }

    @staticmethod
    def deleteOneProblem(ownerId, problemId):
        p = Problem.objects.filter(
            ownerId=ownerId, problemId=problemId).first()
        if not p:
            raise NoProblem
        p.delete()

    @staticmethod
    def deleteProblems(ownerId, questionnaireId):
        ps = Problem.objects.filter(
            ownerId=ownerId, targetQuestionnaireId=questionnaireId)
        ps.delete()

    @staticmethod
    def editOneProblem(ownerId, problemId, form):
        p = Problem.objects.filter(
            ownerId=ownerId, problemId=problemId).first()
        if not p:
            raise NoProblem
        p.title = form.title.data
        p.options = form.jsonData['options']
        p.isRequire = form.isRequire.data
        p.type = form.type.data
        p.save()

    @staticmethod
    def getProblems(qid):
        problems = []
        ps = Problem.objects.filter(
            targetQuestionnaireId=qid).order_by('problemId')
        for p in ps:
            problems.append(p.getProblemJson())
        return problems

    @staticmethod
    def createByTemplates(title, ptype, opt, pid, ownerId, tqid):
        Problem(
            title=title,
            type=ptype,
            options=opt,
            problemId=pid,
            ownerId=ownerId,
            targetQuestionnaireId=tqid
        ).save()

    @staticmethod
    def getOneProblemByPid(pid, oid):
        p = Problem.objects.filter(problemId=pid, ownerId=oid).first()
        if not p:
            raise NoProblem
        return p.getProblemJson()

from app.extensions import db


class Resolution(db.Document):

    targetProblemId = db.IntField()

    type = db.StringField()

    resolution = db.ListField()

    @staticmethod
    def getResolutionByPid(pid):
        resolution = Resolution.objects.filter(targetProblemId=pid)
        return resolution

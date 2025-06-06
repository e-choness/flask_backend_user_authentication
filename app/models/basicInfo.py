from app.extensions import db


class BasicInfo(db.Document):
    spidersTagLinks = db.ListField(default=["init"])

    def getNewestLink(self, index):
        return self.spidersTagLinks[index]

    def renewNewestLink(self, index, newLink):
        self.spidersTagLinks[index] = newLink
        self.save()

    @staticmethod
    def initBasicInfo():
        basicinfo = BasicInfo()
        basicinfo.save()

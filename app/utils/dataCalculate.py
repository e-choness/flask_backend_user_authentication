import requests
from flask import current_app


class DataCalculate:
    typeToDoCount = ["SINGLE_SELECT", "MULTIPLY_SELECT", "DROP_DOWN"]

    @staticmethod
    def getPlace(ip):
        url = 'http://whois.pconline.com.cn/ipJson.jsp?ip={}&json=true'.format(
            ip)
        try:
            res = requests.get(url=url)
        except Exception as e:
            current_app.logger.error(e)
            return {'code': 0}
        data = res.json()
        data['code'] = 1
        return data

    @staticmethod
    def getProvinceData(qid):
        from app.models.complete import Complete
        total = {}
        completes = Complete.objects.filter(targetQuestionnaireId=qid)
        for c in completes:
            province = c.getIpProvince()
            if province in total:
                total[province] += 1
            else:
                total[province] = 1
        return total

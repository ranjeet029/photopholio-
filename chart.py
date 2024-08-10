from user import user_operation
from matplotlib import pyplot as plt

class chart_op:
    def chart_show(self):
        ob = user_operation()
        row=ob.category_chart()
        category=[]
        num=[]
        for r in row:
             category.append(r[0])
             num.append(r[1])
        
        fig = plt.figure(figsize =(10, 7))
        
        plt.pie(num,labels=category,autopct=lambda p:'{:.0f}%'. format(p),shadow=True)

        plt.legend()
        fig.savefig('static/chart/category_chart.png')   # save as image
        return

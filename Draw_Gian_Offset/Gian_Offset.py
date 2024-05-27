from matplotlib import pyplot as plt
import numpy as np
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

class Gainoffsetdraw:
    def __init__(self,Gc,Gl,Gc_t,Gl_t):
        self.Gc=Gc
        self.Gl=Gl
        self.Gc_t=Gc_t
        self.Gl_t=Gl_t

    def display(self):            
        x = np.arange(0,10,0.1)
        yc = self.Gc_t-x*self.Gc
        yb = self.Gl_t-x*self.Gl

        ax = plt.subplot(111)

        plt.plot(x,yc,c='r',lw=2, label=f'copper   :y≥{self.Gc_t}-{self.Gc}*x')
        plt.plot(x,yb,c='b',lw=2, label=f'laminate:y≤{self.Gl_t}-{self.Gl}*x')
        plt.ylim(-250,150) #设置y轴的取值范围
        # 0:‘best'、1:‘upper right'、2:‘upper left'、3:‘lower left'
        # 4:‘lower right'、5:‘right'、6:‘center left'、7:‘center right'
        # 8:‘lower center'、9:‘upper center'10:‘center'
        plt.legend(loc=9) #放置x、y轴的标签

        #计算两直线的交点
        jd_x=round((yc[0]-yb[0])/(self.Gc-self.Gl),2)
        jd_y=round(self.Gc_t-jd_x*self.Gc,0)

        #将交点位置添加到图表
        plt.axvline(x=jd_x,ymin=0,ymax=0.8,c='g',ls='-.')
        plt.axhline(y=jd_y,xmin=0,xmax=1,c='g',ls='-.')

        #将交点坐标在图像上显示出来
        gain_text='Gain_min='+str(jd_x)
        offset_text='Offset_max='+str(jd_y)
        plt.text(jd_x-1,ax.get_ylim()[0]-20, gain_text, ha='left', va='bottom') 
        plt.text(ax.get_xlim()[1]-3, jd_y-30, offset_text, ha='left', va='bottom') 

        #将铜面和基材基础灰度值放置到图表上
        gray_text=f'         Gray value\n             origin  target \n laminate: {self.Gl}    {self.Gl_t}\n copper   : {self.Gc}    {self.Gc_t}'
        plt.text(ax.get_xlim()[1]-3,ax.get_ylim()[1]-70, gray_text, ha='left', va='bottom') 

        #设置X轴、Y轴的标签、图表的名称
        plt.xlabel("Gain",verticalalignment='bottom')
        plt.ylabel("Offset")
        plt.title('Gain-Offset')

        #设置坐标轴的位置
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['left'].set_position(('data', 0))
        plt.show()
        return jd_x,jd_y

class Gain_Offset:
        def __init__(self):
        # 从文件中加载UI定义
            self.ui = QUiLoader().load('./Draw_Gian_Offset/Gain_Offset.ui')

            self.ui.drawbutoon.clicked.connect(self.Draw)
            self.ui.clearbutoon.clicked.connect(self.cleartextBrowser)

        def Draw(self):
             Gc=self.ui.GcEdit.text()
             Gl=self.ui.GlEdit.text()
             Gc_t=self.ui.Gc_tEdit.text()
             Gl_t=self.ui.Gl_tEdit.text()
             if Gc=='':
                Gc=60
             if Gl=='':
                Gl=40
             if Gc_t=='':
                Gc_t=80
             if Gl_t=='':
                Gl_t=30
             Gc=int(Gc)
             Gl=int(Gl)
             Gc_t=int(Gc_t)
             Gl_t=int(Gl_t)

             draw=Gainoffsetdraw(Gc,Gl,Gc_t,Gl_t)      
             Gain,Offset=draw.display()
             info=f'基材原始灰度值：{Gl}，基材目标灰度值：{Gl_t}\n铜面原始灰度值：{Gc}，铜面目标灰度值：{Gc_t}\n需设置的相机最小增益值为：{Gain}，偏移值为：{Offset}\n'

             self.ui.textBrowser.append(str(info))
             self.ui.textBrowser.ensureCursorVisible()  

        def cleartextBrowser(self):
            self.ui.textBrowser.clear()


if __name__ == "__main__":
    app = QApplication([])
    Gain_Offset = Gain_Offset()
    Gain_Offset.ui.show()
    app.exec_()

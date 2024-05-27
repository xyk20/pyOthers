from matplotlib import pyplot as plt
import numpy as np
import cv2
import time

def CvImread(filePath):
    # 核心就是下面这句，一般直接用这句就行，直接把图片转为mat数据
    cvImg = cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cvImg

def display(Gc,Gl):
    Gc_t=80
    Gl_t=30

    x = np.arange(0,10,0.1)
    yc = Gc_t-x*Gc
    yb = Gl_t-x*Gl

    ax = plt.subplot(111)

    plt.plot(x,yc,c='r',lw=2, label=f'copper   :y≥{Gc_t}-{Gc}*x')
    plt.plot(x,yb,c='b',lw=2, label=f'laminate:y≤{Gl_t}-{Gl}*x')
    plt.ylim(-250,150) #设置y轴的取值范围
    # 0:‘best'、1:‘upper right'、2:‘upper left'、3:‘lower left'
    # 4:‘lower right'、5:‘right'、6:‘center left'、7:‘center right'
    # 8:‘lower center'、9:‘upper center'10:‘center'
    plt.legend(loc=9) #放置x、y轴的标签

    #计算两直线的交点
    jd_x=round((yc[0]-yb[0])/(Gc-Gl),2)
    jd_y=round(Gc_t-jd_x*Gc,0)

    #将交点位置添加到图表
    plt.axvline(x=jd_x,ymin=0,ymax=0.8,c='g',ls='-.')
    plt.axhline(y=jd_y,xmin=0,xmax=1,c='g',ls='-.')

    #将交点坐标在图像上显示出来
    gain_text='Gain_min='+str(jd_x)
    offset_text='Offset_max='+str(jd_y)
    plt.text(jd_x-1,ax.get_ylim()[0]-20, gain_text, ha='left', va='bottom') 
    plt.text(ax.get_xlim()[1]-3, jd_y-30, offset_text, ha='left', va='bottom') 

    #将铜面和基材基础灰度值放置到图表上
    gray_text=f'         Gray value\n             origin  target \n laminate: {Gl}    {Gl_t}\n copper   : {Gc}    {Gc_t}'
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
    result_path='./relsut.jpg'
    plt.savefig(result_path)
    plt.close()
    return result_path

while True:
    Gc=90
    Gl=40
    for i in range(50,Gc,1):
        Gc=Gc-1
        result_path=display(Gc,Gl)
        img=CvImread(result_path)
        time.sleep(0.5)
        cv2.imshow("Copper origin gray value 90 to 50,Gain is increasing!",img)
        k=cv2.waitKey(1)
        # 27为 Esc 按键的ASCII码
        if k==27:
            cv2.destroyAllWindows()
            break
        # 32为 空格 按键的ASCII码
        if k==32:
            while True:
                h=cv2.waitKey(1)
                # 13为 Enter 按键的ASCII码
                if h==13:
                    break
    if k==27:
        break

print('程序结束！')

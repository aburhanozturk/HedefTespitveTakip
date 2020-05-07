#Hata 73! .......... Servo dönme zorlanması (Servo son konumda)

from time import sleep
from threading import Thread
import numpy as np
import cv2
import curses
import os
import time

global nod # Ekranda hedef yokken döndürülen değer. if blokları kontrolü için gerekli.
nod = 0 # nod = 0 ise ekranda hedef yok. nod = 1 ise ekranda hedef var.

lowerBound = np.array([0, 149, 120])
upperBound = np.array([83, 255, 255])
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))


def goruntu():
    global nod
    global Mx
    global My
    cap = cv2.VideoCapture(0)
    
    while (cap.isOpened()):
        ret, img = cap.read()
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, lowerBound, upperBound)
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
        maskFinal = maskClose
        _, conts, _ = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #  _ ekle üste
        if ret == True:
            cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
            if len(conts) == 0:
                #print("No Output Data")
                nod = 0
                pass
            for i in range(len(conts)):
                x, y, w, h = cv2.boundingRect(conts[i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                Mx = (x + w / 2)
                My = (y + h / 2)
                cv2.circle(img, (int(Mx), int(My)), 2, (0, 255, 255), -1)
                nod = 1
                time.sleep(0.05)
                print("X" + str(Mx) + " -- Y" + str(My))
            # frame = cv2.flip(img,1)
            cv2.imshow('Son_Hal', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cap.release()
    cv2.destroyAllWindows()


def tekrarla():
   
    # activating servo blaster (servod must be in the same folder as this script!)
    os.system('sudo ./servod')
  
    # setting start up servo positions
    # positions range from (50-240)
    servo1 = 60  # servo1 ilk konum
    servo2 = 60  # servo2 ilk konum
    Ax = 0       # Mx ile aynı değeri takip ediyor.
    Ay = 0       # My ile aynı değeri takip ediyor.
    z = 0        # z değeri nod ile zıt değeri takip ediyor. nod = 0 ise z = 1 olur.
                 #* Ax,Ay ve z değerleri sorun çözümünde kullanıldı ancak şuan için işlevleri var mı bilmiyorum. 
                 #* Kodu inceleyip kodun çalışmasında hata vermeyecekse çıkartılabilirler.
    
                 # servo yönleri kalibre edilmemiştir. Şuan bu sistemde:
                 # X düzleminde (servo1) 60 - 102 sol --- 102 - 108 orta --- 108 - 250 sağ
                 # Y düzleminde (servo2) 60 - 108 ön  --- 108 - 114 alt  --- 114 - 250 arka
    try:
        
        while True:
            print("Tarama döngüsü.!")
            print("z status: ",z)
            # Tarama
            # Eğer nod == 0 yani hedef ekranda yok ise bu if bloğu devreye girer.
            if (nod == 0 or z == 1):
                # servo2 konumunu tarama için 60 a (ilk değer) alır.
                os.system("echo 1=%s > /dev/servoblaster" % servo2)
                time.sleep(0.005)
                #*0 Döngüsü
                while True:
                    # Hedef merkezde mi kontrol edilir.
                    if (Ax > 280 and Ax < 360 and Ay > 200 and Ay < 280):
                        print("Hedef Merkezde! 0")
                        pass
                        break
                    # Servo1 ilk konum ile harekete geçer. (En sol)
                    if (servo1 == 60):
                        # servo1 konumunu arttırarak kamerayı sağa doğru döndürmeye başlar.
                        while True:
                            servo1 = servo1 + 2
                            os.system("echo 0=%s > /dev/servoblaster" % servo1)
                            time.sleep(0.15)
                            # Eğer hedef kamera ile tespit edilirse
                            # servo konumları kx ve ky ye kaydedilir ve tarama döngüsünden çıkılır.
                            # hedef görüldüğü için (nod == 1) z = 0 olur. (nod u tersten takip eder)
                            if (nod == 1):
                                kx = servo1  # tarama sonucu aktarılan servo1 konum
                                ky = servo2  # tarama sonucu aktarılan servo2 konum
                                z = 0
                                pass
                                break
                            # Hedef bulunamaması durumunda ve sağ pozisyonda servo son
                            # konuma ulaşması (en sağ) durumunda döngüyü kırar ve bir sonraki komut satırına geçer.
                            if (servo1 == 240):
                                pass
                                break
                    # servo1 in en sağda olması durumunda        
                    elif (servo1 == 240):
                        # servo1 konumunu azaltarak kamerayı sola doğru döndürmeye başlar.
                        while True:
                            servo1 = servo1 - 2
                            os.system("echo 0=%s > /dev/servoblaster" % servo1)
                            time.sleep(0.15)
                            
                            # Eğer hedef kamera ile tespit edilirse
                            # servo konumları kx ve ky ye kaydedilir ve tarama döngüsünden çıkılır.
                            # hedef görüldüğü için (nod == 1) z = 0 olur. (nod u tersten takip eder)
                            if (nod == 1):
                                kx = servo1  # tarama sonucu aktarılan servo1 konum
                                ky = servo2  # tarama sonucu aktarılan servo2 konum
                                z = 0
                                pass
                                break
                            # Hedef bulunamaması durumunda ve sol pozisyonda servo son
                            # konuma ulaşması (en sol) durumunda döngüyü kırar
                            # ve bir sonraki komut satırlarına geçerek taramaya devam eder.
                            # (while döngüsü ile sağlanır)
                            if (servo1 == 60):
                                pass
                                break
                    # Hedef bulunma durumunu kontrol eder. Bulunması durumunda tarama döngüsünden çıkar.
                    # servo konumlarını kx ve ky ye kaydederek z yi 0 a çeker.
                    if (nod == 1):
                        print("Hedef bulundu.!")
                        kx = servo1  # tarama sonucu aktarılan servo1 konum
                        ky = servo2  # tarama sonucu aktarılan servo2 konum
                        z = 0
                        pass
                        break
                #*0 Döngüsü sonu
                kx = servo1  # tarama sonucu aktarılan servo1 konum
                ky = servo2  # tarama sonucu aktarılan servo2 konum

            # Hedef Takip kısımı (nod == 1 --- Hedef tespit edildi)
            elif (nod == 1):
                z = 0 # Kontrol amaçlı. nod 1 olduğu durumda z her zaman 0 dır.
                
                # Ana döngü hedef kaybedilene kadar çalışmaya devam eder. Takip için.
                #*1 Döngüsü
                while True:
                    # Hedefin ekranda olup olmadığını kontrol eder.
                    if (nod == 0):
                        print("Hedef Kaybedildi! 1")
                        z = 1
                        Ax = int(Mx)
                        Ay = int(My)
                        pass
                        break
                
                    # Hedefin merkezde olup olmadığı kontrol edilir.
                    if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                        Ax = Mx
                        Ay = My
                        while True:
                            print("Hedef Merkezde! 1 ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                            # Merkezden çıkarsa
                            if (Mx < 280 or Mx > 360 or My < 200 or My > 280):
                                print("Hedef Merkezden Çıktı.! M")
                                pass
                                break
                            
                        #pass
                        #break #(Kullanımı hata verebilir veya programı sonlandırabilir)
                    
                    # Tarama verilerinden alınan değerlerle servolar hedefin tespit edildiği konuma gider.
                    # (Güvenlik önlemi - son konum)
                    os.system("echo 0=%s > /dev/servoblaster" % kx)
                    time.sleep(0.15)
                    os.system("echo 1=%s > /dev/servoblaster" % ky)
                    time.sleep(0.15)

                    # 1.Bölge ---------- (Hedef ekranın sol ve üst bölgesinde ise)
                    if (0 <= Mx and Mx < 320 and 0 <= My and My < 240):
                        # Hedef merkezde mi kontrol edilir.
                        if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                            Fx = kx # Servo1 konum değerini alır
                            Fy = ky # Servo2 konum değerini alır
                            # Fx ve Fy otonom uçuş için hedefin yönünü ve konumunu bildirmede
                            # kullanılacak olan değişken değerlerdir.
                            Ax = Mx
                            Ay = My
                            while True:
                                print("Hedef Merkezde! 1B ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                                # Hedef merkezden çıkması durumunda
                                if (Mx < 280 or Mx > 360 or My < 200 or My > 280):
                                    print("Hedef Merkezden Çıktı.! M1")
                                    pass
                                    break
                            pass
                            continue
                        while True:
                            # Yön servosu merkezde mi? (servo1) Merkezdeyse döngüyü kır.
                            if ( 280 < Mx and Mx < 360):
                                Fx = kx
                                print("Yön servosu merkezde.! B1 --- Fx: {}".format(Fx))
                                pass
                                break
                            # Yön servosunun konumunu değiştir.
                            # (1. bölgede olduğu için merkeze yaklaştırmak amacıyla kx azaltılır)
                            if (kx > 58 and kx < 242 ):
                                kx = kx - 2
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                
                                # hedef kamerada mı kontrol edilir..
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                # Servo en son konumunda ve daha fazla dönemez.
                                # Koruma amaçlı servoyu ters yönde döndürür ve döngüyü kırar.
                                print("Hata 73! B1X")
                                kx = kx + 4
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                break

                        while True:
                            # Açı servosu merkezde mi? (servo2) Merkezdeyse döngüyü kır.
                            if ( 200 < My and My < 280):
                                pass
                                break
                            # Açı servosunun konumunu değiştir.
                            # (1. bölgede olduğu için merkeze yaklaştırmak amacıyla ky azaltılır)
                            if (ky > 58 and ky < 242 ):
                                ky = ky - 2
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                
                                # hedef kamerada mı kontrol edilir.
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                # Servo en son konumunda ve daha fazla dönemez.
                                # Koruma amaçlı servoyu ters yönde döndürür ve döngüyü kırar.
                                print("Hata 73! B1Y")
                                ky = ky + 4
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                break

                    # 2.Bölge  ---------- (Hedef ekranın sağ ve üst bölgesinde ise)
                    if (320 <= Mx and Mx <= 640 and 0 <= My and My < 240):
                        if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                            Fx = kx
                            Fy = ky
                            Ax = Mx
                            Ay = My
                            while True:
                                print("Hedef Merkezde! 2B ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                                if (Mx < 310 or Mx > 330 or My < 230 or My > 250):
                                    print("Hedef Merkezden Çıktı.! M2")
                                    pass
                                    break
                            pass
                            continue
                        while True:
                            if (280 < Mx and Mx < 360):
                                Fx = kx
                                print("Yön servosu merkezde.! B2 --- Fx: {}".format(Fx))
                                pass
                                break
                            if (kx > 58 and kx < 242):
                                kx = kx + 2
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B2X")
                                kx = kx - 4
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                break
                            
                        while True:
                            if (200 < My and My < 280):
                                pass
                                break
                            if (ky > 58 and ky < 242):
                                ky = ky - 2
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B2Y")
                                ky = ky + 4
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                break

                    # 3.Bölge  ---------- (Hedef ekranın sol ve alt bölgesinde ise)
                    if (0 <= Mx and Mx < 320 and 240 <= My and My <= 480):
                        if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                            
                            Fx = kx
                            Fy = ky
                            Ax = Mx
                            Ay = My
                            while True:
                                print("Hedef Merkezde! 3B ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                                if (Mx < 310 or Mx > 330 or My < 230 or My > 250):
                                    print("Hedef Merkezden Çıktı.! M3")
                                    pass
                                    break
                            pass
                            continue
                        while True:
                            if (280 < Mx and Mx < 360):
                                Fx = kx
                                print("Yön servosu merkezde.! B3 --- Fx: {}".format(Fx))
                                pass
                                break
                            if (kx > 58 and kx < 242):
                                kx = kx - 2
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B3X")
                                kx = kx + 4
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                break


                        while True:
                            if (200 < My and My < 280):
                                pass
                                break
                            if (ky > 58 and ky < 242):
                                ky = ky + 2
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B3Y")
                                ky = ky - 4
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                break

                    # 4.Bölge  ---------- (Hedef ekranın sağ ve alt bölgesinde ise)
                    if (320 <= Mx and Mx < 640 and 240 <= My and My < 480):
                        if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                            Fx = kx
                            Fy = ky
                            Ax = Mx
                            Ay = My
                            while True:
                                print("Hedef Merkezde! 4B ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                                if (Mx < 310 or Mx > 330 or My < 230 or My > 250):
                                    print("Hedef Merkezden Çıktı.! M4")
                                    pass
                                    break
                            pass
                            continue
                        while True:
                            if (280 < Mx and Mx < 360):
                                Fx = kx
                                print("Yön servosu merkezde.! B4 --- Fx: {}".format(Fx))
                                pass
                                break
                            if (kx > 58 and kx < 242):
                                kx = kx + 2
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B4X")
                                kx = kx - 4
                                os.system("echo 0=%s > /dev/servoblaster" % kx)
                                time.sleep(0.30)
                                break

                        while True:
                            if (200 < My and My < 280):
                                pass
                                break
                            if (ky > 58 and ky < 242):
                                ky = ky + 2
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                
                                
                                if (nod == 0):
                                    print("Hedef Kaybedildi!")
                                    z = 1
                                    pass
                                    break
                            else:
                                print("Hata 73! B4Y")
                                ky = ky - 4
                                os.system("echo 1=%s > /dev/servoblaster" % ky)
                                time.sleep(0.30)
                                break
                    # Hedef merkezde mi kontrol edilir.
                    if (Mx > 280 and Mx < 360 and My > 200 and My < 280):
                        Ax = Mx
                        Ay = My
                        Fx = kx
                        Fy = ky
                        while True:
                            print("Hedef Merkezde! 2 ------ Ax: {} Ay: {} Mx: {} My: {} Fx: {} Fy: {}".format(Ax, Ay, Mx, My, Fx, Fy))
                            if (Mx < 380 or Mx > 360 or My < 200 or My > 280):
                                print("Hedef Merkezden Çıktı.! MM")
                                pass
                                break
                        pass
                        continue
                # Hedef kaybedildiyse tarama döngüsüne burada tekrar girer
                if (nod == 0):
                    print("Hedef Kaybedildi! 2S")
                    os.system("echo 1=%s > /dev/servoblaster" % servo2)
                    time.sleep(0.005)
                    while True:
                        if (Ax > 280 and Ax < 360 and Ay > 200 and Ay < 280):
                            print("Hedef Merkezde! 0")
                            pass
                            break
                        if (servo1 == 60 or z == 1):
                            while True:
                                servo1 = servo1 + 2
                                os.system("echo 0=%s > /dev/servoblaster" % servo1)
                                time.sleep(0.15)
                                if (nod == 1):
                                    kx = servo1  # tarama sonucu aktarılan servo1 konum
                                    ky = servo2  # tarama sonucu aktarılan servo2 konum
                                    z = 0
                                    pass
                                    break
                                if (servo1 == 240):
                                    pass
                                    break
                        if (servo1 == 240):
                            while True:
                                servo1 = servo1 - 2
                                os.system("echo 0=%s > /dev/servoblaster" % servo1)
                                time.sleep(0.15)
                                if (nod == 1):
                                    kx = servo1  # tarama sonucu aktarılan servo1 konum
                                    ky = servo2  # tarama sonucu aktarılan servo2 konum
                                    z = 0
                                    pass
                                    break
                                if (servo1 == 60):
                                    pass
                                    break
                        if (nod == 1):
                            print("Hedef bulundu.! 2SS")
                            kx = servo1  # tarama sonucu aktarılan servo1 konum
                            ky = servo2  # tarama sonucu aktarılan servo2 konum
                            z = 0
                            pass
                            break
                    if (nod == 1):
                        kx = servo1  # tarama sonucu aktarılan servo1 konum
                        ky = servo2  # tarama sonucu aktarılan servo2 konum
                        pass
                        continue
                    
                #*1
                    
    # Kullandığım kaynaktaki kodlar
    finally:
        
        # shut down cleanly
        #curses.nocbreak();
        #screen.keypad(0);
        #curses.echo()
        #curses.endwin()
        pass

# Thread komutu (Görüntü verileri ile servo kontrolün birlikte çalışmasını sağlar)
if __name__ == '__main__':
    tekr = Thread(target=tekrarla)
    isleme = Thread(target=goruntu)
    

    tekr.start()
    isleme.start()

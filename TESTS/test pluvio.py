from machine import ADC, Pin
from time import sleep

val_Godet = ADC(Pin(26))
Godet = 0
def test_godet():
    global Godet
    
    if val_Godet == 0:
        
        Godet += 1
        
        if Godet == 1:
            print("1")
        if Godet == 2:
            print("2")
        if Godet == 3:
            print("3")
        if Godet == 4:
            print("4")
        if Godet == 5:
            print("5")
            
        sleep(0.5)
test_godet()

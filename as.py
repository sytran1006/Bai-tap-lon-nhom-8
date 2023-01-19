
# Modules
import RPi.GPIO as GPIO
import time
from threading import Thread

import glob

# Define GPIO to LCD mapping
LCD_RS = 5
LCD_E = 6
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 16
LCD_D7 = 19
GPIO_Button_1 = 20
GPIO_Button_2 = 26
GPIO_Button_3 = 21
GPIO_Button_Cancel = 17
GPIO_Pump_Motor = 18
GPIO_Heater = 27

LCD_WIDTH = 16  
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  
LCD_LINE_2 = 0xC0 


E_PULSE = 0.0005
E_DELAY = 0.0005

Coffee_Price = 10000  
Coffee_Milk_Price = 15000
Milk_Price = 10000
Product_Price = 0  

Product_List = ["COFFEE", "COFFEE_MILK", "MILK"]
Product_Index = 0
Product_Choose = "" 
Money_Input = 0 
Remaining_Milk = 1  
Remaining_Coffee = 3
Remaining_Water = 3

Is_People_Input_Money = False  
Is_People_Choose_Product = False  

A_Cup_Of_Cafe_Formula = {"Cafe": 0.2, "Milk": 0, "Water": 0.2}  
A_Cup_Of_Cafe_Milk_Formula = {"Cafe": 0.2, "Milk": 0.2, "Water": 0.2} 
A_Cup_Of_Milk_Formula = {"Cafe": 0, "Milk": 0.5, "Water": 0.2}  


def check_for_coffee(): 
    return A_Cup_Of_Cafe_Formula["Cafe"] < Remaining_Coffee and A_Cup_Of_Cafe_Formula["Milk"] < Remaining_Milk and \
           A_Cup_Of_Cafe_Formula["Water"] < Remaining_Water


def check_for_coffee_milk():  
    return A_Cup_Of_Cafe_Milk_Formula["Cafe"] < Remaining_Coffee and A_Cup_Of_Cafe_Milk_Formula[
        "Milk"] < Remaining_Milk and A_Cup_Of_Cafe_Milk_Formula["Water"] < Remaining_Water


def check_for_milk():  
    return A_Cup_Of_Milk_Formula["Cafe"] < Remaining_Coffee and A_Cup_Of_Milk_Formula["Milk"] < Remaining_Milk and \
           A_Cup_Of_Milk_Formula["Water"] < Remaining_Water


def enable_pump_motor_and_heater():
    GPIO.output(GPIO_Pump_Motor, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GPIO_Pump_Motor, GPIO.LOW)
    GPIO.output(GPIO_Heater, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GPIO_Heater, GPIO.LOW)
    return


def product_preparation(product_choose):
    enable_pump_motor_and_heater()
    pwm1 = GPIO.PWM(22, 100)  
    pwm1.start(0)
    pwm2 = GPIO.PWM(23, 100) 
    pwm2.start(0)
    pwm3 = GPIO.PWM(24, 100)  
    pwm3.start(0)

    if product_choose == "COFFEE":
        pwm1.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Formula["Cafe"] / 2 * 5 * 2)
        pwm1.ChangeDutyCycle(15)
        pwm2.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Formula["Milk"] / 2 * 5 * 2)
        pwm2.ChangeDutyCycle(15)
        pwm3.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Formula["Water"] / 2 * 5 * 2)
        pwm3.ChangeDutyCycle(15)

        time.sleep(2)
    if product_choose == "COFFEE_MILK":
        pwm1.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Milk_Formula["Cafe"] / 2 * 5 * 2)
        pwm1.ChangeDutyCycle(15)
        pwm2.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Milk_Formula["Milk"] / 2 * 5 * 2)
        pwm2.ChangeDutyCycle(15)
        pwm3.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Cafe_Milk_Formula["Water"] / 2 * 5 * 2)
        pwm3.ChangeDutyCycle(15)

        time.sleep(2)
    if product_choose == "MILK":
        pwm1.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Milk_Formula["Cafe"] / 2 * 5 * 2)
        pwm1.ChangeDutyCycle(15)
        pwm2.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Milk_Formula["Milk"] / 2 * 5 * 2)
        pwm2.ChangeDutyCycle(15)
        pwm3.ChangeDutyCycle(20)
        time.sleep(A_Cup_Of_Milk_Formula["Water"] / 2 * 5 * 2)
        pwm3.ChangeDutyCycle(15)

        time.sleep(2)

    return


def program():
   
    global Is_People_Add_Milk_To_Coffee
    global Is_People_Choose_Product
    global Is_People_Input_Money
    global Money_Input
    global Product_Choose
    global Product_Price
    global Coffee_Price
    global Coffee_Milk_Price
    global Milk_Price
    global Number_Product_Choose
    global Product_Index
    global Product_List

    lcd_string("SELECT ITEM", LCD_LINE_1)
    if not Is_People_Choose_Product:
        lcd_string("ITEM: " + Product_List[Product_Index], LCD_LINE_2)
        if GPIO.input(GPIO_Button_1):
            if Product_Index > 0:
                Product_Index -= 1
                time.sleep(0.5)
        if GPIO.input(GPIO_Button_2):
            if Product_Index < 2:
                Product_Index += 1
                time.sleep(0.5)
        if GPIO.input(GPIO_Button_3):
            lcd_string("SELECT: " + Product_List[Product_Index], LCD_LINE_2)
            if Product_List[Product_Index] == "COFFEE":
                if not check_for_coffee():
                    lcd_string("SOLD OUT !!!!", LCD_LINE_1)
                    time.sleep(2)
                    return
                Product_Price = Coffee_Price
            if Product_List[Product_Index] == "COFFEE_MILK":
                if not check_for_coffee_milk():
                    lcd_string("SOLD OUT !!!!", LCD_LINE_1)
                    time.sleep(2)
                    return
                Product_Price = Coffee_Milk_Price
            if Product_List[Product_Index] == "MILK":
                if not check_for_milk():
                    lcd_string("SOLD OUT !!!!", LCD_LINE_1)
                    time.sleep(2)
                    return
                Product_Price = Milk_Price
            Product_Choose = Product_List[Product_Index]

            Is_People_Choose_Product = True
            time.sleep(2)

    else:
        Is_Check_Milk_For_Coffee = False
        while Is_People_Choose_Product:
            if GPIO.input(17):  
                lcd_string("BUYING CANCELLED", LCD_LINE_1)
                lcd_string("", LCD_LINE_2)
                time.sleep(1)
                Is_People_Input_Money = False
                Is_People_Choose_Product = False
                Is_People_Add_Milk_To_Coffee = False
                return

            if Money_Input == 0:
                lcd_string("PLEASE PAY  MONEY", LCD_LINE_1)
            else:
                lcd_string("PAID " + str(Money_Input), LCD_LINE_1)
            lcd_string("COST : " + str(Product_Price), LCD_LINE_2)
            if not Is_People_Input_Money:
                if GPIO.input(GPIO_Button_1):
                    Money_Input += 10000
                    lcd_string("PAID " + str(Money_Input), LCD_LINE_1)
                    time.sleep(2)
                if GPIO.input(GPIO_Button_2):
                    Money_Input += 5000
                    lcd_string("PAID " + str(Money_Input), LCD_LINE_1)
                    time.sleep(2)
                if GPIO.input(GPIO_Button_3):
                    Money_Input += 2000
                    lcd_string("PAID " + str(Money_Input), LCD_LINE_1)
                    time.sleep(2)
                if Product_Choose == "COFFEE":
                    if Money_Input >= Coffee_Price:
                        Is_People_Input_Money = True
                elif Product_Choose == "COFFEE_MILK":
                    if Money_Input >= Coffee_Milk_Price:
                        Is_People_Input_Money = True
                elif Product_Choose == "MILK":
                    if Money_Input >= Milk_Price:
                        Is_People_Input_Money = True

            else:
                while Is_People_Input_Money:
                    lcd_string("", LCD_LINE_2)
                    lcd_string("MAKING YOUR ITEM...", LCD_LINE_1)
                    lcd_string("WAITING....", LCD_LINE_2)

                    pwm = GPIO.PWM(4, 100)
                    pwm.start(0)
                    pwm.ChangeDutyCycle(20)
                    #

                    thread = Thread(target=enable_pump_motor_and_heater())
                    thread.start()
                    #

                    product_preparation(Product_Choose)
                    pwm.ChangeDutyCycle(15)
                    time.sleep(2)
                    lcd_string("PLEASE TAKE YOUR ITEM", LCD_LINE_1)
                    lcd_string("THANK YOU", LCD_LINE_2)
                    time.sleep(2)
                    Is_People_Input_Money = False
                    Is_People_Choose_Product = False
                    Is_People_Add_Milk_To_Coffee = False

                    Money_Input = 0
                    Product_Choose = ""
		    
# Main function
def main () :
 # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(LCD_E, GPIO.OUT)  
    GPIO.setup(LCD_RS, GPIO.OUT)  
    GPIO.setup(LCD_D4, GPIO.OUT)  
    GPIO.setup(LCD_D5, GPIO.OUT) 
    GPIO.setup(LCD_D6, GPIO.OUT)  
    GPIO.setup(LCD_D7, GPIO.OUT)  

    GPIO.setup(GPIO_Button_1, GPIO.IN)
    GPIO.setup(GPIO_Button_2, GPIO.IN)
    GPIO.setup(GPIO_Button_3, GPIO.IN)
    GPIO.setup(GPIO_Button_Cancel, GPIO.IN)
    GPIO.setup(GPIO_Pump_Motor, GPIO.OUT)
    GPIO.setup(GPIO_Heater, GPIO.OUT)


    GPIO.setup(4, GPIO.OUT)
    pwm = GPIO.PWM(4, 100)  ## PWM Frequency
    pwm.start(0)
    GPIO.setup(22, GPIO.OUT)
    pwm = GPIO.PWM(22, 100)  ## PWM Frequency
    pwm.start(0)
    GPIO.setup(23, GPIO.OUT)
    pwm = GPIO.PWM(23, 100)  ## PWM Frequency
    pwm.start(0)
    GPIO.setup(24, GPIO.OUT)
    pwm = GPIO.PWM(24, 100)  ## PWM Frequency
    pwm.start(0)
    GPIO.setup(25, GPIO.OUT)
    pwm = GPIO.PWM(25, 100)  ## PWM Frequency
    pwm.start(0)
    """while 1:
        pwm.ChangeDutyCycle(60)  # 16 : 18 do, 17 : 36 do, 18 : 54 do
        # time.sleep(0.8)
        # pwm.ChangeDutyCycle(10)
        time.sleep(5)
        pwm.ChangeDutyCycle(18)
        time.sleep(5)"""
    # Initialise display
    lcd_init()

    while True:
        program()

        # time.sleep(2)
	
def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):

    GPIO.output(LCD_RS, mode)  # RS

    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    lcd_toggle_enable()

    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    lcd_toggle_enable()


def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_string(message, line):

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)
	
	
# Command line execution

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()

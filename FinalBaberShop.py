from threading import Thread, Lock, Event
import time, random
#By Rodrigo Casanova

mutex = Lock()

#Interval in seconds
customerIntervalMin = 1
customerIntervalMax = 10
haircutDurationMin = 4
haircutDurationMax = 24
cashierDurationMin = 1
cashierDurationMax = 3

#Class with all the barber shop methods, inicialized with 2 lists, the waiting customers and waiting in couch customers.
#There will be 3 queues, queue for the seat, for the waiting room and for the cashier.
class BarberShop:
        waitingCustomers = []
        waitingInCouch = []
#Method to inicialize the barber, number of seats and cashier. Displaying their intervals of time.
        def __init__(self, barber, numberOfSeats,cashier):
                self.barber = barber
                self.numberOfSeats = numberOfSeats
                self.cashier = cashier
                print('BarberShop initilized with {} seats'.format(numberOfSeats))
                print('Customer min interval {}'.format(customerIntervalMin))
                print('Customer max interval {}'.format(customerIntervalMax))
                print('Haircut min duration {}'.format(haircutDurationMin))
                print('Haircut max duration {}'.format(customerIntervalMax))
                print('Cashier min duration {}'.format(cashierDurationMin))
                print('Cashier max duration {}'.format(cashierDurationMax))
                print('---------------------------------------')
#Method to open the barber shop
        def openShop(self):
                print('Barber shop is opening')
                workingThread = Thread(target = self.barberGoToWork)
                workingThread2 = Thread(target = self.cashierGoToWork)

                workingThread.start()
                workingThread2.start()
#Method to call the barber to work
        def barberGoToWork(self):
                while True:
                        #mutex.acquire()
#First it will check if there is nobody in the waiting room, if there is noone it will send the customer directly to the barber chair.
                        if len(self.waitingInCouch) > 0:
                                c = self.waitingInCouch[0]
                                del self.waitingInCouch[0]
                                #mutex.release()
                                self.barber.cutHair(c)

 #If there is noone on the waiting room it will send them directly to the barber's chair.                               
                        if len(self.waitingCustomers) > 0:
                                c = self.waitingCustomers[0]
                                del self.waitingCustomers[0]
                               # mutex.release()
                                self.barber.cutHair(c)


#If there is no customers in the waiting room and in the shop the barber will sleep.                               

                        else:
                               # mutex.release()
                                print('Aaah, all done, going to sleep')
                                barber.sleep()
                                print('Barber woke up')

#Method to call the cashier to work.                               
        def cashierGoToWork(self):
                while True:
                        mutex.acquire()

                        if len(self.waitingCustomers) > 0:
                                c = self.waitingCustomers[0]
                                del self.waitingCustomers[0]
                                mutex.release()
                                self.cashier.work(c)
#If there is no more customers in the shop the cashier will rest.                                

                        else:
                                mutex.release()

                                print('Aaah, all done everyone paid')
                                cashier.sleep()
                                print('Cashier woke up')

#Method to enter the barber shop. The customer will check if there is a available seat, if not it will go to the couch(waiting room).

        def enterBarberShop(self, customer):
                mutex.acquire()
                print('>> "{}" entered the shop and is looking for a seat'.format(customer.name))

#If there are no seats available the program will put the custumer in the waitingInCouch list.                
                if len(self.waitingCustomers) >= self.numberOfSeats:
                        print('All barbers are occupied, "{}" is going to the waiting room.'.format(customer.name))
                        self.waitingInCouch.append(c)

                        mutex.release()
#If there is a seat available, it will take the customer directly to the barber's seat.                        
                elif len(self.waitingCustomers) < self.numberOfSeats:
                        print('"{}" went directly to the chair'.format(customer.name))
                        self.waitingCustomers.append(c)
                        mutex.release()
                        barber.wakeUp()

#Method to create a line for the cashier.                        
        def enterCashierLine(self, customer):
                mutex.acquire()
                print('>> "{}" is getting in line to pay'.format(customer.name))

                if len(self.waitingCustomers) >= 0:

                        mutex.release()
                        cashier.work(customer)




#Class to create customers.               
class Customer:
        def __init__(self, name):
                self.name = name
#Class to create all the barber's activities.
class Barber:
        barberWorkingEvent = Event()

        def sleep(self):
                self.barberWorkingEvent.wait()

        def wakeUp(self):
                self.barberWorkingEvent.set()

        def cutHair(self, customer):
                #Set barber as busy
                self.barberWorkingEvent.clear()

                print('"{}" is having a haircut'.format(customer.name))

                randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
                time.sleep(randomHairCuttingTime)
                print('"{}" Hair cut time was {} minutes'.format(customer.name, randomHairCuttingTime))
                #print('{0} is going to the cashier to pay'.format(customer.name))

                print('"{}" is done'.format(customer.name))
                barberShop.enterCashierLine(customer)

#Class to create all the cashier activities.                
class Cashier:
        cashierWorkingEvent = Event()
        def sleep(self):
                self.cashierWorkingEvent.wait()
        def wakeUp(self):
                self.cashierWorkingEvent.set()

        def work(self, customer):
                self.cashierWorkingEvent.clear()
                #print('{0} is going to pay for the haircut.'.format(customer.name))
                randomPaymentTime = random.randrange(cashierDurationMin, cashierDurationMax+1)

                print('"{}" paid and is going home.'.format(customer.name))
                print('"{}" Time in line {} minutes'.format(customer.name, randomPaymentTime))

if __name__ == '__main__':
        customers = []
#The names that will populate the List.
        customers.append(Customer('Ronaldo'))
        customers.append(Customer('Pedro'))
        customers.append(Customer('Maria'))
        customers.append(Customer('Axel'))
        customers.append(Customer('Andrea'))
        customers.append(Customer('Roberto'))
        customers.append(Customer('Lily'))
        customers.append(Customer('Sofia'))
        customers.append(Customer('Catia'))
        customers.append(Customer('Mary'))
        customers.append(Customer('James'))
        customers.append(Customer('Margret'))
        customers.append(Customer('Bryan'))
        customers.append(Customer('Mathew'))
        customers.append(Customer('Jorge'))
        customers.append(Customer('Joseph'))
        customers.append(Customer('Agnaldo'))

        barber = Barber()
        cashier = Cashier()
        numberOfSeats = 3

        barberShop = BarberShop(barber, numberOfSeats, cashier)
        barberShop.openShop()

        while len(customers) > 0:
                c = customers.pop()
                #New customer enters the barbershop
                barberShop.enterBarberShop(c)

                customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)

                time.sleep(customerInterval)






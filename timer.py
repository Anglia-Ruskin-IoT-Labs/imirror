

 
def RestartTimer():
    counter = open('/tmp/counter', 'w')
    value = str(60)
    counter.write(value)
    counter.close()
    

def ZeroTimer():
    counter = open('/tmp/counter', 'w')
    value = str('0           ')
    counter.write(value)
    counter.close()

def DecrementTimer():
    counter = open('/tmp/counter', 'r+')
    value = counter.read()
    counter.close()
    counter = open('/tmp/counter', 'r+')
    counter.write('          ') ###in case noone use it for 316 years
    counter.close()
    counter = open('/tmp/counter', 'r+')
    temp = int(value) - 1
    rewrite = str(temp)
    counter.write(rewrite)
    counter.close()

def ReadTimer():
    counter = open('/tmp/counter', 'r')
    tmp = counter.read()
    value = int(tmp)
    counter.close()
    return value



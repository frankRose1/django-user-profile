
password = 'FRANKrose123!'
first = 'frank'
last = 'rose'

def check(password, val):
  if val.lower() in password.lower():
    print('its here')
  else:
    print('Not in there')



check(password, first)
check(password, last)
check(password, 'random')

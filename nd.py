import pyautogui
import PIL
import subprocess
import time

SCREEN = "nd_screen.png"  # any file already here will be destroyed

im = None

shop        = PIL.Image.open('nd_shop.png')
shopleft    = PIL.Image.open('nd_shopleft.png')
shopleftm   = PIL.Image.open('nd_shopleftm.png')
shopright   = PIL.Image.open('nd_shopright.png')
shoprightm  = PIL.Image.open('nd_shoprightm.png')
shoptop     = PIL.Image.open('nd_shoptop.png')
shoptopm    = PIL.Image.open('nd_shoptopm.png')
shopbottom  = PIL.Image.open('nd_shopbottom.png')
shopbottomm = PIL.Image.open('nd_shopbottomm.png')
transmute   = PIL.Image.open('nd_transmute.png')
transmute2  = PIL.Image.open('nd_transmute2.png')
secretshop  = PIL.Image.open('nd_secretshop.png')
secretshop2 = PIL.Image.open('nd_secretshop2.png')

def run(command):
  #return subprocess.check_output(command).decode("utf-8").replace('\r', '')
  return subprocess.run(command, shell=True)

def screenshot():
  global im
  #run('magick import -window "Crypt of the NecroDancer v4.1.0-b5237" '+SCREEN)
  run('magick import -silent -window "Crypt of the NecroDancer v4.1.0-b5142" '+SCREEN)
  # TODO sometimes the previous image is opened, even after a delay?!
  im = PIL.Image.open(SCREEN)
  if im.width != 640 and im.height != 360:
    assert False, (im.width, im.height)

def locate(needle_im):
  try:
    return pyautogui.locate(needle_im, im, confidence=0.9)
  except pyautogui.ImageNotFoundException:
    return None

def locatesecretshop():
  box = locate(secretshop)
  if box:
    # out of the ideal 10x10 tile center, we search for the 7th and 8th rows
    # (near the bottom), so the middle row is 1 above the search space
    return (box.left+5, box.top-1)
  box = locate(secretshop2)
  if box:
    return (box.left+5, box.top-1)
  return None

def locateshop():
  box = locate(shop)
  if box:
    box = locate(shopleft)
    if box:
      return (box.left+box.width, box.top+5)
    box = locate(shopleftm)
    if box:
      return (box.left+box.width, box.top+5)
    box = locate(shopright)
    if box:
      return (box.left, box.top+5)
    box = locate(shoprightm)
    if box:
      return (box.left, box.top+5)
    box = locate(shoptop)
    if box:
      return (box.left+5, box.top+box.height)
    box = locate(shoptopm)
    if box:
      return (box.left+5, box.top+box.height)
    box = locate(shopbottom)
    if box:
      return (box.left+5, box.top)
    box = locate(shopbottomm)
    if box:
      return (box.left+5, box.top)
  return None

def go(steplist):
  for move in steplist:
    if move == 'U':
      pyautogui.press('i')
    elif move == 'L':
      pyautogui.press('j')
    elif move == 'D':
      pyautogui.press('k')
    elif move == 'R':
      pyautogui.press('l')
    elif move == '-':
      pass
    elif move == 'b':
      pyautogui.press('x')
    else:
      assert False, move
    time.sleep(0.43)

def navigatetoshop(horiz_steps, horiz_dir, vert_steps, vert_dir):
  if horiz_steps == 2:
    go(horiz_dir)
    go(vert_dir*4)
    go(horiz_dir)
    go(vert_dir*(vert_steps-3))
  elif vert_steps == 2:
    go(vert_dir)
    go(horiz_dir*4)
    go(vert_dir)
    go(horiz_dir*(horiz_steps-3))
  elif horiz_steps < vert_steps:
    go(horiz_dir*horiz_steps)
    go(vert_dir*(vert_steps+1))
  else:
    go(vert_dir*vert_steps)
    go(horiz_dir*(horiz_steps+1))
  screenshot()
  return locate(transmute) or locate(transmute2)

def navigatetosecretshop(horiz_steps, horiz_dir, inverse_horiz_dir, vert_steps, vert_dir, inverse_vert_dir):
  if horiz_steps == 3:
    go(vert_dir*vert_steps)
    go(horiz_dir*2)
    go('b')
    go(inverse_horiz_dir*2)
    go('-')
    go(horiz_dir*3)
  elif vert_steps == 3:
    go(horiz_dir*horiz_steps)
    go(vert_dir*2)
    go('b')
    go(inverse_vert_dir*2)
    go('-')
    go(vert_dir*3)
  else:
    # approach the hallway wall from the side
    if horiz_steps > 3:
      go(vert_dir*(vert_steps-1))
      go(horiz_dir*horiz_steps)
      go('b')
      go(inverse_horiz_dir*2)
      go('-')
      go(horiz_dir*2)
      go(vert_dir)
    else:
      go(horiz_dir*(horiz_steps-1))
      go(vert_dir*vert_steps)
      go('b')
      go(inverse_vert_dir*2)
      go('-')
      go(vert_dir*2)
      go(horiz_dir)
  screenshot()
  return locate(transmute) or locate(transmute2)

def navigateoutofsecretshop(horiz_steps, inverse_horiz_dir, vert_steps, inverse_vert_dir):
  go('RL')
  if horiz_steps == 3:
    go(inverse_horiz_dir*3)
    go(inverse_vert_dir*vert_steps)
  elif vert_steps == 3:
    go(inverse_vert_dir*3)
    go(inverse_horiz_dir*horiz_steps)
  elif horiz_steps > 3:
    go(inverse_vert_dir)
    go(inverse_horiz_dir*horiz_steps)
    go(inverse_vert_dir*(vert_steps-1))
  else:
    go(inverse_horiz_dir)
    go(inverse_vert_dir*vert_steps)
    go(inverse_horiz_dir*(horiz_steps-1))

def main():
  print('Please manually switch to ND window (sleeping 5 seconds)')
  time.sleep(5)

  start = round(time.time())
  navigable_shops = 0
  total_shops = 0
  navigable_secretshops = 0
  total_secretshops = 0

  while True:
    #time.sleep(2)
    pyautogui.press('q')
    time.sleep(0.5)
    screenshot()

    secretshop_location = locatesecretshop()
    shop_location = locateshop()

    if secretshop_location:
      left_coords, top_coords = secretshop_location
      horiz_steps = round((left_coords - 320)/12)
      vert_steps = round((top_coords + 6 - 180)/12)
      horiz_dir = 'L' if horiz_steps <= 0 else 'R'
      vert_dir = 'U' if vert_steps <= 0 else 'D'
      inverse_horiz_dir = 'R' if horiz_steps <= 0 else 'L'
      inverse_vert_dir = 'D' if vert_steps <= 0 else 'U'
      horiz_steps = abs(horiz_steps)
      vert_steps = abs(vert_steps)
      total_secretshops += 1
      if (horiz_steps <= 2) ^ (vert_steps <= 2):  # xor
        navigable_secretshops += 1
        print(f'Found {navigable_secretshops}/{total_secretshops} secret shops after {round(time.time())-start} seconds')
        if navigatetosecretshop(horiz_steps, horiz_dir, inverse_horiz_dir, vert_steps, vert_dir, inverse_vert_dir):
          print("Found transmute in secret shop!")
          pyautogui.press('y')
          break
      saved_horiz_steps = horiz_steps
      saved_vert_steps = vert_steps

    if shop_location:
      left_coords, top_coords = shop_location
      horiz_steps = round((left_coords - 320)/12)
      vert_steps = round((top_coords + 6 - 180)/12)
      horiz_dir = 'L' if horiz_steps <= 0 else 'R'
      vert_dir = 'U' if vert_steps <= 0 else 'D'
      horiz_steps = abs(horiz_steps)
      vert_steps = abs(vert_steps)
      total_shops += 1
      #print(f'Shop found {horiz_steps} steps {horiz_dir} and {vert_steps} steps {vert_dir}')
      if (horiz_steps <= 2) ^ (vert_steps <= 2):  # xor
        if secretshop_location:
          # bad code style: vars conditionally defined
          navigateoutofsecretshop(saved_horiz_steps, inverse_horiz_dir, saved_vert_steps, inverse_vert_dir)
        navigable_shops += 1
        print(f'Found {navigable_shops}/{total_shops} shops after {round(time.time())-start} seconds')
        if navigatetoshop(horiz_steps, horiz_dir, vert_steps, vert_dir):
          print("Found transmute in shop!")
          pyautogui.press('y')
          break


if __name__ == '__main__':
  main()

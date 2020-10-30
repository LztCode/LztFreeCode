import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import random as r

m = PyMouse()
k = PyKeyboard()
uTime = float(input('请输入开始击键前等待时间(秒): '))
uStartTime = float(input('请输入击键间隔时间下限(秒): '))
uEndTime = float(input('请输入击键间隔时间上限(秒): '))

time.sleep(uTime)

print('开始击键')
file_name = './test.txt'
with open(file_name, 'r', encoding="utf-8") as f:
    let = f.read()
    f.close()
letter = []
for iword in let:
    # letter += iword.replace("\n","").replace("\t","")
    letter += iword.replace("\t", "")
# print(letter)
for qWord in letter:
    # time.sleep(r.uniform(0.03, 0.09))
    time.sleep(r.uniform(uStartTime, uEndTime))
    k.press_key(qWord)
    k.release_key(k.shift_key)
    k.release_key(k.control_key)
    k.release_key(k.alt_key)
    k.release_key(k.caps_lock_key)
    k.press_key(k.delete_key)
    k.release_key(k.delete_key)

print('结束击键')

# k.press_key(k.alt_key)#按住alt键
# k.press_key(k.control_key)#按住ctrl键
# k.press_key(k.enter_ikey)#按住enter键
# k.tap_key(k.tab_key)#点击tab键
# k.tap_key(k.delete_key)#点击delete键
# k.release_key(k.alt_key)#松开alt键
# k.tap_key(k.function_keys[5])#点击功能键F5
# k.tap_key(k.numpad_keys[5],2)#点击小键盘s共2次

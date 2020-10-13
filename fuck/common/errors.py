
OK = 0

VCODE_ERROR = 1000


LOGIN_REQUIRE = 1001

USER_NOT_EXIST = 1002

PROFILE_ERROR = 1003

"""
type:除了可以验证类型以外还可以批量"定义类"
    def run(self):
        print('im god')
    Dog = type('类名',(object,),{'属性１':1,'属性２':2,'函数':run})
    d = Dog()
    d.run()
-->im god
# python中，函数也是一种特殊的属性存于类中
"""

class LogicError(Exception):
    code = 0

    def __str__(self): # 调用类的时候直接打印__str__()函数
        return self.__class__.__name__  #__class__.__name__:就是类名


def generate_logic_error(name:str,code:int) -> LogicError:
    base_cls = (LogicError,)
    return type(name,base_cls,{'code':code})

OK = generate_logic_error('OK',0)
VcodeError = generate_logic_error('VcodeError',1000)
VcodeExist = generate_logic_error('VcodeExist',1001)
LoginRequire = generate_logic_error('LoginRequire',1002)
UserNotExist = generate_logic_error('UserNotExist',1003)
ProfileError = generate_logic_error('ProfileError',1004)
NotHasPerm = generate_logic_error('NotHasPerm',1005)

import math
from os import fdopen

fVLN = -180
fLN = -60
fMN = -30
fSN = -10
fNO = 0
fSP = 10
fMP = 30
fLP = 60
fVLP = 180
FL_AND = "AND"
FL_OR = "OR"

la_angle_min = -30
la_angle_max = 30

motor_power = 0.5


class FuzzyRule:
    def __init__(self, fe, op, fde, z):
        self.fe = fe
        self.op = op
        self.fde = fde
        self. z = z

# fl_rule_arr = []


# fl_rule_arr.append(FuzzyRule(fNO, FL_AND, fNO, fNO))
# fl_rule_arr.append(FuzzyRule(fVLN, FL_OR, fVLN, fVLP))
# fl_rule_arr.append(FuzzyRule(fVLP, FL_OR, fVLP, fVLN))
# fl_rule_arr.append(FuzzyRule(fLN, FL_AND, fSN, fVLP))
# fl_rule_arr.append(FuzzyRule(fLP, FL_AND, fSP,fVLN))
# fl_rule_arr.append(FuzzyRule(fSN, FL_AND, fSN,fSP))
# fl_rule_arr.append(FuzzyRule(fSP, FL_AND, fSP,fSN))
numofrules = 7  # счетчик правил для нечеткого регулятора


class CourseRegulator:

    gl_last_cource_error: float
    gl_cource_error: float
    COURCE_ERROR_FILT_SIZE: float
    cource_error_arr: float = []
    la_target_ang_arr: float = []
    LA_TARGET_FILT_SIZE: float
    cource_error_pointer: float
    la_target_filt_pointer: float
    fl_rule_arr = []
    loc_angle: float

    def __init__(self):
        self.gl_last_cource_error = 0.0
        self.gl_cource_error = 0.0
        self.COURCE_ERROR_FILT_SIZE = 10
        self.cource_error_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.la_target_ang_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.LA_TARGET_FILT_SIZE = 10
        self.cource_error_pointer = 0
        self.la_target_filt_pointer = 0
        self.fl_rule_arr.append(FuzzyRule(fNO, FL_AND, fNO, fNO))
        self.fl_rule_arr.append(FuzzyRule(fVLN, FL_OR, fVLN, fVLP))
        self.fl_rule_arr.append(FuzzyRule(fVLP, FL_OR, fVLP, fVLN))
        self.fl_rule_arr.append(FuzzyRule(fLN, FL_AND, fSN, fVLP))
        self.fl_rule_arr.append(FuzzyRule(fLP, FL_AND, fSP, fVLN))
        self.fl_rule_arr.append(FuzzyRule(fSN, FL_AND, fSN, fSP))
        self.fl_rule_arr.append(FuzzyRule(fSP, FL_AND, fSP, fSN))

    def normalice(self, value: float, y_min: float, y_max: float, x_min: float, x_max: float):
        val = 0.0
        val = (value - y_max) * (x_min - x_max) / (y_min - y_max) + x_max
        return val

    def normalice_center_point(self, value: float, y_min: float, y_mid: float, y_max: float, x_min: float, x_mid: float, x_max: float):
        val = 0.0
        if (value > y_mid):
            val = self.normalice(value, y_mid, y_max, x_mid, x_max)
        elif (value <= y_mid):
            val = self.normalice(value, y_min, y_mid, x_min, x_mid)
        else:
            return x_mid
        return val

    def mu(self, x, A):
        """
        Степень принадлежности µÃ(x)  какой степени (мере) элемент x принадлежит нечёткому множеству Ã.
        #Args
            х Элемент из Х
            A Нечеткое множество Ã
        #Returns
            Мера принадлежности
        """
        return math.exp(-(pow(x - A, 2) / (2 * pow(30, 2))))

    def processRules(self, fe, de):
        """
        """
        summ_alpha_c = 0.0
        summ_alpha = 0.0
        for i in range(numofrules):
            alpha = 0.0
            my_mue = 0.0
            my_mude = 0.0
            my_mue = self.mu(fe, self.fl_rule_arr[i].fe)
            my_mude = self.mu(de, self.fl_rule_arr[i].fde)
            if (self.fl_rule_arr[i].op == FL_AND):
                if (my_mue < my_mude):
                    alpha = my_mue
                else:
                    alpha = my_mude
            else:
                if my_mue > my_mude:
                    alpha = my_mue
                else:
                    alpha = my_mude
            # alpha = fl_rule_arr[i].op == 0 ? min_my_float(mue, mude) : max_my_float(mue, mude);
            # числитель и знаменатель для дискретного варианта
            # центроидного метода приведения к четкости
            summ_alpha_c = summ_alpha_c + (alpha * self.fl_rule_arr[i].z)
            summ_alpha = summ_alpha + alpha

        # вычисляем воздействие на объект управления
        ret = summ_alpha_c / summ_alpha
        return ret

    
    def calculateAngle(self, current_heading: float, bearing: float):
        try:
            self.gl_cource_error = current_heading - bearing
            self.cource_error_arr[self.cource_error_pointer] = self.gl_cource_error

            # sum_cource = 0.0
            # for i in range (self.COURCE_ERROR_FILT_SIZE):
            #     sum_cource += self.cource_error_arr[i]
            # self.cource_error_pointer = self.cource_error_pointer + 1
            # if (self.cource_error_pointer == self.COURCE_ERROR_FILT_SIZE) :
            #     self.cource_error_pointer = 0
            # self.gl_cource_error = sum_cource / self.COURCE_ERROR_FILT_SIZE

            self.delta_cource_error = self.gl_cource_error - self.gl_last_cource_error
            self.gl_last_cource_error = self.gl_cource_error
            self.loc_angle = self.processRules(
                self.gl_cource_error, self.delta_cource_error)

            self.loc_angle = self.normalice_center_point(
                self.loc_angle, -180.0, 0.0, 180.0, la_angle_min, 0.0, la_angle_max)

            # self.la_target_ang_arr[self.la_target_filt_pointer] = self.loc_angle
            # sum_la = 0.0
            # for i in range(self.LA_TARGET_FILT_SIZE):
            #     sum_la = sum_la + self.la_target_ang_arr[i]

            # self.la_target_filt_pointer = self.la_target_filt_pointer + 1
            # if self.la_target_filt_pointer == self.LA_TARGET_FILT_SIZE :
            #     self.la_target_filt_pointer = 0
            # self.loc_angle = sum_la / self.LA_TARGET_FILT_SIZE

            return self.loc_angle
        except:
            return 0.0

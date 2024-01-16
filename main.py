import numpy as np
import matplotlib.pyplot as plt

default_color_order = ['b', 'g', 'r', 'c', 'y', 'm', 'purple', 'brown', 'orange']


def dice_roll_string_to_array_lambda(dice_string="3d8 +4d12"):
    dice_arr = dice_string.replace(" ", "").split('+')
    dice_shape = []
    lambda_shape = []
    lambda_instr = []
    for dice_type in dice_arr:
        if 'H' in dice_type:
            lambda_instr.append('H')
        elif 'L' in dice_type:
            lambda_instr.append('L')
        else:
            lambda_instr.append('')

        dice_type = dice_type.replace("H", "").replace("L", "")
        n, d = dice_type.split('d')[:2]
        lambda_shape.append(int(n))

        for i in range(int(n)):
            dice_shape.append(int(d))

    # print(dice_shape)
    # print(lambda_shape)
    # print(lambda_instr)

    return dice_shape, lambda_shape, lambda_instr


def distribute_array(arr, distr):
    ret_arr = []
    for i, x in enumerate(distr):
        ret_arr.append(arr[sum(distr[:i]):sum(distr[:i+1])])
    return ret_arr


def create_lambda(shape, instr):
    def f(arr):
        reshaped_arr = distribute_array(arr, shape)
        # print(reshaped_arr)
        result = 0
        for i, chunk in enumerate(reshaped_arr):
            result += sum(chunk) + len(chunk)
            if instr[i] == 'H':
                result -= min(chunk)+1
            elif instr[i] == 'L':
                result -= max(chunk)+1
        # print(result)
        return result
    return f


def dice_prob(dice_shape=None, count_f=None):
    # print(dice_shape)
    if dice_shape is None:
        dice_shape = [8, 12]

    if count_f is None:
        def count_f(x):
            return sum(x)+len(x)

    dice_index_matrix = np.zeros(dice_shape, dtype=bool)
    # print(dice_index_matrix.shape)

    p_dict = dict()
    for (x, i) in np.ndenumerate(dice_index_matrix):
        k = count_f(x)
        if k in p_dict:
            p_dict[k] += 1
        else:
            p_dict[k] = 1.0

    print(p_dict)

    for k in p_dict.keys():
        # multiplied by 100 to adjust showing probability as a percentage
        p_dict[k] = p_dict[k]*100 / dice_index_matrix.size

    print(p_dict)

    return p_dict.keys(), p_dict.values()


def plot_graphs(dice_configs):
    for i, d_c in enumerate(dice_configs):
        print("Dice Config: %s" % d_c)
        dice_shape, lambda_shape, lambda_instr = dice_roll_string_to_array_lambda(d_c)
        funt = create_lambda(lambda_shape, lambda_instr)
        d_arr, p_arr = dice_prob(dice_shape, funt)

        # divided by 100 to transform percentage to probability
        mean = sum([i * p / 100 for (i, p) in zip(d_arr, p_arr)])
        aad = sum([abs(mean - i) * p / 100 for (i, p) in zip(d_arr, p_arr)])
        aad_label_plus = "MEAN + AAD: ~%s" % round(mean + aad, 1)
        aad_label_mins = "MEAN - AAD: ~%s" % round(mean - aad, 1)

        plt.plot(d_arr, p_arr, label=d_c, color=default_color_order[i])
        label = "MEAN: ~%s AAD: ~%s" % (round(mean, 1), round(aad, 1))
        print(label)

        plt.axvline(x=mean, color=default_color_order[i], label=label)
        plt.axvline(x=mean+aad, color=default_color_order[i], label=aad_label_plus)
        plt.axvline(x=mean-aad, color=default_color_order[i], label=aad_label_mins)

        plt.ylabel("Probability")
        plt.xlabel("Dice Result")
        plt.legend()
        plt.show()


if __name__ == '__main__':
    plot_graphs(["2d8L+2d12L", "1d8+2d12L", "2d8L+1d12", "1d8+1d12", "2d8H+1d12", "1d8+2d12H", "2d8H+2d12H"])


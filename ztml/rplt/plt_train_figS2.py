#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2021/05/25 09:01:54'

import numpy as np
import matplotlib.pyplot as plt
import os


def plt_mse(data, outfn):
    # lv #3CAF6F
    fig = plt.figure()
    data = data[1:, :]
    x = data[:, 0]
    ytrain = data[:, -2]
    ytest = data[:, -1]

    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax1 = fig.add_axes([left, bottom, width, height])
    ax1.plot(x, ytrain, c='#347FE2', linewidth=3.2)
    ax1.plot(x, ytest, c='#F37878' ,linewidth=3.2)
    ax1.set_xlim(-1, 300)
    ax1.set_xlabel('Steps')
    ax1.set_ylabel("Mean Square Error (MSE)")
    left, bottom, width, height = 0.4, 0.4, 0.35, 0.35
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.plot(x, ytrain, c='#347FE2', linewidth=2.2)
    ax2.plot(x, ytest, c='#F37878', linewidth=2.2)
    
    train_final_mean = np.mean(ytrain[3000:])
    test_final_mean = np.mean(ytest[3000:])
    ax2.plot(range(300, 5000), [train_final_mean]*(5000-300), 'r', linestyle='--', linewidth=2.2)
    ax2.text(2000, 0.004, 'MSE=%.5f' % train_final_mean)
    ax2.set_xlabel('Steps')
    ax2.set_ylabel('MSE')
    ax2.set_xlim(300, 5000)
    ax2.set_ylim(0, 0.01)
    ax2.set_xticks([300, 1000, 2000, 3000, 4000, 5000])
    
    plt.savefig(outfn)


def read_mse_data(fn):
    with open(fn, 'r') as f:
        data = np.array([[float(m.split(':')[-1]) for m in i.split('|')] for i in f.readlines()])
    return data


def read_cal_predit(fn):
    with open(fn, 'r') as f:
        data = np.array([i.split() for i in f.readlines()[0:]], dtype=np.float)
    newpredict = np.array([1.05 if i > 0.5 else 0.05 for i in data[:, 1]], dtype=np.float)
    return np.vstack((data[:, 0], newpredict)).transpose()

    
def run_mse(fn, outfn):
    dd = read_mse_data(fn)
    plt_mse(dd, outfn)


def plt_result(predict_data, training_data, text=None, save_fn=None, show=False):
    label_font = {"fontsize": 16, 'family': 'Times New Roman'}
    legend_font = {"fontsize": 12, 'family': 'Times New Roman'}
    tick_font_dict = {"fontsize": 12, 'family': 'Times New Roman'}
    index_label_font = {"fontsize": 20, 'weight': 'bold', 'family': 'Times New Roman'}
    pindex = ['A', 'B', 'C', 'D', 'E', 'F']
    _xwd, _ywd = 0.118, 0.12
    sax = [[0.18098039215686275 + 0.020, 0.60 + 0.1, _xwd, _ywd],
           [0.49450980392156866 + 0.035, 0.60 + 0.1, _xwd, _ywd],
           [0.82803921568627460 + 0.030, 0.60 + 0.1, _xwd, _ywd],
           [0.18098039215686275 + 0.020, 0.11 + 0.1, _xwd, _ywd],
           [0.49450980392156866 + 0.035, 0.11 + 0.1, _xwd, _ywd],
           [0.82803921568627460 + 0.030, 0.11 + 0.1, _xwd, _ywd]]

    nrow = 2
    ncol = 3
    fig, axes = plt.subplots(nrow, ncol, figsize=(16, 8))
    plt.rc('font', family='Times New Roman', weight='normal')
    axes = axes.flatten()
    
    assert axes.shape[0] == len(predict_data) == len(training_data)
    if text is not None:
        assert axes.shape[0] == len(text)
    colors = {'Calculated': '#3CAF6F', 'Predicted': '#FF8C00'}

    for i in range(axes.shape[0]):
        ax = axes[i]
        pd1 = predict_data[i]
        ax.scatter(range(1, len(pd1)+1), pd1[:, 0], edgecolors='#53c482', color=colors['Calculated'], alpha=1, linewidths=0.01, s=90)
        ax.scatter(range(1, len(pd1)+1), pd1[:, 1], edgecolors='#ffa227', color=colors['Predicted'], alpha=1, linewidths=0.01, s=90)
        slice_set = -0.1, 1.15
        _tmp_xy = np.linspace(slice_set, pd1.shape[0])
        ax.set_xlim(-5, len(pd1)+5)
        ax.set_ylim(slice_set)
        ax.text(3, 0.55, text[i], fontdict=legend_font)

        ax.text(0.01, 1.2, pindex[i], fontdict=index_label_font)
        ax.set_xticks([0, 100, 200, 252])
        ax.set_xticklabels(ax.get_xticks(), tick_font_dict)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['N-type', 'P-type'], tick_font_dict)
        ax.set_xlabel('Data point', tick_font_dict)
        
        if i == 0:
            labels = list(colors.keys())
            handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
            ax.legend(handles=handles, labels=labels, ncol=2, loc='upper left', bbox_to_anchor=[0.2, 0.3])

        d = ax.get_position()
        print(i, d)
        tdata = training_data[i][1:, :]
        tx = tdata[:, 0]
        ytrain = tdata[:, -2]
        ytest = tdata[:, -1]

        left, bottom, width, height = sax[i]
        
        if i == 3:
            train_final_mean = np.mean(ytrain[8000:])
            test_final_mean = np.mean(ytest[8000:])
        else:
            train_final_mean = np.mean(ytrain[2500:])
            test_final_mean = np.mean(ytest[2500:])

        ax2 = fig.add_axes([left, bottom, width, height])
        if i > 1:
            lw = 1.2
        else:
            lw = 2.2
        ax2.plot(tx, ytrain, c='#347FE2', linewidth=lw, label='train')
        ax2.plot(tx, ytest, c='#F37878', linewidth=1.2, label='test')
        
        if i == 0:
            ax2.set_xlim(-120, 8000)
            ax2.set_ylim(-0.001, 1)
            ax2.text(100, 0.5, 'train:%.4f\ntest :%.4f' % (float(train_final_mean), float(test_final_mean)))
            ax2.legend(fontsize=8, loc='upper right')
        elif i == 1:
            ax2.set_xlim(-120, 1000)
            ax2.set_ylim(-0.001, 1)
            ax2.text(600, 0.1, 'train:%.5f\ntest :%.5f' % (float(train_final_mean), float(test_final_mean)))
            ax2.legend(fontsize=8, loc='lower right')
        elif i == 3:
            ax2.set_xlim(-120, 1000)
            ax2.set_ylim(-0.001, 1)
            ax2.text(2000, 0.25, 'train:%.5f\ntest :%.5f' % (float(train_final_mean), float(test_final_mean)))
            ax2.legend(fontsize=8)
        elif i == 4:
            ax2.set_xlim(-120, 8000)
            ax2.set_ylim(-0.001, 1)
            ax2.text(2000, 0.01, 'train:%.5f\ntest :%.5f' % (float(train_final_mean), float(test_final_mean)))
            ax2.legend(fontsize=8)
        else:
            ax2.set_xlim(-120, 1000)
            ax2.set_ylim(-0.001, 1)
            ax2.text(1000, 0.01, 'train:%.5f\ntest :%.5f' % (float(train_final_mean), float(test_final_mean)))
            ax2.legend(fontsize=8)

        ax2.set_ylabel('Cross Entropy')
        plt.tight_layout()

    if save_fn is not None:
        plt.savefig(save_fn)
        
    if show:
        plt.show()

if __name__ == '__main__':
    # fn, ofn = r"training_module/out_run3.train", 'train.pdf'
    # fn, ofn = r"training_module/out_run3.test", 'test.pdf'
    label = 'run1'
    save_dir = r'..\rtrain\3ntype_training_module'
    # run_mse(os.path.join(save_dir, 'running_%s.log' % label), 'training_%s.pdf' % label)
    text = ["Activation : Relu\nOptimizer : Adam\nHidden Layers :\n[100, 50, 20]",
            "Activation : Tanh\nOptimizer : Adam\nHidden Layers :\n[100, 50, 20]",
            "Activation : Sigmod\nOptimizer : Adam\nHidden Layers :\n[100, 50, 20]",
            "Activation : Sigmod\nOptimizer : SGD\nHidden Layers :\n[100, 50, 20]",
            "Activation : Sigmod\nOptimizer : Adam\nHidden Layers :\n[100, 100, 50, 20]",
            "Activation : Sigmod\nOptimizer : Adam\nHidden Layers :\n[500, 100, 50, 20]"]
    for i in ['train_30_train.csv', 'train_30_test.csv', 'valid_40.csv']:
        predict_data, training_data = [], []
        # for label in ['3layer_100_Elu', '3layer_100_PRelu', '3layer_100_sigmod', '3layer_100_Tanh', '3layer_100', '4layer_100', '4layer_500']:
        for label in ["3layer_100", "3layer_100_sgd", "3layer_100_sgd_Sigmod", "3layer_100_sgd_Tanh",
                      "3layer_100_sgd_Sigmod", "3layer_100_sgd_Tanh"]: #'3layer_100_Elu', '3layer_100_PRelu',
            training_fn = os.path.join(save_dir, 'running_%s.log' % label)
            training_data.append(read_mse_data(training_fn))

            output_fn = os.path.join(save_dir, 'result_%s_%s.out' % (i, label))
            predict_data.append(read_cal_predit(output_fn))
        
        save_fn = 'plt_%s_figS2.pdf' % i
        # plt_result(predict_data, training_data, text, save_fn=None, show=True)
        plt_result(predict_data, training_data, text, save_fn=save_fn, show=False)

        exit()

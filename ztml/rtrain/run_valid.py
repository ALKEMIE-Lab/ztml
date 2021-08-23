#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2021/06/15 22:01:37'

import os
from ztml.rtrain.train import ttest
from ztml.rtrain.train_Ntype import cross_entropyloss_ntype_ttest
import torch.nn as nn


def use_ml_to_predict_zt(head_dir, fname, has_t=True):
    save_dir = r'..\rtrain\final_training_module'
    nfeature = 11
    hidden_layer = [100, 100, 50, 20]  # [100, 50, 20]  [100, 100, 50, 20]
    label = '4layer_100'  # '3layer_100_Elu', '3layer_100_PRelu', '3layer_100_sigmod', '3layer_100_Tanh', '3layer_100', '4layer_100', '4layer_500'
    activation = nn.ReLU()
    num = 12000
    
    ttest(test_csv_fn=os.path.join(head_dir, fname),
          mp_fn=os.path.join(save_dir, 'dnn_params_%d_%s.pkl' % (num, label)),
          output_fn='z_result_valid_has_t_%s.out' % fname,
          save_dir=save_dir, n_feature=nfeature, hidden_nodes=hidden_layer,
          batch_size=500, shuffle=False, activation=activation,
          has_t=has_t)


def cel_use_ml_to_predict_ntype(head_dir, fname, has_t=True):
    save_dir = r'..\rtrain\final_ntype_training_module'
    nfeature = 11
    hidden_layer = [100, 100, 50, 20]  # [100, 50, 20]  [100, 100, 50, 20]
    label = '4layer_100'  # '3layer_100_Elu', '3layer_100_PRelu', '3layer_100_sigmod', '3layer_100_Tanh', '3layer_100', '4layer_100', '4layer_500'
    activation = nn.Tanh()
    num = 193
    
    cross_entropyloss_ntype_ttest(test_csv_fn=os.path.join(head_dir, fname),
                mp_fn=os.path.join(save_dir, 'dnn_params_%d_%s.pkl' % (num, label)),
                output_fn='ntype_z_result_valid_has_t_%s.out' % fname, shuffle=False,
                save_dir=save_dir, n_feature=nfeature, hidden_nodes=hidden_layer,
                batch_size=500, zt=False, n_output=2, has_t=has_t, activation=activation)


if __name__ == '__main__':
    head_dir = r'G:\ztml\ztml\rdata\all_rmcoref_data'
    fn2 = r'30_for_predict.csv'
    fn1 = r'10_for_check.csv'
    
    # has_t 指定想要获取那一列特征并且输出到结果中，-5列是温度(必须去掉label列)，第3列是C原子总数, 第12列wei B_Gpa, 可以区分开化合物的一列
    has_t = [-1, 2, 6]
    use_ml_to_predict_zt(head_dir, fn1, has_t=has_t)
    use_ml_to_predict_zt(head_dir, fn2, has_t=has_t)
    # use_ml_to_predict_ntype(head_dir, fn1, has_t=has_t)
    # use_ml_to_predict_ntype(head_dir, fn2, has_t=has_t)
    cel_use_ml_to_predict_ntype(head_dir, fn1, has_t=has_t)
    cel_use_ml_to_predict_ntype(head_dir, fn2, has_t=has_t)

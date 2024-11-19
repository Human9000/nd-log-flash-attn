
import time
import torch
import pandas as pd
from models import LogFA1d, LogFA2d, LogFA3d
from ptflops import get_model_complexity_info


if __name__ == '__main__':

    df = pd.DataFrame(columns=['model', 'channels', 'heads', 'bases', 'size', 'flops', 'params',  'time(ms)'])

    ma1 = LogFA1d(32, 4, [8,], down_factor=1, regist_flops=True).cuda()
    ma2 = LogFA2d(32, 4, [8,], down_factor=1, regist_flops=True).cuda()
    ma3 = LogFA3d(32, 4, [8,], down_factor=1, regist_flops=True).cuda()

    res = get_model_complexity_info(ma1, (32, 224*224,), as_strings=True, print_per_layer_stat=False)
    n = 10

    with torch.no_grad():
        # 1d
        time_start = time.time()
        for i in range(n):
            res = get_model_complexity_info(ma1, (32, 224*224,), as_strings=True, print_per_layer_stat=False)
        df.loc[df.shape[0]] = ['LogFA1d', 32, 4, [8,], (224*224,), *res, int((time.time() - time_start)*1000)*1./n]

        # 2d
        time_start = time.time()
        for i in range(n):
            res = get_model_complexity_info(ma2, (32, 224,  224), as_strings=True, print_per_layer_stat=False)
        df.loc[df.shape[0]] = ['LogFA2d', 32, 4, [8,], (224,  224), *res, int((time.time() - time_start)*1000)*1./n]

        # 3d
        time_start = time.time()
        for i in range(n):
            res = get_model_complexity_info(ma3, (32, 128, 128, 128), as_strings=True, print_per_layer_stat=False)
        df.loc[df.shape[0]] = ['LogFA3d', 32, 4, [8,], (128, 128, 128), *res, int((time.time() - time_start)*1000)*1./n]
    print(df)
    #      model  channels  heads bases             size       flops  params  time(ms)
    # 0  LogFA1d        32      4   [8]         (50176,)   1.03 GMac  4.51 k       1.1
    # 1  LogFA2d        32      4   [8]       (224, 224)   1.04 GMac   4.7 k       1.2
    # 2  LogFA3d        32      4   [8]  (128, 128, 128)  48.65 GMac  5.28 k      39.0

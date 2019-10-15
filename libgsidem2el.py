## @package libgsidem2el 地理院標高タイルから標高値を取得するライブラリ
#  @brief 地理院標高タイルから標高値を取得するライブラリ
# 地図の種類はDEM5A,DEM5B,DEM10B,DEMGMの４種類が選択可能 https://maps.gsi.go.jp/help/pdf/demapi.pdf参照
# zoom levelは，DEM5A,B:15, DEM10B:0-14, DEMGM:0-8
# getELメソッドで取得，DEM5AB，10Bは[m],DEMGMは[cm]の標高値を返す．
# それぞれの地図の対象範囲外は'outside'を返す
# 水面等により欠測の場合は，'e'を返す（地理院タイルの使用）.
# 一度読み込んだタイルはクラスの変数demdfに保存．近接するデータの取得が高速化される反面，大領域を一度に処理する場合はメモリを消費する．
#  @author computational-sediment-hyd https://github.com/computational-sediment-hyd
#  @date   2018/12/19
#  @version  version 0.1.0

import numpy as np
import pandas as pd
import urllib.request

## 地理院標高タイルから標高値を取得するライブラリ
# @brief
class libgsidem2el:
    def __init__(self, dem:'DEM5A, DEM5B, DEM10B, DEMGM' = 'DEM5A'):
        self.demdf = {}
    # https://maps.gsi.go.jp/development/ichiran.html#dem
        kind = {'DEM5A':'dem5a', 'DEM5B':'dem5b', 'DEM10B':'dem', 'DEMGM':'demgm' }
        self.url = "https://cyberjapandata.gsi.go.jp/xyz/" + kind[dem] + "/"
        
    # get Elevation from tile layer
    def getEL(self, lon, lat, zoom=15): 
    # change lon,lat to pixel coordinate
        z = zoom 
        L = 85.05112878
        x = 2**(z+7)*(lon/180.0+1.0)
        y = 2**(z+7)/np.pi*(-np.arctanh(np.sin(np.pi/180.0*lat)) + np.arctanh(np.sin(np.pi/180.0*L)))
    
    # set tile number
        Xt, Yt = int(x//256), int(y//256)
    # set pixle number per tile
        Xp, Yp = int(x%256), int(y%256)
        
        key = str(Xt) + '-' + str(Yt)
        url = self.url + str(z) + "/" + str(Xt) + "/" + str(Yt) + ".txt"
        if key in self.demdf:
            df = self.demdf[key]
            return df.iloc[Yp, Xp]
        else:
            # add url error works
            req = urllib.request.Request(urllib)
            try:
                df = pd.read_csv(url, header=None)
                self.demdf[key] = df     
                return df.iloc[Yp, Xp]
            except urllib.error.HTTPError as error:
                return 'outside'
            except urllib.error.URLError as error:
                return 'outside'
            
    def __del__(self):
        del self.demdf

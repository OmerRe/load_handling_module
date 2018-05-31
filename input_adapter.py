# def fill(**kwargs):
#     for line in range(0,6):
#         # fill_to.loc[line,'device_sn'] = he_num
#         kwargs['fill_to'].loc[line,'gps_lat'] = kwargs['fill_from'].loc[line,'gps_lat']
#         kwargs['fill_to'].loc[line,'gps_lon'] = kwargs['fill_from'].loc[line,'gps_lon']
#         kwargs['fill_to'].loc[line,'gps_alt'] = kwargs['fill_from'].loc[line,'gps_alt']
#         kwargs['fill_to'].loc[line,'bmp_alt'] = kwargs['fill_from'].loc[line,'bmp_alt']
#         kwargs['fill_to'].loc[line,'bmp_tmp'] = kwargs['fill_from'].loc[line,'bmp_tmp']
#         kwargs['fill_to'].loc[line,'acc_ax'] = kwargs['fill_from'].loc[line,'acc_ax']
#         kwargs['fill_to'].loc[line,'acc_ay'] = kwargs['fill_from'].loc[line,'acc_ay']
#         kwargs['fill_to'].loc[line,'acc_az'] = kwargs['fill_from'].loc[line,'acc_az']
#         kwargs['fill_to'].loc[line,'weight'] = kwargs['fill_from'].loc[line,'weight']
#         kwargs['fill_to'].loc[line,'event_timestamp'] = kwargs['t']
#         kwargs['fill_to'].loc[line,'mtlb'] = kwargs['mtlb']
#         # kwargs['fill_to'].loc[line,'image_url'] = fill_from.loc[line,'image_url']
#         kwargs['mtlb']=kwargs['mtlb']+1
#         kwargs['t']=kwargs['t']+1
#     kwargs['fill_to'].fillna(0, inplace=True)
import time

class InputAdapter:
    mtlb = 1
    t=int(time.time())
    def __init__(self, fill_to):
        self.fill_to = fill_to

    def fill(self , fill_from):
        for line in range(0,7):
            self.fill_to.loc[line,'gps_lat'] = fill_from.loc[line,'gps_lat']
            self.fill_to.loc[line,'gps_lon'] = fill_from.loc[line,'gps_lon']
            self.fill_to.loc[line,'gps_alt'] = fill_from.loc[line,'gps_alt']
            self.fill_to.loc[line,'bmp_alt'] = fill_from.loc[line,'bmp_alt']
            self.fill_to.loc[line,'bmp_tmp'] = fill_from.loc[line,'bmp_tmp']
            self.fill_to.loc[line,'acc_ax'] = fill_from.loc[line,'acc_ax']
            self.fill_to.loc[line,'acc_ay'] = fill_from.loc[line,'acc_ay']
            self.fill_to.loc[line,'acc_az'] = fill_from.loc[line,'acc_az']
            self.fill_to.loc[line,'weight'] = fill_from.loc[line,'weight']
            self.fill_to.loc[line,'event_timestamp'] = self.t
            self.fill_to.loc[line,'mtlb'] = self.mtlb
            self.fill_to.loc[line,'device_sn'] = fill_from.loc[line,'device_sn'][6]
            self.fill_to.loc[line,'image_url'] = fill_from.loc[line,'image_url']
            self.mtlb=self.mtlb+1
            self.t=self.t+1


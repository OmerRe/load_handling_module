import sys
from astropy.table import Table, Column
import numpy as np
import pandas as pd
from input_adapter import InputAdapter
import time
from data_smoother import smooth_weight, smooth_gps, smooth_acc

he_num = 1
run_id=1
##  Import Data
# % try
#     conn = database('vndb','vndbroot','AkuoKfo321!','Vendor','MySQL','Server','vnmysql.c4a62i7b81an.us-east-2.rds.amazonaws.com');
#     conn.Message
# % catch err
# %     system(['C:\Users\Administrator\Desktop\AG_Modules_Production\RawData_Filter_HE' num2str(he_num) '.exe &']);
# % end
# % [~,metadata] = select(conn,sqlquery);
# sqlquery = ['select * from lhm_tc_status where mtlb=(select max(mtlb) from lhm_tc_status where device_sn = ' num2str(he_num) ')'];
# [data_mtlb,~] = select(conn,sqlquery); %,'MaxRows',3)
data = pd.read_csv('C:\\Users\\omerc\\Desktop\\raw_he1_mar26.csv')

# mtlb=data_mtlb.mtlb+1;
# run_id=data_mtlb.module_run_id+1;
RawDataTable_RT = pd.DataFrame(np.nan, index=[0],columns=['mtlb','device_sn','event_timestamp','gps_lat','gps_lon','gps_alt','bmp_alt','bmp_tmp','acc_ax','acc_ay','acc_az','weight','image_url'])
LTP_X_SummaryTable_RT = pd.DataFrame([],columns=['Customer_ID','Site_ID','VN_Module_ID','VN_HE_ID','LTPX_Id','LTPX_Start','LTPX_End','LTPX_DateStart','LTPX_DateEnd','LTPX_Duration','LTPX_LoadAccessoryID','LTPX_LoadAccessoryNomWeight','LTPX_LoadID','LTPX_LoadNomWeight','LTPX_LocationStartLon','LTPX_LocationStartLan','LTPX_LocationStartAlt','LTPX_LocationEndLon','LTPX_LocationEndLan','LTPX_LocationEndAlt','LTPX_MotionWithLoad','LTPX_MotionWithoutLoad','LTPX_IdleWithLoad','LTPX_IdleWithoutLoad','LTPX_DurationWithLoad','LTPX_DurationWithoutLoad','LTPX_IdleTimeWaste','LTPX_IdleTimeWasteVsDuration_Ratio','LTPX_WeightLegality','LTPX_AreaStart','LTPX_AreaEnd','LTPX_ValuableAreaValidation','LTPX_CraneUtilization'])
Status_Table = pd.DataFrame(np.nan, index=[0], columns=['mtlb','module_run_id','device_sn','event_timestamp','gps_lat','gps_lon','gps_alt','bmp_alt','bmp_tmp','acc_ax','acc_ay','acc_az','weight','module_step_id','crane_motion_status','crane_motion_status_continual','crane_motion_status_accumulative'])
SmoothedRawDataTable_RT = pd.DataFrame([],columns=['mtlb','device_sn','event_timestamp','gps_lat','gps_lon','gps_alt','bmp_alt','bmp_tmp','acc_ax','acc_ay','acc_az','weight','image_url'])

count_delay=0
inputAdapter = InputAdapter(RawDataTable_RT)
inputAdapter.fill(data)
RawDataTable_RT.fillna(0, inplace=True)


#fill(fill_from=data, fill_to=RawDataTable_RT, t=0, mtlb=mtlb )
#
COUNT_ALERT=0
# formatOut = 'dd mmm yyyy, HH:MM:SS';
Status_Table.loc[1,'module_run_id'] = run_id
# Status_Table.device_sn(1)=RawDataTable_RT.device_sn(1);
# Status_Table.event_timestamp(1)=RawDataTable_RT.event_timestamp(1);
line=8
jj=2
# raw_he=cell(1);
if RawDataTable_RT.loc[1,'weight'] <= 90:
    Status_Table.loc[1,'module_step_id']=1
else:
    Status_Table.loc[1,'module_step_id']=3
RawDataTable_weight_temp = np.array (0)
# mtlb=RawDataTable_RT.mtlb(size(RawDataTable_RT,1))+1;
Status_Table.loc[1,'mtlb'] = RawDataTable_RT.loc[1,'mtlb']
#
# %% smooth weight
# % i=2;
# % win_weight=4;
# % while i<(size(RawDataTable,1)-1)
# %     if ((abs(RawDataTable.weight(i+1)-RawDataTable.weight(i-1))<win_weight)||(abs(RawDataTable.weight(i+2)-RawDataTable.weight(i-1))<win_weight))
# %         RawDataTable.weight(i)=RawDataTable.weight(i-1);
# %     end
# %     i=i+1;
# % end
#
while(1):
    if LTP_X_SummaryTable_RT.empty:
#          LTP_X_Mode_Variables = {'LTPX_Id','LTPX_LoadType','LTPX_WeightChangeMode','LTPX_LonChangeMode','LTPX_LanChangeMode','LTPX_AltChangeMode', 'LTPX_MotionStatus'};
#          LTP_X_Mode_Variables_Size_RT = size (LTP_X_Mode_Variables);
#          LTP_X_Initiate_Matrix_RT = zeros(size(RawDataTable_RT,1),LTP_X_Mode_Variables_Size_RT(2));
#          LTP_X_Mode_Table_RT = Create_LTPX_Mode_Tables (LTP_X_Initiate_Matrix_RT,LTP_X_Mode_Variables);% Get required tables for LTP_X
        LTP_X_Mode_Table_RT = pd.DataFrame(np.nan, index=[0],columns=['LTPX_Id','LTPX_LoadType','LTPX_WeightChangeMode','LTPX_LonChangeMode','LTPX_LanChangeMode','LTPX_AltChangeMode','LTPX_MotionStatus'])


#         AxonGo_FMEA_Variable1=struct('ID',1,'Function','GPS Data Fails Counter','Potential_Failure_Mode','TBD','Potential_Effect_of_Falure','TBD','Severity_Level',0,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','TBD','Detection_Level',0,'Risk_Profile_Number',0);
#         AxonGo_FMEA_Variable2=struct('ID',2,'Function','Dinanometer Data Fails','Potential_Failure_Mode','TBD','Potential_Effect_of_Falure','TBD','Severity_Level',0,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','TBD','Detection_Level',0,'Risk_Profile_Number',0);
#         AxonGo_FMEA_Variable3=struct('ID',3,'Function','TBD','Potential_Failure_Mode','TBD','Potential_Effect_of_Falure','TBD','Severity_Level',0,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','TBD','Detection_Level',0,'Risk_Profile_Number',0);
#         AxonGo_FMEA_Array_RT=[AxonGo_FMEA_Variable1, AxonGo_FMEA_Variable2, AxonGo_FMEA_Variable3];
#         AxonGo_FMEA_Table_RT=struct2table(AxonGo_FMEA_Array_RT); %return the FMEA table with required variables
#
#         % % Step 2.4.2 - LTP FMEA Table
#         % This table will manage the LTP process realted
#         % fails on the customer entities. For example, non relevatn load type, over
#         % duration, fail, collisions, etc. AxonGo platform will provide a health report based on this FMEA also
#         LTP_FMEA_Variable1=struct('ID',1.1,'Function','Track to Load','Potential_Failure_Mode','Crane Continious Idle Time','Potential_Effect_of_Falure','LTP Cycle Time','Severity_Level',5,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','Visual','Detection_Level',9,'Risk_Profile_Number',0);
#         LTP_FMEA_Variable2=struct('ID',2.1,'Function','Load Banding','Potential_Failure_Mode','TBD','Potential_Effect_of_Falure','TBD','Severity_Level',9,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','No detection','Detection_Level',10,'Risk_Profile_Number',0);
#         LTP_FMEA_Variable3=struct('ID',3.1,'Function','Load Conveying','Potential_Failure_Mode','Crane Idle Time','Potential_Effect_of_Falure','LTP Cycle Time','Severity_Level',5,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','Visual','Detection_Level',9,'Risk_Profile_Number',0);
#         LTP_FMEA_Variable4=struct('ID',3.2,'Function','Load Conveying','Potential_Failure_Mode','Load Fall','Potential_Effect_of_Falure','People Ingury; Material Costs;LTP Cycle Time','Severity_Level',10,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','Visual','Detection_Level',9,'Risk_Profile_Number',0);
#         LTP_FMEA_Variable5=struct('ID',3.3,'Function','Load Conveying','Potential_Failure_Mode','Non Legal Weight Convey','Potential_Effect_of_Falure','Building Speed','Severity_Level',10,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','Visual','Detection_Level',9,'Risk_Profile_Number',0);
#         LTP_FMEA_Variable6=struct('ID',4.1,'Function','Load Unbanding','Potential_Failure_Mode','TBD','Potential_Effect_of_Falure','TBD','Severity_Level',9,'Potential_Causes_of_Fail','TBD','Occurance_Level',0,'Current_Controls','No detection','Detection_Level',10,'Risk_Profile_Number',0);
#         LTP_FMEA_Array_RT=[LTP_FMEA_Variable1,LTP_FMEA_Variable2,LTP_FMEA_Variable3,LTP_FMEA_Variable4,LTP_FMEA_Variable5,LTP_FMEA_Variable6];
#         LTP_FMEA_Table_RT=struct2table(LTP_FMEA_Array_RT); %return the FMEA table with required variables
#
#         % % Step 2.4.3 - LTP FMEA RPN Ratings
#         % This table have to be defined to rate the RPN as desided by customers.
#         % Here it is defined by VN CSO judgement
#         LTP_FMEA_RPNRate_Variable1=struct('RPN_Level',10,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable2=struct('RPN_Level',9,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable3=struct('RPN_Level',8,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable4=struct('RPN_Level',7,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable5=struct('RPN_Level',6,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable6=struct('RPN_Level',5,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable7=struct('RPN_Level',4,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable8=struct('RPN_Level',3,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable9=struct('RPN_Level',2,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Variable10=struct('RPN_Level',1,'Severity_Level_Description','TBD','Occurance_Level_Description','TBD','Detectability_Level_Description','TBD');
#         LTP_FMEA_RPNRate_Array_RT=[LTP_FMEA_RPNRate_Variable1,LTP_FMEA_RPNRate_Variable2,LTP_FMEA_RPNRate_Variable3,LTP_FMEA_RPNRate_Variable4,LTP_FMEA_RPNRate_Variable5,LTP_FMEA_RPNRate_Variable6,LTP_FMEA_RPNRate_Variable7,LTP_FMEA_RPNRate_Variable8,LTP_FMEA_RPNRate_Variable9,LTP_FMEA_RPNRate_Variable10];
#         LTP_FMEA_RPNRate_Table_RT=struct2table(LTP_FMEA_RPNRate_Array_RT);
#
#         % % Step 2.5 - Control Tables
#
#         % % Step 2.5.1 - LTP Process Control Table
#         % This table will manage the LTP process realted
#         % fails on the customer entities. For example, non relevatn load type, over
#         % duration, fail, collisions, etc. AxonGo platform will provide a health report based on this FMEA also
#         LTP_CotrolTable_Variable1=struct('ID',1,'Parameter_Name','Crane Continious Idle Time [Fails Counts]','Parameter_Value',0,'LDL','N.A.','LCL','N.A.','Target','N.A.','UCL',30,'UDL',60);
#         LTP_CotrolTable_Variable2=struct('ID',2,'Parameter_Name','Crane Continious Idle Time [Successes Counts]','Parameter_Value',0,'LDL','N.A.','LCL','N.A.','Target','N.A.','UCL',30,'UDL',60);
#         LTP_CotrolTable_Variable3=struct('ID',3,'Parameter_Name','Load Weight Legality [Fails Counts]','Parameter_Value',0,'LDL','N.A.','LCL','N.A.','Target','N.A.','UCL','N.A.','UDL',100);
#         LTP_CotrolTable_Variable4=struct('ID',4,'Parameter_Name','Load Weight Legality [Success Counts]','Parameter_Value',0,'LDL','N.A.','LCL','N.A.','Target','N.A.','UCL','N.A.','UDL',100);
#         LTP_ControlTable_Array_RT=[LTP_CotrolTable_Variable1, LTP_CotrolTable_Variable2, LTP_CotrolTable_Variable3, LTP_CotrolTable_Variable4];
#         LTP_Control_Table_RT=struct2table(LTP_ControlTable_Array_RT);%return the Control table with required variables
#
#         % % Step 2.5.2 - AxonGo Control Table
#         % This table will manage the LTP process realted
#         % fails on the customer entities. For example, non relevatn load type, over
#         % duration, fail, collisions, etc. AxonGo platform will provide a health report based on this FMEA also
#         AxonGo_CotrolTable_Variable1=struct('ID',1,'Parameter_Name','GPS Data Fails Counter','Parameter_Value',0,'LDL',0,'LCL',0,'Target',0,'UCL',0,'UDL',0);
#         AxonGo_CotrolTable_Variable2=struct('ID',2,'Parameter_Name','Dinanometer Data Fails','Parameter_Value',0,'LDL',0,'LCL',0,'Target',0,'UCL',0,'UDL',0);AxonGo_FMEA_Array_RT=[AxonGo_FMEA_Variable1, AxonGo_FMEA_Variable2];
#         AxonGo_ControlTable_Array_RT=[AxonGo_CotrolTable_Variable1, AxonGo_CotrolTable_Variable2];
#         AxonGo_Control_Table_RT=struct2table(AxonGo_ControlTable_Array_RT);%return the FMEA table with required variables
#

    if SmoothedRawDataTable_RT.empty:
        for i in range(1,6):
            weight_SR=4
            gps_lon_SR=4
            gps_lat_SR=4
            gps_alt_SR=4
            HE_Acc_SR=4
            if  ((RawDataTable_RT.loc[i,'gps_lon']==0) & (RawDataTable_RT.loc[i,'gps_lat']==0) & (RawDataTable_RT.loc[i,'gps_alt']==0)):
                RawDataTable_RT.loc[i,'gps_lon'] = RawDataTable_RT.loc[i-1,'gps_lon']
                RawDataTable_RT.loc[i,'gps_lat'] = RawDataTable_RT.loc[i-1,'gps_lat']
                RawDataTable_RT.loc[i,'gps_alt'] = RawDataTable_RT.loc[i-1,'gps_alt']

            if  i>=weight_SR:  # number of point to start from (if SR=4, we will start smooth from point 5)
                RawDataTable_weight_temp = np.append(RawDataTable_weight_temp,RawDataTable_RT.loc[i,'weight'])
                WeightData2Smooth = np.array([RawDataTable_RT.loc[i-4,'weight'],RawDataTable_RT.loc[i-3,'weight'],RawDataTable_RT.loc[i-2,'weight'],RawDataTable_RT.loc[i-1,'weight'],RawDataTable_RT.loc[i,'weight']])
                SmoothedRawDataTable_RT.loc[i-3,'weight'] = smooth_weight(WeightData2Smooth)

            if i>=gps_lon_SR:  # number of point to start from (if SR=4, we will start smooth from point 5)
                LonData2Smooth = np.array([RawDataTable_RT.loc[i-4,'gps_lon'],RawDataTable_RT.loc[i-3,'gps_lon'],RawDataTable_RT.loc[i-2,'gps_lon'],RawDataTable_RT.loc[i-1,'gps_lon'],RawDataTable_RT.loc[i,'gps_lon']])
                SmoothedRawDataTable_RT.loc[i-3,'gps_lon']= smooth_gps(LonData2Smooth)

            if i>=gps_lat_SR:  # number of point to start from (if SR=4, we will start smooth from point 5)
                LatData2Smooth = np.array([RawDataTable_RT.loc[i-4,'gps_lat'],RawDataTable_RT.loc[i-3,'gps_lat'],RawDataTable_RT.loc[i-2,'gps_lat'],RawDataTable_RT.loc[i-1,'gps_lat'],RawDataTable_RT.loc[i,'gps_lat']])
                SmoothedRawDataTable_RT.loc[i-3,'gps_lat']= smooth_gps(LatData2Smooth)

            if i>=gps_alt_SR:  # number of point to start from (if SR=4, we will start smooth from point 5)
                altData2Smooth = np.array([RawDataTable_RT.loc[i-4,'gps_alt'],RawDataTable_RT.loc[i-3,'gps_alt'],RawDataTable_RT.loc[i-2,'gps_alt'],RawDataTable_RT.loc[i-1,'gps_alt'],RawDataTable_RT.loc[i,'gps_alt']])
                SmoothedRawDataTable_RT.loc[i-3,'gps_alt']= smooth_gps(altData2Smooth)

            if i>=HE_Acc_SR: # number of point to start frome (if SR=4, we will start smooth from point 5)
                AcceleratorData2Smooth_x = np.array([RawDataTable_RT.loc[i-4,'acc_ax'],RawDataTable_RT.loc[i-3,'acc_ax'],RawDataTable_RT.loc[i-2,'acc_ax'],RawDataTable_RT.loc[i-1,'acc_ax'],RawDataTable_RT.loc[i,'acc_ax']])
                SmoothedRawDataTable_RT.loc[i-3,'acc_ax']= smooth_acc(AcceleratorData2Smooth_x)

            if i>=HE_Acc_SR: # number of point to start frome (if SR=4, we will start smooth from point 5)
                AcceleratorData2Smooth_y = np.array([RawDataTable_RT.loc[i-4,'acc_ay'],RawDataTable_RT.loc[i-3,'acc_ay'],RawDataTable_RT.loc[i-2,'acc_ay'],RawDataTable_RT.loc[i-1,'acc_ay'],RawDataTable_RT.loc[i,'acc_ay']])
                SmoothedRawDataTable_RT.loc[i-3,'acc_ay']= smooth_acc(AcceleratorData2Smooth_y)

            if i>=HE_Acc_SR: # number of point to start frome (if SR=4, we will start smooth from point 5)
                AcceleratorData2Smooth_z = np.array([RawDataTable_RT.loc[i-4,'acc_az'],RawDataTable_RT.loc[i-3,'acc_az'],RawDataTable_RT.loc[i-2,'acc_az'],RawDataTable_RT.loc[i-1,'acc_az'],RawDataTable_RT.loc[i,'acc_az']])
                SmoothedRawDataTable_RT.loc[i-3,'acc_az']= smooth_acc(AcceleratorData2Smooth_z)


            if i>=4:
                SmoothedRawDataTable_RT.loc[i-3,'mtlb']=RawDataTable_RT.loc[i-3,'mtlb']
                SmoothedRawDataTable_RT.loc[i-3,'device_sn']=RawDataTable_RT.loc[i-3,'device_sn']
                SmoothedRawDataTable_RT.loc[i-3,'event_timestamp']=RawDataTable_RT.loc[i-3,'event_timestamp']
                Status_Table.loc[(i-3),'mtlb']=RawDataTable_RT.loc[(i-3),'mtlb']
                Status_Table.loc[(i-3),'device_sn']=SmoothedRawDataTable_RT.loc[i-3,'device_sn']

                Status_Table.loc[(i-3),'event_timestamp']=SmoothedRawDataTable_RT.loc[i-3,'event_timestamp']
                Status_Table.loc[(i-3),'gps_lat']=SmoothedRawDataTable_RT.loc[i-3,'gps_lat']
                Status_Table.loc[(i-3),'gps_lon']=SmoothedRawDataTable_RT.loc[i-3,'gps_lon']
                Status_Table.loc[(i-3),'gps_alt']=SmoothedRawDataTable_RT.loc[i-3,'gps_alt']
                Status_Table.loc[(i-3),'acc_ax']=SmoothedRawDataTable_RT.loc[i-3,'acc_ax']
                Status_Table.loc[(i-3),'acc_ay']=SmoothedRawDataTable_RT.loc[i-3,'acc_ay']
                Status_Table.loc[(i-3),'acc_az']=SmoothedRawDataTable_RT.loc[i-3,'acc_az']
                Status_Table.loc[(i-3),'weight']=SmoothedRawDataTable_RT.loc[i-3,'weight']
                Status_Table.loc[(i-3),'module_step_id']=Status_Table.loc[1,'module_step_id']
                Status_Table.loc[(i-3),'module_run_id']=Status_Table.loc[1,'module_run_id']


#     %%    RT fullfill
#     SmoothedRawDataTable_RT.mtlb(i-3)=RawDataTable_RT.mtlb(i-3);
#     SmoothedRawDataTable_RT.device_sn(i-3)=RawDataTable_RT.device_sn(i-3);
#     SmoothedRawDataTable_RT.event_timestamp(i-3)=RawDataTable_RT.event_timestamp(i-3);
#     % % For step 3.3.1
#     weight_SR=4; % SR - Smoother Rezolution (number of simple to weght till the beginning
#
#     % % For step 3.3.2
#     gps_lon_SR=4; % SR - Smoother Rezolution (number of simple to weght till the beginning
#
#     % % For step 3.3.3
#     gps_lat_SR=4; % SR - Smoother Rezolution (number of simple to weght till the beginning
#
#     % % For step 3.3.4
#     gps_alt_SR=4; % SR - Smoother Rezolution (number of simple to weght till the beginning
#
#     % % For step 3.3.5
#     HE_Accellerator_SR=4; % SR - Smoother Rezolution (number of simple to weght till the beginning
#
#     % % Main real time block
#     %         while i<=RawDataTable_Size_RT(1) % Symulate the real time data run, where the the column #1 size describes number fo lines in the table
#     %           if i>4
#     % % Step 3.2 - Imporvement ot the data health (data reilability control and real time imporvement)
#
#     % % Step 3.2.1 - Data Relaibility Validation and Correction by "Doctor Data"(future feature)
#     % In this step data reailabilty will be verified ongoing vs success
#     % criteria, correction will be done immidiatelly in a retrospective mode.
#     % Each time the problsm will appear, the even will be counted and
#     % inclding into AxonGo_FMEA_Table. Once more then 3 seconds data flow will
#     % not appear, AxonGo will stop and alert with eror message id that is equal
#     % to AxonGo_FMEA_Variable ID.
#     if ((RawDataTable_RT.gps_lon(i)==0) && (RawDataTable_RT.gps_lat(i)==0) && (RawDataTable_RT.gps_alt(i)==0))
#         %Verify vs FMEA success criteria:
#         AxonGo_Control_Table_RT.Parameter_Value(1)=AxonGo_Control_Table_RT.Parameter_Value(1)+1;
#         % Update by new data:
#         RawDataTable_RT.gps_lon(i)=RawDataTable_RT.gps_lon(i-1);
#         RawDataTable_RT.gps_lat(i)=RawDataTable_RT.gps_lat(i-1);
#         RawDataTable_RT.gps_alt(i)=RawDataTable_RT.gps_alt(i-1);
#         % Update AxonGo_FMEA_Table per need
#         % Currently Fails is in case there are 3 continious bins fails happend
#         if AxonGo_Control_Table_RT.Parameter_Value(1)>AxonGo_Control_Table_RT.UCL(1)
#             AxonGo_FMEA_Table_RT.Occurance_Level(1)=AxonGo_FMEA_Table_RT.Occurance_Level(1)+1;
#             AxonGo_Control_Table_RT.Parameter_Value(1)=0;
#         end
#     elseif ((RawDataTable_RT.weight(i)==0) && (LTP_X_SummaryTable_RT.LTPX_Id(1)>0))
#         AxonGo_Control_Table_RT.Parameter_Value(2)=AxonGo_Control_Table_RT.Parameter_Value(2)+1;
#         % Update by new data:
# %         RawDataTable_RT.weight(i)=RawDataTable_RT.weight(i-1);
#         % Update AxonGo_FMEA_Table per need
#         % Currently Fails is in case there are 3 continious bins fails happend
#         if AxonGo_Control_Table_RT.Parameter_Value(2)==AxonGo_Control_Table_RT.UCL(2)
#             AxonGo_FMEA_Table_RT.Occurance_Level(2)=AxonGo_FMEA_Table_RT.Occurance_Level(2)+1;
#             AxonGo_Control_Table_RT.Parameter_Value(2)=0;
#         end
#     end
#     % % Step 3.3 - Smoothness of data in a real time mode
#     % During this step the data should be smoothed and be prepaired for future and advanced analysis.
#     % % Step 3.3.1 - Smooth WEIGHT data in a realtime mode
#     % Decided to use our feature follwoing learnings of the KERNEL's model (Gaussian kernel)as a most teffective for this mission
#     if i>weight_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         RawDataTable_weight_temp(i)= median(RawDataTable_RT.weight(i-4:i));
#         WeightData2Smooth=table(RawDataTable_weight_temp(i-4),RawDataTable_weight_temp(i-3),RawDataTable_weight_temp(i-2),RawDataTable_weight_temp(i-1),RawDataTable_weight_temp(i));
#         SmoothedRawDataTable_RT.weight(i-3)= Weight_Data_Smoother(WeightData2Smooth);
#     end
#
#     % % Step 3.3.2 - Smooth Lon data in a realtime mode
#     % Decided to develope our own feature follwoing learnings of the KERNEL's model (Gaussian kernel)that is not that good for a realtime as a most teffective for this mission
#     if i>gps_lon_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         LonData2Smooth=table(RawDataTable_RT.gps_lon(i-4),RawDataTable_RT.gps_lon(i-3),RawDataTable_RT.gps_lon(i-2),RawDataTable_RT.gps_lon(i-1),RawDataTable_RT.gps_lon(i));
#         SmoothedRawDataTable_RT.gps_lon(i-3)= Lon_Data_Smoother(LonData2Smooth);
#     end
#
#     % % Step 3.3.3 - Smooth Lan data for in a realtime mode
#     if i>gps_lat_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         LanData2Smooth=table(RawDataTable_RT.gps_lat(i-4),RawDataTable_RT.gps_lat(i-3),RawDataTable_RT.gps_lat(i-2),RawDataTable_RT.gps_lat(i-1),RawDataTable_RT.gps_lat(i));
#         SmoothedRawDataTable_RT.gps_lat(i-3)= Lan_Data_Smoother(LanData2Smooth);
#     end
#
#     % % Step 3.3.4 - Smooth Alt data for in a realtime mode
#     if i>gps_alt_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         AltData2Smooth=table(RawDataTable_RT.gps_alt(i-4),RawDataTable_RT.gps_alt(i-3),RawDataTable_RT.gps_alt(i-2),RawDataTable_RT.gps_alt(i-1),RawDataTable_RT.gps_alt(i));
#         SmoothedRawDataTable_RT.gps_alt(i-3)= Alt_Data_Smoother(AltData2Smooth);
#     end
#
#     % % Step 3.3.5 - Smooth Accelerator data for in a realtime mode
#     if i>HE_Accellerator_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         AcceleratorData2Smooth_x=table(RawDataTable_RT.acc_ax(i-4),RawDataTable_RT.acc_ax(i-3),RawDataTable_RT.acc_ax(i-2),RawDataTable_RT.acc_ax(i-1),RawDataTable_RT.acc_ax(i));
#         SmoothedRawDataTable_RT.acc_ax(i-3)= Accelerator_Data_Smoother(AcceleratorData2Smooth_x);
#     end
#
#     if i>HE_Accellerator_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         AcceleratorData2Smooth_y=table(RawDataTable_RT.acc_ay(i-4),RawDataTable_RT.acc_ay(i-3),RawDataTable_RT.acc_ay(i-2),RawDataTable_RT.acc_ay(i-1),RawDataTable_RT.acc_ay(i));
#         SmoothedRawDataTable_RT.acc_ay(i-3)= Accelerator_Data_Smoother(AcceleratorData2Smooth_y);
#     end
#
#     if i>HE_Accellerator_SR % number of point to start frome (if SR=4, we will start smooth from point 5)
#         AcceleratorData2Smooth_z=table(RawDataTable_RT.acc_az(i-4),RawDataTable_RT.acc_az(i-3),RawDataTable_RT.acc_az(i-2),RawDataTable_RT.acc_az(i-1),RawDataTable_RT.acc_az(i));
#         SmoothedRawDataTable_RT.acc_az(i-3)= Accelerator_Data_Smoother(AcceleratorData2Smooth_z);
#     end
#     %             i=i+1; %Promote data counter by 1
#     %         end
#     %% Step 4 - LTPX Analysis Parameters Summary
#     % The mission of this step is to summarize end to end all LTPX related parameters.
#
#     % % Step 4.1 - Preliminary settings for following steps
#     % % Step 4.1.1 - For general loop
#     if ~(LTP_X_SummaryTable_RT.LTPX_Start(1))
#         n=4; %Realtime promoter, that will move by 1 (the resolution sensitivitiy)stop once RawDataTable lengnt will reach maximun value of the RawDataTable
#         % % Step 4.1.2 - LTPX Feedback Sensitivity level
#         %         FBsens_default=3; %fbsens - feedback sesitivity level (hoe many bins the back will be analyzed
#         %         FFsens_default=3;
#         %         i=i+FFsens_default; %promote i by fbsens level to start analysis
#         % !!! Note: The fbsesn may be unique to each sensor, where there is an importance to Step 4.1.3 - LTP_X_Summary Table Initiation
#         m=1;
#         %         SmoothedRawDataTable_RT=RawDataTable_RT;
#         LTP_X_SummaryTable_RT.LTPX_Id(m)=m;
#         LTP_X_SummaryTable_RT.LTPX_Start(m)=n;
#         LTP_X_SummaryTable_RT.LTPX_DateStart(m)=RawDataTable_RT.event_timestamp(n);%{RawDataTable_RT.event_timestamp(n)};
#         LTP_X_SummaryTable_RT.LTPX_LocationStartLon(m)=RawDataTable_RT.gps_lon(n);
#         LTP_X_SummaryTable_RT.LTPX_LocationStartLan(m)=RawDataTable_RT.gps_lat(n);
#         LTP_X_SummaryTable_RT.LTPX_LocationStartAlt(m)=RawDataTable_RT.gps_alt(n);
#     end
#     %     SmoothedRawDataTable_RT=RawDataTable_RT;
#     % Main real tyme block
#     % while i<=(RawDataTable_Size_RT(1)-5) % Symulate the real time data run, where the the column #1 size describes number fo lines in the table
#     % % Step 4.2 - LTPX Change Modes Calculation and Storage in LTPX_Mode_Table, where '-1'-Change Down, '0'-No Change, '1'-Change Up
#     % % Step 4.2.1 - LTPX Weight Sensor Analysis for changes
#     LTPX_Weight_WWMax=0.2; % Maximum working window
#     LTPX_Weight_WWMin=0.2; % Minimum working window
#     FBsens_default=3; %fbsens - feedback sesitivity level (hoe many bins the back will be analyzed
#     FFsens_default=3;
#     j=n-FBsens_default;
#     % Smoothed data to be transform into logaritmic scale. Motivations is
#     % to make the high value nambers more smoother and reduce the noise of
#     % resolution to lower level.
#     LTPX_Weight_WWMean=(log(SmoothedRawDataTable_RT.weight(j))+log(SmoothedRawDataTable_RT.weight(j+1))+log(SmoothedRawDataTable_RT.weight(j+2)))/3; % Baseline caclulation of 3 previous points
#     if (log(SmoothedRawDataTable_RT.weight(n))>(LTPX_Weight_WWMean+LTPX_Weight_WWMax)) && ((log(SmoothedRawDataTable_RT.weight(n))-log(SmoothedRawDataTable_RT.weight(n-1))>0.2)) %0.2 is a sensitivity level of the change between cloghted points to be less sensitive to point to point changes
#         LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=1; % i+1 is to put a step directly in the change start point. !!!NOTE: Need to do an adjustment during development, not relevant for POC
#     else
#         if (log(SmoothedRawDataTable_RT.weight(n))<(LTPX_Weight_WWMean-LTPX_Weight_WWMax) && ((log(SmoothedRawDataTable_RT.weight(n))-log(SmoothedRawDataTable_RT.weight(n-1)))<-0.2)) %5 is a sensitivity level of the change between cloghted points to be less sensitive to point to point changes
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=-1;
#         else
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=0;
#         end
#     end
#     % % Step 4.2.1.1 - Side Effect Improvement
#     % Due to noisy signal the side effect can appear, means within two bins
#     % same value may be. We're talking about 1 or -1 values only. 0's are
#     % OK, since they show us a stablization
#     if (LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)==0) && (LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-1)~=0)
#         k=1;
#         while LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-k)~=0
#             k=k+1;
#         end
#         if k>1
#             for j=1:1:k-2
#                 LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-j)=0;
#             end
#         end
#         % % Step 4.2.1.2 - Repeatbility phenomena optimization
#         % Due to noisy data and after step 4.2.1.2 some of point may be with
#         % same value 1 or -1 and closed to each other with a range of 3-4
#         % zeores. If pont are within this range it's possible to efford point
#         % form the right side ZEROS
#         l=0;
#         OptimalLimit=2;
#         while l<OptimalLimit %maximum limit of K point with zeros between to 1 or -1 values (to ignore infinity loop)
#             if LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-(j+2)-l)==0
#                 l=l+1;
#             else
#                 LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-(j+1))=0;
#                 l=OptimalLimit;
#             end
#         end
#     end
#
#     % % Step 4.2.2 - LTPX GPS Sensor analysis for changes
#     % In this step required for defintion of the motions along LTP and it's
#     % summary in LTPX_Mode_Teble where assignment shoudl be done per below:
#     % in lon, lan and alt if we have motion - 1, no motion - 0.
#     % Skip non relevant to motion data, for example in the
#     % beginning the GPS gives data even if HE is not installed. The data
#     % comes within error. Need to skip this kind of phenomena with while
#     % weight >0 due to accuracy.
#     % Caclulate 'motion mode up' - 1, 'motion mode down'- '-1' of
#     % 'stable mode' -0 for each GPS parameter
#     j=n-FBsens_default; % reset j
#
#     % % Step 4.2.2.1 - Motion Calculation for LON only
#     LTPX_Lon_WWMax=0.0015; % Maximum working window for Longtitude   %changed from 1.5
#     LTPX_Lon_WWMin=0.0015; % Minimum working window for Longtitude   %changed from 1.5
#     LTPX_Lon_StepSens=1;
#     LTPX_Lon_WWMean=(SmoothedRawDataTable_RT.gps_lon(j)+SmoothedRawDataTable_RT.gps_lon(j+1)+SmoothedRawDataTable_RT.gps_lon(j+2))/3;    % Baseline caclulation of 3 previous points
#     LTPX_Lon_Delta=SmoothedRawDataTable_RT.gps_lon(n)-SmoothedRawDataTable_RT.gps_lon(n-1);
#     if (SmoothedRawDataTable_RT.gps_lon(n)>(LTPX_Lon_WWMean+LTPX_Lon_WWMax)) % && (abs(LTPX_Lon_Delta)>LTPX_Lon_StepSens)
#         LTP_X_Mode_Table_RT.LTPX_LonChangeMode(n)=1; % i+1 is to put a step directly in the change start point. !!!NOTE: Need to do an adjustment during development, not relevant for POC
#     else
#         if (SmoothedRawDataTable_RT.gps_lon(n)<(LTPX_Lon_WWMean-LTPX_Lon_WWMin)) % && (abs(LTPX_Lon_Delta)>LTPX_Lon_StepSens)
#             LTP_X_Mode_Table_RT.LTPX_LonChangeMode(n)=-1;
#         else
#             LTP_X_Mode_Table_RT.LTPX_LonChangeMode(n)=0;
#         end
#     end
#
#     % % Step 4.2.2.2 - Motion Caclulation for LAN only
#     LTPX_Lan_WWMax=0.0015; % Maximum working window for Langtitude  %change from 1.5
#     LTPX_Lan_WWMin=0.0015; % Minimum working window for Langtitude  %change from 1.5
#     LTPX_Lan_StepSens=2; %Sensitivity of change bin to bin
#     LTPX_Lan_WWMean=(SmoothedRawDataTable_RT.gps_lat(j)+SmoothedRawDataTable_RT.gps_lat(j+1)+SmoothedRawDataTable_RT.gps_lat(j+2))/3;    % Baseline caclulation of 3 previous points
#     LTPX_Lan_Delta=SmoothedRawDataTable_RT.gps_lat(n)-SmoothedRawDataTable_RT.gps_lat(n-1);
#     if (SmoothedRawDataTable_RT.gps_lat(n)>(LTPX_Lan_WWMean+LTPX_Lan_WWMax)) % && (abs(LTPX_Lan_Delta)>LTPX_Lan_StepSens)
#         LTP_X_Mode_Table_RT.LTPX_LanChangeMode(n)=1; % i+1 is to put a step directly in the change start point. !!!NOTE: Need to do an adjustment during development, not relevant for POC
#     else
#         if (SmoothedRawDataTable_RT.gps_lat(n)<(LTPX_Lan_WWMean-LTPX_Lan_WWMin)) % && (abs(LTPX_Lon_Delta)>LTPX_Lon_StepSens)
#             LTP_X_Mode_Table_RT.LTPX_LanChangeMode(n)=-1;
#         else
#             LTP_X_Mode_Table_RT.LTPX_LanChangeMode(n)=0;
#         end
#     end
#
#
#     % % Step 4.2.2.3 - Motion Calculation for ALT only
#     LTPX_Alt_WWMax=1; % Maximum working window for Altgtitude  %change from 300
#     LTPX_Alt_WWMin=1; % Minimum working window for Altgtitude  %change from 300
#     LTPX_Alt_StepSens=350; %Sensitivity of change bin to bin
#     LTPX_Alt_WWMean=(SmoothedRawDataTable_RT.gps_alt(j)+SmoothedRawDataTable_RT.gps_alt(j+1)+SmoothedRawDataTable_RT.gps_alt(j+2))/3;    % Baseline caclulation of 3 previous points
#     LTPX_Alt_Delta=SmoothedRawDataTable_RT.gps_alt(n)-SmoothedRawDataTable_RT.gps_alt(n-1);
#     if SmoothedRawDataTable_RT.gps_alt(n)>(LTPX_Alt_WWMean+LTPX_Alt_WWMax) % && (abs(LTPX_Lan_Delta)>LTPX_Lan_StepSens)
#         LTP_X_Mode_Table_RT.LTPX_AltChangeMode(n)=1; % i+1 is to put a step directly in the change start point. !!!NOTE: Need to do an adjustment during development, not relevant for POC
#     else
#         if (SmoothedRawDataTable_RT.gps_alt(n)<(LTPX_Alt_WWMean-LTPX_Alt_WWMin)) % && (abs(LTPX_Lon_Delta)>LTPX_Lon_StepSens)
#             LTP_X_Mode_Table_RT.LTPX_AltChangeMode(n)=-1;
#         else
#             LTP_X_Mode_Table_RT.LTPX_AltChangeMode(n)=0;
#         end
#     end
#
#     % % Step 4.2.3 - Crane Motion Analysis and Summary in real time mode
#     % Update of the events regarding high level analysis (not related directly to spesific LTP, but use LTP data for high level analysis)
#     % will be summarised in relevant tables. For example, all crane related events will be summarized in talble LTP.
#     % % Step 4.2.3.1 - Crane Motion caclulation
#
#     %     if RawDataTable.acc_ax(n)==RawDataTable.acc_ax(n-1)==RawDataTable.acc_ax(n-2)
#     if (LTP_X_Mode_Table_RT.LTPX_LonChangeMode(n)~=0) || (LTP_X_Mode_Table_RT.LTPX_LanChangeMode(n)~=0) || (LTP_X_Mode_Table_RT.LTPX_AltChangeMode(n)~=0)
#
#         Status_Table.crane_motion_status(n)=1;
#     else
#         Status_Table.crane_motion_status(n)=0;
#     end
#
#     % % Step 4.2.3.2 - Motion Duration Calculation for Crane
#     if (Status_Table.crane_motion_status(n-1)==Status_Table.crane_motion_status(n))
#         if Status_Table.crane_motion_status(n)==0
#             Status_Table.crane_motion_status_continual(n)=Status_Table.crane_motion_status_continual(n-1)+1;
#         end
#         if Status_Table.crane_motion_status(n)==1
#             Status_Table.crane_motion_status_continual(n)=Status_Table.crane_motion_status_continual(n-1)+1;
#         end
#     else
#         % % Step 4.2.3.2.1 - Validate vs control table and count fails per criteria
#         if Status_Table.crane_motion_status(n-1)==0
#             if Status_Table.crane_motion_status_continual(n-1)>LTP_Control_Table_RT.UDL(1)
#                 LTP_Control_Table_RT.Parameter_Value(1)=LTP_Control_Table_RT.Parameter_Value(1)+1;
#             else
#                 LTP_Control_Table_RT.Parameter_Value(2)=LTP_Control_Table_RT.Parameter_Value(2)+1;
#             end
#         end
#     end
#
#     % % Step 4.3 - LTPX Camera Data analysis for changes
#     % This step is required to analyse camera data an update LTP_X mode talble on by relevant data.
#     % % Step 4.3.1 - LTPX Load Type Recognition
#     % !!!Note: Currently is not real and using sensors analysis for load
#     % type recognition. however, fucntion realated to camera aoutput will
#     % be analysed leter with relevant function.
#     Weight_Temp=SmoothedRawDataTable_RT.weight(n);
#     if  std(SmoothedRawDataTable_RT.weight(n-3:n))>7
#         LTP_X_Mode_Table_RT.LTPX_LoadType(n)=Get_Load_Type(Weight_Temp,base);
#     else
#         LTP_X_Mode_Table_RT.LTPX_LoadType(n) = LTP_X_Mode_Table_RT.LTPX_LoadType(n-1);
#     end
#
#
#     % % Step 4.3.1 - Load detection errors and correction
#     % Error may appear due to sensor unstablilty or mode of operation
#     % related issues. For example: worker may have impact on dinamometer
#     % during load banding, that will come in account as single change
#     % phenomena within in number of bins. This blok is looking back back
#     % within defalult sensititvity level and correcting to reqiured laod
#     % type errors
#     k=0;
#     l=0;
#     for j=1:1:(FBsens_default-1)
#         if (LTP_X_Mode_Table_RT.LTPX_LoadType(n)~=LTP_X_Mode_Table_RT.LTPX_LoadType(n-j))
#             k=k+1;
#         end
#         if (LTP_X_Mode_Table_RT.LTPX_LoadType(n-j)==LTP_X_Mode_Table_RT.LTPX_LoadType(n-j-1))
#             l=l+1;
#         end
#     end
#     if k>0 && k<FBsens_default-1 && l<FBsens_default-1
#         % Fix data
#         for j=1:1:k
#             LTP_X_Mode_Table_RT.LTPX_LoadType(n-j)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#         end
#     end
#
#     % % Step 4.3.2 - LoadType Vs WeightChageMode Alignment
#     k=0;
#     l=0;
#     for j=0:1:FBsens_default
#         % validate of alignment is required
#         if (LTP_X_Mode_Table_RT.LTPX_LoadType(n-j)~=LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-j))
#             k=k+1;
#         end
#         % remember where alignment is required
#         if (LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n-j)~=0)
#             l=j;
#         end
#     end
#     if l>0
#         for j=0:1:l
#             LTP_X_Mode_Table_RT.LTPX_LoadType(n-l)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#         end
#     end
#
#     % % Step 4.3.3 - WeightChageMode Vs LoadType Alignment
#     if (LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)~=LTP_X_Mode_Table_RT.LTPX_LoadType(n)) && (LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)==0)
#         % Define and update elevation where missing
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==0 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==1
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=1;
#         end
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==1 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==2
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=1;
#         end
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==0 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==2
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=1;
#         end
#         % Define and update reduction where missing
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==2 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==1
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=-1;
#         end
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==2 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==0
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=-1;
#         end
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n-1)==1 && LTP_X_Mode_Table_RT.LTPX_LoadType(n)==0
#             LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)=-1;
#         end
#     end
#
#     % % Step 4.4 - LPTX Start and End Detection
#     % This step is required to catch a start point of LTPX and End point of LTPX to summarize findings in LTP_X_SummaryTable
#     % 6 different states accure in this case when possibility is to
#     % elevate load without accessory (start), elevate load wtih accessory
#     % (start), elevate accessory (start), remove load by leave accessury
#     % (end), remove load without accessory (end), remove accessory (end).
#     % The loop below takes in account all 6 scenarios and update summary
#     % table per each scenario.
#
#
#     Status_Table.mtlb(n)=SmoothedRawDataTable_RT.mtlb(n);
#     Status_Table.device_sn(n)=SmoothedRawDataTable_RT.device_sn(n);
#     Status_Table.event_timestamp(n)=SmoothedRawDataTable_RT.event_timestamp(n);
#     Status_Table.gps_lat(n)=SmoothedRawDataTable_RT.gps_lat(n);
#     Status_Table.gps_lon(n)=SmoothedRawDataTable_RT.gps_lon(n);
#     Status_Table.gps_alt(n)=SmoothedRawDataTable_RT.gps_alt(n);
#     Status_Table.acc_ax(n)=SmoothedRawDataTable_RT.acc_ax(n);
#     Status_Table.acc_ay(n)=SmoothedRawDataTable_RT.acc_ay(n);
#     Status_Table.acc_az(n)=SmoothedRawDataTable_RT.acc_az(n);
#     Status_Table.weight(n)=SmoothedRawDataTable_RT.weight(n);
#     Status_Table.module_step_id(n)=Status_Table.module_step_id(n-1);
#     Status_Table.module_run_id(n)=Status_Table.module_run_id(n-1);
#
#     % % Step 4.4.1 - Weight elevation detected
#     if LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)==1
#         % define what kind of elevation is it (attached accessory or load)
#         % Step 4.4.1.1 - Accessory attached
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n)==1
#             LTP_X_SummaryTable_RT.LTPX_LoadAccessoryID(m)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#         end
#         % Step 4.4.1.2 - Load attached
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n)==2
#             LTP_X_SummaryTable_RT.LTPX_LoadID(m)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#             Status_Table.module_step_id(n)=3;
#         end
#     end
#
#
#     % % Step 4.4.2 - Weight reduction detected
#     if LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)==-1  && (Status_Table.weight(n-3)>base) % reduction detected% reduction detected
#         % % Step 4.4.2.1 - Load deattached
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n)==1 || LTP_X_Mode_Table_RT.LTPX_LoadType(n)==0
#             Status_Table.module_step_id(n)=1;
#             LTP_X_SummaryTable_RT.LTPX_LoadAccessoryID(m)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#             % % Step 4.4.2.1.1 - End of LTP_X and summary
#             LTP_X_SummaryTable_RT.LTPX_End(m)=n-1;
#             LTP_X_SummaryTable_RT.LTPX_DateEnd(m)=RawDataTable_RT.event_timestamp(n-1,:);%{RawDataTable_RT.event_timestamp(n-1,:)};
#             Start=LTP_X_SummaryTable_RT.LTPX_Start(m);
#             End=LTP_X_SummaryTable_RT.LTPX_End(m);
#             LTP_X_SummaryTable_RT.LTPX_Duration(m)=End-Start;
#             % Step 4.4.2.1.1.1 - Corect if duration is ZERO
#             % This phenomean appears usually due ot sinle pick
#             if LTP_X_SummaryTable_RT.LTPX_Duration(m)==0
#                 flag_Dur=1;
#                 LTP_X_SummaryTable_RT.LTPX_End(m-1)=LTP_X_SummaryTable_RT.LTPX_End(m);
#                 LTP_X_SummaryTable_RT.LTPX_End(m-1)=LTP_X_SummaryTable_RT.LTPX_End(m);
#                 m=m-1;
#                 Start=LTP_X_SummaryTable_RT.LTPX_Start(m);
#                 End=LTP_X_SummaryTable_RT.LTPX_End(m);
#                 LTP_X_SummaryTable_RT.LTPX_Duration(m)=End-Start;
#             end
#             % % Step 4.4.2.1.2 - Caclulate NominalWeight loaded along LTPX for both load and accessory
#             LoadNomWeight=LTPX_CalcLoadNomWeight(Start,End,LTP_X_Mode_Table_RT,SmoothedRawDataTable_RT);
#             AccessoryNomWeight=LTPX_CalcAccessoryNomWeight(Start,End,LTP_X_Mode_Table_RT,SmoothedRawDataTable_RT);
#             LTP_X_SummaryTable_RT.LTPX_LoadNomWeight(m)=LoadNomWeight-AccessoryNomWeight;
#             LTP_X_SummaryTable_RT.LTPX_LoadAccessoryNomWeight(m)=AccessoryNomWeight;
#             % % Step 4.4.2.1.2.1 - Validate and update if load is leagal (cranes are not alloud to elevate loads under 100 kg)
#             if LTP_X_SummaryTable_RT.LTPX_LoadNomWeight(m)<LTP_Control_Table_RT.UDL(3)
#                 LTP_X_SummaryTable_RT.LTPX_WeightLegality(m)=0;
#                 LTP_Control_Table_RT.Parameter_Value(3)=LTP_Control_Table_RT.Parameter_Value(3)+1;
#             else
#                 LTP_X_SummaryTable_RT.LTPX_WeightLegality(m)=1;
#                 LTP_Control_Table_RT.Parameter_Value(4)=LTP_Control_Table_RT.Parameter_Value(4)+1;
#             end
#             % % Step 4.4.2.1.3 - Update end location
#             LTP_X_SummaryTable_RT.LTPX_LocationEndLon(m)=SmoothedRawDataTable_RT.gps_lon(n-1);
#             LTP_X_SummaryTable_RT.LTPX_LocationEndLan(m)=SmoothedRawDataTable_RT.gps_lat(n-1);
#             LTP_X_SummaryTable_RT.LTPX_LocationEndAlt(m)=SmoothedRawDataTable_RT.gps_alt(n-1);
#             % % Step 4.4.2.1.4 - Caclulate motion with and whout load, idle with or without load
#             LTP_X_SummaryTable_RT.LTPX_MotionWithLoad(m)=CalcMotionWithLoad(Start,End,Status_Table,LTP_X_Mode_Table_RT);
#             LTP_X_SummaryTable_RT.LTPX_MotionWithoutLoad(m)=CalcMotionWithoutLoad(Start,End,Status_Table,LTP_X_Mode_Table_RT);
#             LTP_X_SummaryTable_RT.LTPX_IdleWithLoad(m)=CalcNoMotionWithLoad(Start,End,Status_Table,LTP_X_Mode_Table_RT);
#             LTP_X_SummaryTable_RT.LTPX_IdleWithoutLoad(m)=CalcNoMotionWithoutLoad(Start,End,Status_Table,LTP_X_Mode_Table_RT);
#             % % Step 4.4.2.1.5 - Caclulate Duration GoTo Load and Load Convery
#             % this cacluldation will add to the LTPX summary of the step
#             % GOTO LOAD (nncluding banding and unbanding) and LOAD CONVEY
#             % (when load is in the air and ot the way to destination)
#             LTP_X_SummaryTable_RT.LTPX_DurationWithLoad(m)=LTP_X_SummaryTable_RT.LTPX_MotionWithLoad(m)+LTP_X_SummaryTable_RT.LTPX_IdleWithLoad(m);
#             LTP_X_SummaryTable_RT.LTPX_DurationWithoutLoad(m)=LTP_X_SummaryTable_RT.LTPX_MotionWithoutLoad(m)+LTP_X_SummaryTable_RT.LTPX_IdleWithoutLoad(m);
#             % % Step 4.4.2.1.6 - Idle Vs Motion Ratio
#             Duration_Band=0; % time [sec] to band in avarage the premise according to empirical behavior
#             Duration_Unband=0; % time [sec] to unband in avarage the premise according to empirical behavior
#             LTP_X_SummaryTable_RT.LTPX_IdleTimeWaste(m)=LTP_X_SummaryTable_RT.LTPX_IdleWithLoad(m)+(LTP_X_SummaryTable_RT.LTPX_IdleWithoutLoad(m)-Duration_Unband-Duration_Band); % Waste due to idle time within each LTP
#             LTP_X_SummaryTable_RT.LTPX_IdleTimeWasteVsDuration_Ratio(m)=100*((LTP_X_SummaryTable_RT.LTPX_Duration(m)-LTP_X_SummaryTable_RT.LTPX_IdleTimeWaste(m))/LTP_X_SummaryTable_RT.LTPX_Duration(m)); % Persentage of idle time wastes within single LTP
#             % % Step 4.4.2.1.7 - CraneUtilization
#             LTP_X_SummaryTable_RT.LTPX_CraneUtilization(m)=LTP_X_SummaryTable_RT.LTPX_IdleTimeWasteVsDuration_Ratio(m);
#             % % Step 4.4.2.1.8 - Initiate next LTP
#             LTP_X_SummaryTable_RT.VN_HE_ID(m)=RawDataTable_RT.device_sn(m);
#             % add summery .exe function here
#             %             if ~(LTP_X_SummaryTable_RT.LTPX_Duration(m)==0)
#             %             system('C:\Users\omerc\Desktop\matlab_MCR\PI_Historical_Tableau_Ver_1\for_redistribution\application\PI_Historical_Tableau_Ver_1.exe &');
#             %                 % system('C:\Users\omerc\Desktop\matlab_tests\step1_test\application\step1_test.exe < EXIT.txt')
#             %             end
#             m=m+1;
#             LTP_X_SummaryTable_RT.LTPX_Id(m)=m;
#             LTP_X_SummaryTable_RT.LTPX_Start(m)=n;
#             LTP_X_SummaryTable_RT.LTPX_DateStart(m)=RawDataTable_RT.event_timestamp(n,:);%{RawDataTable_RT.event_timestamp(n,:)};
#             LTP_X_SummaryTable_RT.LTPX_LocationStartLon(m)=SmoothedRawDataTable_RT.gps_lon(n);
#             LTP_X_SummaryTable_RT.LTPX_LocationStartLan(m)=SmoothedRawDataTable_RT.gps_lat(n);
#             LTP_X_SummaryTable_RT.LTPX_LocationStartAlt(m)=SmoothedRawDataTable_RT.gps_alt(n);
#         end
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n)==2
#             LTP_X_SummaryTable_RT.LTPX_LoadID(m)=LTP_X_Mode_Table_RT.LTPX_LoadType(n);
#         end
#     end
#     t_calculate=toc(t_calculate);
#
#     if t_calculate>0.3
#         yourMsg = 'done calculate';
#         %  fid = fopen(fullfile('C:\Users\Administrator\Desktop', 'LogFile.txt'), 'a');
#         fid = fopen(fullfile('C:\Users\omerc\Documents\GitHub\Algo-mat', 'LogFile.txt'), 'a');
#         if fid == -1
#             error('Cannot open log file.');
#         end
#         fprintf(fid, '\n%s: %s, %f\n', datestr(now, 0), yourMsg,t_calculate );
#         fclose(fid);
#     end
#
#     %writing to SQL
#     %     t_write=tic;
#     %         status_rt_temp=table2array(Status_Table(n,:));
#     %
#     %         fastinsert(conn,'lhm_tc_status',LTP_Mode_Table_Variables,status_rt_temp);
#     %     t_write=toc(t_write);
#     %     if t_write>0.6
#     %         yourMsg = 'done writing';
#     % %         fid = fopen(fullfile('C:\Users\Administrator\Desktop', 'LogFile.txt'), 'a');
#     %         fid = fopen(fullfile('C:\Users\omerc\Desktop\New folder', 'LogFile.txt'), 'a');
#     %         if fid == -1
#     %             error('Cannot open log file.');
#     %         end
#     %         fprintf(fid, '\n%s: %s, %f\n', datestr(now, 0), yourMsg,t_write );
#     %         fclose(fid);
#     %
#     %     end
#
#     if LTP_X_Mode_Table_RT.LTPX_WeightChangeMode(n)==-1  && (Status_Table.weight(n-3)>base) % reduction detected% reduction detected
#         % % Step 4.4.2.1 - Load deattached
#         if LTP_X_Mode_Table_RT.LTPX_LoadType(n)==1 || LTP_X_Mode_Table_RT.LTPX_LoadType(n)==0
#             if ~(LTP_X_SummaryTable_RT.LTPX_Duration(m-1)<=2)
#                 if flag_Dur~=1
#                     Status_Table.module_run_id(n)=Status_Table.module_run_id(n)+1;
#                     javaaddpath('C:\Program Files\MATLAB\Jave_heap\jheapcl\MatlabGarbageCollector.jar')
#                     %                 Historical_RT_Test(Status_Table(find(Status_Table.module_run_id==Status_Table.module_run_id(n-1)),:),conn);
#                     %                 close(conn)
#                     jheapcl
#                     %                 conn = database('vndb','vndbroot','AkuoKfo321!','Vendor','MySQL','Server','vnmysql.c4a62i7b81an.us-east-2.rds.amazonaws.com');
#                     %                 system('C:\Users\omerc\Desktop\matlab_MCR\PI_Historical_Tableau_Ver_1\for_redistribution\application\PI_Historical_Tableau_Ver_1.exe &');
#                     % system('C:\Users\omerc\Desktop\matlab_tests\step1_test\application\step1_test.exe < EXIT.txt')
#                 end
#                 flag_Dur=0;
#             end
#         end
#     end
#
#     %send mail if idle time eqaul to 5 min
#     %     if ((Status_Table.crane_motion_status_continual(n)==4*300)&&(Status_Table.crane_motion_status(n)==0))        %idle time
#     %         %         sendolmail('omer.cohen@vnatures.net','Alert from HE1 - VN','Idle time is eqaul to 5 min');
#     %         idle_str=char(datestr((t-600+10800)/86400 + datenum(1970,1,1)));
#     %         sendgmmail('0528630921@glb.al','3206#ran.oren@vnatures.net#SA999I',['Crane ' num2str(crane_num) ' idle 10 minutes, from ' idle_str(13:17) '. ' char(RawDataTable_RT.image_url(n))]);   %Daniel Haled
#     %         sendgmmail('0528630921@glb.al','3206#ran.oren@vnatures.net#SA999I',[ ' ???? ' num2str(crane_num) ' ???? 10 ????, ??? ' idle_str(13:17) '. ' char(RawDataTable_RT.image_url(n))]);   %Daniel Haled
#     %
#     %         %         sendgmmail('0502166116@glb.al','3206#ran.oren@vnatures.net#SA999I','Crene no. 1: Idle time is eqaul to 20 minn');     %Danny Harmann
#     %             COUNT_ALERT=COUNT_ALERT+1;
#     %     end
#
#     if Status_Table.weight(n-1)<100 &&  Status_Table.weight(n-1)> 20
#         new_base_counter = new_base_counter+1;
#         if Status_Table.module_step_id(n) == 3 && new_base_counter>150
#             if std(Status_Table.weight(end-new_base_counter+5:end-5)) < 4
#                 base = min(base,max(Status_Table.weight(end-new_base_counter+10:end-10))+7);
#                 new_base_counter=0;
#             end
#         end
#     else
#         new_base_counter=0;
#         if (Status_Table.weight(n-1) == 0) || mod(line,13000)==0
#         base = 100;
#         end
#     end
#
#
#     if jj > size(raw_he,1)
#         %         count_delay=0;
#         % id_prev=data.id;
#         t_read=tic;
# %         sqlquery = ['SELECT * FROM hawkeye_rawdata where event_timestamp >  FROM_UNIXTIME(' num2str(t) ') and device_sn = "he0000' num2str(he_num) '"'...
# %             ' Order by event_timestamp'];
#         sqlquery = ['SELECT * FROM hawkeye_rawdata where event_timestamp >  FROM_UNIXTIME(' num2str(t) ') and event_timestamp < ''2018-05-21 15:56:47'' and device_sn = "he0000' num2str(he_num) '"'...
#           ' Order by event_timestamp'];
#         [data,~] = select(conn,sqlquery); %,'MaxRows',3)
#         t_read=toc(t_read);
#         if t_read>0.3
#             yourMsg = 'done reading';
#             %  fid = fopen(fullfile('C:\Users\Administrator\Desktop', 'LogFile.txt'), 'a');
#         fid = fopen(fullfile('C:\Users\omerc\Documents\GitHub\Algo-mat', 'LogFile.txt'), 'a');
#             if fid == -1
#                 error('Cannot open log file.');
#             end
#             fprintf(fid, '\n%s: %s, %f\n', datestr(now, 0), yourMsg,t_read );
#             fclose(fid);
#
#         end
#         jj=1;
#         % while(data.id==id_prev)
#         %     [data,~] = select(conn,sqlquery); %,'MaxRows',3)
#         % end
#         while isempty(data)
#             sqlquery = ['SELECT * FROM hawkeye_rawdata where event_timestamp >  FROM_UNIXTIME(' num2str(t) ') and device_sn = "he0000' num2str(he_num) '"'...
#                 ' Order by event_timestamp'];
#             data = select(conn,sqlquery);
# %             t_delay = datetime('now');
# %             t_delay= posixtime(t_delay)-10800;
# %             if abs((t_delay-t)) > 200
# %                 system(['C:\Users\Administrator\Desktop\AG_Modules_Production\RawData_Filter_HE' num2str(he_num) '.exe &']);
# %                 break
# %             end
#         end
#         %             count_delay=count_delay+1;
#         %             if count_delay==10
#         %                 t=t+1;
#         %                 count_delay=0;
#         %             end
#         %             sqlquery = ['SELECT * FROM hawkeye_rawdata where event_timestamp =  FROM_UNIXTIME(' num2str(t) ') and device_sn = "he0000' num2str(he_num) '"'...
#         %                 ' Order by event_timestamp'];
#         %             [data,~] = select(conn,sqlquery);
#
#         data_cell=table2cell(data);
#         Char_HE_ID= char(data_cell(:,2));
#         idx =find(str2num(Char_HE_ID(:,7))==he_num);
#         raw_he=cell(size(idx,1),size(data_cell,2));
#         raw_he(:,:)=data_cell(idx,:);
#         % if isempty(raw_he)
#         %     return;
#         % end
#     end
#     raw_he_num(1,1)=str2double(cell2mat(raw_he(jj,5)));
#     raw_he_num(1,2)=str2double(cell2mat(raw_he(jj,7)));
#     raw_he_num(1,3)=str2double(cell2mat(raw_he(jj,9)));
#     raw_he_num(1,4:7)=cell2mat(raw_he(jj,12:15));
#     raw_he_num(1,8:9)=cell2mat(raw_he(jj,10:11));
#     if isnan(raw_he_num(1,1))
# %         counter_gps_NotonCrane=counter_gps_NotonCrane+1;
#         raw_he_num(1,1)= RawDataTable_RT.gps_lat(line-1);
#         raw_he_num(1,2)= RawDataTable_RT.gps_lon (line-1);
#         raw_he_num(1,3)= RawDataTable_RT.gps_alt(line-1);
# %     else
# %         counter_gps_NotonCrane=0;
# %         flag_NotonCrane=0;
#     end
#     if isnan(raw_he_num(1,4))
#         raw_he_num(1,4)= RawDataTable_RT.acc_ax(line-1);
#         raw_he_num(1,5)= RawDataTable_RT.acc_ay(line-1);
#         raw_he_num(1,6)= RawDataTable_RT.acc_az(line-1);
#     end
#     if isnan(raw_he_num(1,7))
#         raw_he_num(1,7)= RawDataTable_RT.weight(line-1);
#     end
# %     if raw_he_num(1,7)==0
# %         counter_weight_NotonCrane=counter_weight_NotonCrane+1;
# %     else
# %         counter_weight_NotonCrane=0;
# %         flag_NotonCrane=0;
# %     end
#     he_id_char=char(raw_he(jj,2));
#     he_id_int=str2num(he_id_char(1,7));
#     RawDataTable_RT.mtlb(line) = mtlb;
#     RawDataTable_RT.event_timestamp(line) = t; %raw_he(jj,3);
#     RawDataTable_RT.weight(line) = raw_he_num(1,7);
#     RawDataTable_RT.gps_lon (line)= raw_he_num(1,2);
#     RawDataTable_RT.gps_lat(line) = raw_he_num(1,1);
#     RawDataTable_RT.gps_alt(line) = raw_he_num(1,3);
#     RawDataTable_RT.acc_ax(line) = raw_he_num(1,4);
#     RawDataTable_RT.acc_ay(line) = raw_he_num(1,5);
#     RawDataTable_RT.acc_az(line) = raw_he_num(1,6);
#     RawDataTable_RT.bmp_alt(line) = raw_he_num(1,8);
#     RawDataTable_RT.bmp_tmp(line) = raw_he_num(1,9);
#     RawDataTable_RT.device_sn(line) = he_id_int;
#     RawDataTable_RT.image_url(line) = raw_he(jj,16);
#     t_delay = datetime('now');
#     t_delay= posixtime(t_delay)-10800;
#     t_arrival = char(data.event_arrival_timestamp(jj))
#     b(n,1)=posixtime(datetime(t_arrival(1:19),'Format',formatOut));
#     if (t_delay-(posixtime(datetime(t_arrival(1:19),'Format',formatOut)))) > 250
# %         sendgmmail('0528630921@glb.al','3206#ran.oren@vnatures.net#SA999I', ['HE' num2str(he_num) ': Delay is above 5 min. Restart the system']);
# %         sendgmmail('omer.cohen@vnatures.net','VN', ['!!! HE' num2str(he_num) ': Delay is above 5 min. Restart the system. t_delay:' num2str(t_delay) ', t_arrival:' num2str(posixtime(datetime(t_arrival(1:19),'Format',formatOut)))]);
# %         system(['C:\Users\Administrator\Desktop\AG_Modules_Production\RawData_Filter_HE' num2str(he_num) '.exe &']);
# %         return
#     end
#     jj=jj+1;
#     line=line+1
#     mtlb=mtlb+1;
#     if mod(line,10)==0
#         jheapcl
#     end
#     t=t+1;
#     i=i+1;
#     n=n+1;
#         figure(1)
#         plot(1:n-1,Status_Table.crane_motion_status_continual(1:n-1))
#         hold on
#         plot(1:n-1,20*Status_Table.crane_motion_status(1:n-1))
#         figure(2)
#         plot(1:n-1,RawDataTable_RT.weight(1:n-1),'-o')
#         hold on
#         plot(1:n-1,SmoothedRawDataTable_RT.weight(1:n-1),'h')
#         ylabel('Weight');
#         figure(3)
#         plot(1:n-1,RawDataTable_RT.acc_ax(1:n-1),'b')
#         hold on
#         plot(1:n-1,RawDataTable_RT.acc_ay(1:n-1),'g')
#         plot(1:n-1,RawDataTable_RT.acc_az(1:n-1),'r')
#         figure(4)
#         plot(1:n-1,RawDataTable_RT.bmp_alt(1:n-1),'k')
#         hold on
#         plot(1:n-1,RawDataTable_RT.gps_alt(1:n-1),'g')
#         ylabel('Barometer Altitude');
#         try
#             if  ~isequal(RawDataTable_RT.image_url(line-1),RawDataTable_RT.image_url(line-2))
#                 im = imread(char(RawDataTable_RT.image_url(line-1)));
#                 figure(5)
#                 imshow(im,'InitialMagnification',200);
#             end
#         end
#         pause(0.001)
#
# %     if (counter_weight_NotonCrane > 800) && (counter_weight_NotonCrane > 800)
# %         flag_NotonCrane=1;
# %     end
#
#     RawDataTable_char_RT = char(datestr(t/86400 + datenum(1970,1,1)));
#     if isequal(RawDataTable_char_RT(13:20),'08:09:46')
#         writetable(Status_Table,'Status_Table_APR22_HE1.csv');
#         pause
#     end
#     %
#     % if isequal(RawDataTable_char_RT(n-1,15:19),'59:00')
#     %     save('Summary_historical_RT');
#     % end
#     % kk=kk+1
# end
# % end

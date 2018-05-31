import numpy as np

# smooth_weight
def smooth_weight( data ):
    #     smoothing loop
    j=0
    while (j<10): #define how smooth do we want our data to be (more counts, smoother data will be)
        mean1 = np.mean([data[0],data[1],data[2]])
        mean2 = np.mean([data[1],data[2],data[3]])
        mean3 = np.mean([data[2],data[3],data[4]])
        smoothed = np.mean([np.mean([mean1,mean2]),np.mean([mean3,mean2])])
        if(data[0]>smoothed):
            data[0]=data[0]-0.5*(data[0]-smoothed)
        elif (data[0]<smoothed):
            data[0]=data[0]+0.5*(smoothed-data[0])

        if(data[1]>smoothed):
            data[1]=data[1]-0.5*(data[1]-smoothed)
        elif (data[1]<smoothed):
            data[1]=data[1]+0.5*(smoothed-data[1])

        if(data[2]>smoothed):
            data[2]=data[2]-0.5*(data[2]-smoothed)
        elif (data[2]<smoothed):
            data[2]=data[2]+0.5*(smoothed-data[2])

        if(data[3]>smoothed):
            data[3]=data[3]-0.5*(data[3]-smoothed)
        elif (data[3]<smoothed):
            data[3]=data[3]+0.5*(smoothed-data[3])

        if(data[4]>smoothed):
            data[4]=data[4]-0.5*(data[4]-smoothed)
        elif (data[4]<smoothed):
            data[4]=data[4]+0.5*(smoothed-data[4])

        #     run smoothing algorithm again
        mean1 = np.mean([data[0],data[1],data[2]])
        mean2 = np.mean([data[1],data[2],data[3]])
        mean3 = np.mean([data[2],data[3],data[4]])
        smoothed = np.mean([np.mean([mean1,mean2]),np.mean([mean3,mean2])])
        j=j+1
    return smoothed


def smooth_gps( data ):
    j=0
    while (j<3): #define how smooth do we want our data to be (more counts, smoother data will be)
    # run avarage algorithm
        mean1 = np.mean([data[0],data[1],data[2]])
        mean2 = np.mean([data[1],data[2],data[3]])
        mean3 = np.mean([data[2],data[3],data[4]])
        smoothed = np.mean([np.mean([mean1,mean2]),np.mean([mean3,mean2])])
    # Move all data closer to running  avarage
        data[0] = (data[0] + smoothed)/2
        data[1] = (data[1] + smoothed)/2
        data[2] = (data[2] + smoothed)/2
        data[3] = (data[3] + smoothed)/2
        data[4] = (data[4] + smoothed)/2
        j=j+1
    return smoothed

def smooth_acc( data ):
    j=0
    while (j<3): #define how smooth do we want our data to be (more counts, smoother data will be)
    # run avarage algorithm
        mean1 = np.mean([data[0],data[1],data[2]])
        mean2 = np.mean([data[1],data[2],data[3]])
        mean3 = np.mean([data[2],data[3],data[4]])
        smoothed = np.mean([np.mean([mean1,mean2]),np.mean([mean3,mean2])])
    #    Move all data closer to running  avarage
        data[0] = (data[0] + smoothed)/2
        data[1] = (data[1] + smoothed)/2
        data[2] = (data[2] + smoothed)/2
        data[3] = (data[3] + smoothed)/2
        data[4] = (data[4] + smoothed)/2
        j=j+1
    return smoothed





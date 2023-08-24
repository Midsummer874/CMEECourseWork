#Import the required packages
from torch.utils.data import Dataset, DataLoader, Subset
from PIL import Image
import torch
import torchvision.transforms as transforms
from collections import defaultdict
import pandas as pd
import os
import collections
data=pd.read_excel('Copy of groupby_cp.xlsx')

dic_class_index={
'pre':0,'post':0,'control':1
}
value=data[['Original name','flower_id','pollination status','new_time_series']].values

#label corresponding to the flower id
dic_id_label=collections.defaultdict(list)
#Flower id corresponds to the image address of the flower
dic_id_name=collections.defaultdict(list)
dirname='segmentation/'
lst_path=os.listdir(dirname)
# for name in os.listdir(dirname):
#     lst_path.append(name[:-3])
print(lst_path)

for i in range(len(value)):
    if value[i][0]+'png' in lst_path:
        dic_id_label[value[i][1]].append(dic_class_index[value[i][2]])
        dic_id_name[value[i][1]].append(dirname+value[i][0]+'png')

print(dic_id_label)
print(dic_id_name)

lst_img_path=[]
lst_img_label=[]
for k in dic_id_name:
    lst_img_path.append(dic_id_name[k])
    lst_img_label.append(dic_id_label[k])
print(lst_img_path)
print(lst_img_label)

# sys.exit()
# seed=np.random.randint(1e9)
timesteps=4
h,w=224,224
mean=[0.485,0.456,0.406]
std=[0.229,0.224,0.225]
num_classes=2

test_transformer=transforms.Compose([
        transforms.Resize((h,w)),
        transforms.ToTensor(),
        transforms.Normalize(mean,std),
        ])



from torch import nn
from torchvision import models


#Modeling
class ResnetRnn(nn.Module):
    def __init__(self,params_model):
        super(ResnetRnn,self).__init__()
        num_classes=params_model["num_classes"]
        dr_rate=params_model["dr_rate"]
        pretrained=params_model["pretrained"]
        rnn_hidden_size=params_model["rnn_hidden_size"]
        rnn_num_layers=params_model["rnn_num_layers"]

        #The base model is resnet50
        baseModel=models.resnet50(pretrained=pretrained)
        num_features=baseModel.fc.in_features
        baseModel.fc=Identity()
        self.baseModel=baseModel
        #Prevent overfitting
        self.dropout=nn.Dropout(dr_rate)
        #Add LSTM model
        self.rnn=nn.LSTM(num_features,rnn_hidden_size,rnn_num_layers)
        self.fc1=nn.Linear(rnn_hidden_size, num_classes)
    def forward(self,x):
        # print(x.shape)
        # import sys
        # sys.exit()
        b_z,ts,c,h,w=x.shape
        # ts,c,h,w=x.shape
        # print(x.shape)
        # torch.Size([4, 3, 224, 224, 1])

        ii=0
        y=self.baseModel((x[:,ii]))
        output,(hn,cn)=self.rnn(y.unsqueeze(1))

        for ii in range(1,ts):
            y=self.baseModel((x[:,ii]))
            out,(hn,cn)=self.rnn(y.unsqueeze(1),(hn,cn))
        out=self.dropout(out[:,-1])
        # out=self.dropout(out)
        out=self.fc1(out)
        # print(out.shape)
        return out

class Identity(nn.Module):
    def __init__(self):
        super(Identity,self).__init__()
    def forward(self,x):
        return x

params_model={
    "num_classes":num_classes,
    "dr_rate":0.1,
    "pretrained":True,
    "rnn_num_layers":1,
    "rnn_hidden_size":100,
    }
model=ResnetRnn(params_model)

#Move the model to the GPU device
print(torch.cuda.is_available())
device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# model=model.to(device)

#Read the trained model weights
# model.load_state_dict(torch.load('best_model.pth'))
model.load_state_dict(torch.load('models/weights.pt'))
model = model.to(device)
model.eval()  #Set the model to evaluation mode

dic_true_num=defaultdict(int)
dic_sum_num=defaultdict(int)
for i in range(len(lst_img_path)):
    lst_path=lst_img_path[i]
    lst_label=lst_img_label[i]

    if 1 in lst_label:
        label = 1
    else:
        label = 0

    for j in range(len(lst_path)):
        lst_data=lst_path[:j+1]

        while len(lst_data) < timesteps:
            lst_data.append(lst_data[-1])

        lst_data = lst_data[-timesteps:]

        #Load image
        frames = []
        for p2i in lst_data:
            frame = Image.open(p2i).convert('RGB')
            frames.append(frame)

        #Data enhancement transformation
        frames_tr = []
        for frame in frames:
            frame = test_transformer(frame)
            frames_tr.append(frame)

        #Data merging
        if len(frames_tr) > 0:
            frames_tr = torch.stack(frames_tr)

        #Forecast
        # out = model(frames_tr.reshape((-1, *frames_tr.shape)).to(device))
        out = model(torch.stack([frames_tr]).to(device))
        # out=model(frames_tr)
        print(lst_data,out,label)
        pred = out.argmax(dim=1, keepdim=True)
        # print(j,pred[0][0],label)

        dic_sum_num[j] += 1
        if pred[0][0]==label:
            dic_true_num[j] +=1
        # print(lst_class[pred[0][0]])
        # dic_true_num = defaultdict(int)
        # dic_sum_num = defaultdict(int)

for i in dic_sum_num:
    print(f'Time {i+1} Accuracy: {dic_true_num[i]/dic_sum_num[i]:.4f}')
    # print('new_time_series=%s,accuracy：'(i+1),dic_true_num[i]/dic_sum_num[i])

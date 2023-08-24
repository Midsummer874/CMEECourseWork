from torch.utils.data import Dataset, DataLoader, Subset
from PIL import Image
import torch
import random
import pandas as pd
import os

import collections
data=pd.read_excel('Copy of groupby_cp.xlsx')

dic_class_index={
'pre':0,'post':0,'control':1
}
value=data[['Original name','flower_id','pollination status']].values

dic_id_label=collections.defaultdict(list)
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
lst_img_path_train=[]
lst_img_label_train=[]

lst_img_path_test=[]
lst_img_label_test=[]

train_size=0.2
for k in dic_id_name:
    if random.random()<train_size:
        lst_img_path_train.append(dic_id_name[k])
        lst_img_label_train.append(dic_id_label[k])
    else:
        lst_img_path_test.append(dic_id_name[k])
        lst_img_label_test.append(dic_id_label[k])
print('Train data：',len(lst_img_path_train))
print('Test data：',len(lst_img_path_test))

dic={1:0,0:1}
for idx in range(len(lst_img_label_train)):
    if 1 in lst_img_label_train[idx]:
        dic[1]+=1
    else:
        dic[0]+=1
print(dic)
dic={1:0,0:1}
for idx in range(len(lst_img_label_test)):
    if 1 in lst_img_label_test[idx]:
        dic[1]+=1
    else:
        dic[0]+=1
print(dic)
# print(dic)
# sys.exit()

#Define the data set class
class VideoDataset(Dataset):
    def __init__(self,lst_img_path,lst_img_label,transform):
        self.transform=transform
        self.lst_img_path=lst_img_path
        self.lst_img_label=lst_img_label

    def __len__(self):
        return len(self.lst_img_path)

    def __getitem__(self,idx):
        path2imgs=self.lst_img_path[idx]
        #If insufficient, add more data
        while len(path2imgs)<timesteps:
            path2imgs.append(path2imgs[-1])
        path2imgs=path2imgs[-timesteps:]

        if 1 in self.lst_img_label[idx]:
            label=1
        else:
            label=0
        #Read image
        frames=[]
        for p2i in path2imgs:
            frame=Image.open(p2i).convert('RGB')
            frames.append(frame)
        # seed=np.random.randint(1e9)

        #Data enhancement transformation
        frames_tr=[]
        for frame in frames:
            frame=self.transform(frame)
            frames_tr.append(frame)
        #Data merging
        if len(frames_tr)>0:
            frames_tr=torch.stack(frames_tr)
        return frames_tr, label
timesteps=4
#Define transformation parameter
num_classes=2
h,w=224,224
mean=[0.485,0.456,0.406]
std=[0.229,0.224,0.225]



import torchvision.transforms as transforms
#Image data transformation and data enhancement
train_transformer=transforms.Compose([
        transforms.Resize((h,w)),#Conversion size
        transforms.RandomHorizontalFlip(p=0.5),#Horizontal flip
        transforms.RandomAffine(degrees=0, translate=(0.1,0.1)),#Random affine variation
        transforms.ToTensor(),#Format conversion
        transforms.Normalize(mean,std),#The ImageNet standard
        ])
#Read training data
train_ds=VideoDataset(lst_img_path=lst_img_path_train,lst_img_label=lst_img_label_train,transform=train_transformer)

#Define a transformation function for the test set
test_transformer=transforms.Compose([
        transforms.Resize((h,w)),
        transforms.ToTensor(),
        transforms.Normalize(mean,std),
        ])
#Read test data
test_ds=VideoDataset(lst_img_path=lst_img_path_test,lst_img_label=lst_img_label_test,transform=test_transformer)

# Define the collate_fn_rnn helper function to read the test data according to the format of the batch conversion image
def collate_fn_rnn(batch):
    imgs_batch,label_batch=list(zip(*batch))
    imgs_batch=[imgs for imgs in imgs_batch if len(imgs)>0]
    label_batch=[torch.tensor(l) for l, imgs in zip(label_batch,imgs_batch) if len(imgs)>0]
    imgs_tensor=torch.stack(imgs_batch)
    labels_tensor=torch.stack(label_batch)
    return imgs_tensor,labels_tensor

#Define the data loader
batch_size=4
train_dl=DataLoader(train_ds, batch_size=batch_size,shuffle=True,collate_fn=collate_fn_rnn)
test_dl=DataLoader(test_ds,batch_size=2*batch_size,shuffle=False,collate_fn=collate_fn_rnn)

from torch import nn
from torchvision import models

#Structural model
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
        #Add LSTM
        self.rnn=nn.LSTM(num_features,rnn_hidden_size,rnn_num_layers)
        self.fc1=nn.Linear(rnn_hidden_size, num_classes)

    def forward(self,x):
        b_z,ts,c,h,w=x.shape
        # print(x.shape)
        # import sys
        # sys.exit()
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
device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model=model.to(device)

#Read the trained model weights
model.load_state_dict(torch.load('best_model.pth'))
# model.load_state_dict(torch.load('models/weights.pt'))

#Define the loss function, optimizer, and learning rate plan:
from torch import optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import myutils
#Defined loss function
loss_func=nn.CrossEntropyLoss(reduction="sum")
#Set learning rate
opt=optim.Adam(model.parameters(),lr=3e-5)
lr_scheduler=ReduceLROnPlateau(opt,mode="min",factor=0.5,patience=5,verbose=1)
os.makedirs("./models",exist_ok=True)
#Call the train_val helper function in myutils to train the model
params_train={
	"num_epochs":20,
	"optimizer":opt,
	"loss_func":loss_func,
	"train_dl":train_dl,
	"val_dl":test_dl,
	"sanity_check":False,
	"lr_scheduler":lr_scheduler,
	"path2weights":"./models/weights.pt",
}
#Training model
model,loss_hist,metric_hist=myutils.train_val(model,params_train)

#After the training, plot the training progress
myutils.plot_loss(loss_hist, metric_hist)
#Save model
# torch.save(model.state_dict(),'best_model.pth')
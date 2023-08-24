#This script is used for training the model
import os
import torch
import copy
from tqdm import tqdm_notebook
from torchvision.transforms.functional import to_pil_image
import matplotlib.pylab as plt
device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def train_val(model, params):
    num_epochs=params["num_epochs"]
    loss_func=params["loss_func"]
    opt=params["optimizer"]
    train_dl=params["train_dl"]
    val_dl=params["val_dl"]
    sanity_check=params["sanity_check"]
    lr_scheduler=params["lr_scheduler"]
    path2weights=params["path2weights"]

    loss_history={"train":[],"val":[]}
    metric_history={"train":[],"val":[]}
    best_model_wts=copy.deepcopy(model.state_dict())
    best_loss=float("inf")
    for epoch in range(num_epochs):
        current_lr=get_lr(opt)
        print("Epoch {}/{}, current lr={}".format(epoch, num_epochs-1,current_lr))
        model.train()
        train_loss,train_metric=loss_epoch(model,loss_func,train_dl,sanity_check,opt)
        loss_history["train"].append(train_loss)
        metric_history["train"].append(train_metric)
        model.eval()
        with torch.no_grad():
            val_loss,val_metric=loss_epoch(model,loss_func,val_dl,sanity_check)
        if val_loss<best_loss:
            best_loss=val_loss
            best_model_wts=copy.deepcopy(model.state_dict())
            torch.save(model.state_dict(),path2weights)
            print("Copied best model weights")
        loss_history["val"].append(val_loss)
        metric_history["val"].append(val_metric)
        lr_scheduler.step(val_loss)
        if current_lr!=get_lr(opt):
            print("Loading best model weights")
            model.load_state_dict(best_model_wts)
        print("Train loss:%.6f, dev loss:%.6f, accuracy:%.2f" % (train_loss, val_loss, 100*val_metric))
        print("-"*10)
    model.load_state_dict(best_model_wts)
    return model, loss_history, metric_history

def get_lr(opt):
    for param_group in opt.param_groups:
        return param_group["lr"]

def metrics_batch(output, target):
    pred=output.argmax(dim=1,keepdim=True)
    # print(pred)

    corrects=pred.eq(target.view_as(pred)).sum().item()
    # print(pred)
    # print(target)
    # print(corrects)
    return corrects

def loss_batch(loss_func, output, target, opt=None):
    # print(output,target)
    loss=loss_func(output, target)
    with torch.no_grad():
        metric_b=metrics_batch(output,target)
    if opt is not None:
        opt.zero_grad()
        loss.backward()
        opt.step()
    return loss.item(), metric_b
def loss_epoch(model, loss_func, dataset_dl, sanity_check=False,opt=None):
    running_loss=0.0
    running_metric=0.0
    len_data=len(dataset_dl.dataset)
    # print(888888888,len_data)
    for xb,yb in dataset_dl:
        xb=xb.to(device)
        yb=yb.to(device)
        output=model(xb)
        # print(output,yb)
        # print(yb)
        loss_b,metric_b=loss_batch(loss_func,output,yb,opt)
        running_loss+=loss_b
        if metric_b is not None:
            running_metric+=metric_b
        if sanity_check is True:
            break
    loss=running_loss/float(len_data)
    metric=running_metric/float(len_data)
    return loss, metric

def plot_loss(loss_hist, metric_hist):
    num_epochs=len(loss_hist["train"])
    plt.title("Train-Val Loss")
    plt.plot(range(1,num_epochs+1),loss_hist["train"],label="train")
    plt.plot(range(1,num_epochs+1),loss_hist["val"],label="val")
    plt.ylabel("Loss")
    plt.xlabel("Training Epochs")
    plt.legend()
    plt.show()
    plt.title("Train-Val Accuracy")
    plt.plot(range(1,num_epochs+1),metric_hist["train"],label="train")
    plt.plot(range(1,num_epochs+1),metric_hist["val"],label="val")
    plt.ylabel("Accuracy")
    plt.xlabel("Training Epochs")
    plt.legend()
    plt.show()

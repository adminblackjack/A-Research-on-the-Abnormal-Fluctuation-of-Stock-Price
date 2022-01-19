import sys
import numpy as np
import matplotlib.pyplot as plt
import paddle
import pandas as pd
import os

ckpt_path='checkpoints/'
if not os.path.exists(ckpt_path):
    os.mkdir(ckpt_path)

path=os.getcwd()
dataset=pd.read_csv('000001.XSHE_new.csv')
col='high'
use_gpu=False
if use_gpu:
    paddle.set_device('gpu')
else:
    paddle.set_device('cpu')


def normalize(dt, data_min,data_range):
    return (dt-data_min)/data_range

def inverse_normalization(dt,data_min, data_range):
    return dt*data_range+data_min

class Dataset(paddle.io.Dataset):
    def __init__(self,dataset):
        """
        初始化数据集
        :param dataset:归一化之后的数据
        """
        super(Dataset,self).__init__()
        self.data=dataset
        self.x_data=[]
        self.y_data=[]

        self.transform()

    def transform(self):
        # 每100天的数据作为一个输入
        for i in range(100,len(self.data)):
            # 将每100天的数据转换成100行1列的二维数组，然后再放到列表中
            self.x_data.append(np.array(self.data[i-100:i].reshape(-1, 1)))
            self.y_data.append(np.array(self.data[i]))

    def __getitem__(self,idx):
        # 返回单条数据
        data=self.x_data[idx]
        label=self.y_data[idx]
        return data, label

    def __len__(self):
        return len(self.x_data)

class Network(paddle.nn.Layer):
    def __init__(self):
        super(Network,self).__init__()

        self.lstm=paddle.nn.LSTM(
            input_size=1,
            hidden_size=50,
            num_layers=4,
            dropout=0.2,
        )

        self.fc=paddle.nn.Linear(in_features=50,out_features=1)

    def forward(self,x):
        outputs, final_states=self.lstm(x)
        # 使用最后一层的final_state作为全连接层的输入数据
        y=self.fc(final_states[0][3])
        return y
    
def train():
    train_data = dataset[col][:500].values
    # 计算训练集的最大值 最小值 极差
    train_data_max=train_data.max()
    train_data_min=train_data.min()
    train_data_range=train_data_max-train_data_min

    # 对数据进行归一化
    train_data=normalize(train_data,train_data_min,train_data_range).astype('float32')

    train_data=Dataset(train_data)
    train_loader=paddle.io.DataLoader(train_data,batch_size=500,shuffle=False)

    print('训练集大小：',len(train_data))
    model=Network()
    opt=paddle.optimizer.Adam(parameters=model.parameters(),learning_rate=0.001)
    mse_loss=paddle.nn.MSELoss()

    ckpt=False
    base_epoch=0
    if ckpt:
        base_epoch=1000
        ckpt_model_file_path=os.path.join(ckpt_path,'model.pdparams')
        ckpt_opt_file_path=os.path.join(ckpt_path,'opt.pdparams')
        model.set_state_dict(paddle.load(ckpt_model_file_path))
        opt.set_state_dict(paddle.load(ckpt_opt_file_path))
    epochs = 400
    model.train()
    for epoch in range(base_epoch,base_epoch + epochs):
        for batch_id,data in enumerate(train_loader()):
            x_data=data[0]
            y_data=data[1]
            predict=model.forward(x_data)

            loss=mse_loss(predict,y_data.reshape((-1, 1)))

            loss.backward()
            opt.step()
            opt.clear_grad()
            if batch_id%20 == 0:
                print("epoch：{},batch_id:{},loss:{}".format(epoch,batch_id, loss.numpy()))

        if epoch%50==0:
            paddle.save(model.state_dict(),os.path.join(ckpt_path,'ckpt_model_epoch_{}.pdparams'.format(epoch)))
            paddle.save(opt.state_dict(),os.path.join(ckpt_path,'ckpt_opt_epoch_{}.pdparams'.format(epoch)))

    # 保存最终的模型
    paddle.save(model.state_dict(),os.path.join(ckpt_path,'model.pdparams'))
    paddle.save(opt.state_dict(),os.path.join(ckpt_path,'opt.pdparams'))

train()


def plot_result(test_data,predicted_data,y_label):
    '''
    将最终的结果画图
    param test_data:验证集
    param predicted_data:预测值
    param y_label:y轴的label
    return:None
    '''
    plt.plot(test_data, color='blue',label='000001 real')
    plt.plot(predicted_data, color='green',label='000001 predict')
    plt.title("000001 stock price")
    plt.xlabel('time')
    plt.ylabel(y_label)
    plt.legend()
    plt.show()

def predict():
    test_data=dataset[col][501:].values


    train_data=dataset[col][:500].values
    # 计算训练集的最大值 最小值 极差
    train_data_max=train_data.max()
    train_data_min=train_data.min()
    train_data_range=train_data_max-train_data_min

    # 对数据进行归一化
    train_data=normalize(train_data,train_data_min,train_data_range).astype('float32')

    # 归一化
    test_data=normalize(test_data,train_data_min,train_data_range).astype('float32')

    # 将历史100天的数据与测试数据在水平方向上进行平铺
    test_input=np.hstack((train_data[-100:],test_data)).astype('float32')
    test_input=Dataset(test_input)

    test_loader=paddle.io.DataLoader(test_input,batch_size=len(test_input),drop_last=False)

    model=Network()
    model_path=os.path.join(ckpt_path,'model.pdparams')
    state_dict=paddle.load(model_path)
    model.load_dict(state_dict)

    model.eval()
    result=None

    for batch_id,data in enumerate(test_loader()):
        x_data=data[0]
        predicts=model.forward(x_data)
        result=predicts.reshape((-1, 1))

    result=inverse_normalization(result,train_data_min,train_data_range).numpy()
    test_set=dataset[col][501:].values
    plot_result(test_set,result,col)

predict()

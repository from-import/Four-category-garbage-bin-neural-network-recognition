# Four-category-garbage-bin-neural-network-recognition
四分类垃圾桶神经网络识别

https://maixhub.com/model/training/project


训练参数： 图像增强+随机镜像+随机旋转+随机模糊  
缩放方式contain  
缩放宽度224  
缩放高度224  
平均值123.5  
标准差58.395  

模型信息:  
部署平台nncase  
模型类型transfer_learning  
模型网络default  
主干网络mobilenet_0.75  

训练参数:   
训练次数100  
批量大小32  
学习率0.001  
标注框限制10  

混淆矩阵  
•	横坐标是期望值（即标注的标签值），纵坐标是模型预测的值，中间的数值为计数  
•	期望值和预测值相同的数量越多表示验证集的拟合效果越好  
•	注意，如果你发现在验证集的正确率很高，而实际在硬件上跑起来准确率低，则需要考虑是不是训练数据的数量和覆盖的场景不足  
 ![image](https://github.com/user-attachments/assets/5207b936-c855-41db-8a82-3cc40671f5cb)  


损失和精确度  
•	loss 指损失函数计算后的损失值，值看左侧纵坐标，在下降说明模型训练仍然可以收敛，但不代表实际效果好  
•	acc 指预测正确率，值看右侧纵坐标，代表在训练集上的正确率，在上升说明模型正在训练集上收敛，但不代表实际效果好  
•	val_acc 指在验证集的预测正确率，代表在验证集上的正确率，用来作为判断模型训练效果的依据，实际应用效果则取决于验证集和实际场景的差距  
在验证集上第100次训练迭代有最佳准确率：0.969  

 ![image](https://github.com/user-attachments/assets/b7072585-66fe-41de-8f1e-3fbdb0d3467b)  


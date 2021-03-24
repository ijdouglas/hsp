library(magrittr)
library(dplyr)
library(ggpubr)
library(MASS)
library(ggplot2)
library(ggrepel)
setwd("~/Desktop/sth-sth/matlabs")


################################################

bend_label_csv = read.csv("bend_labels.csv")
bend_mds = read.csv("bend_matlab_mds.csv",header=FALSE)
colnames(bend_mds) = c("Dim1","Dim2")

ggplot(data=bend_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=bend_label_csv[,2], pch=bend_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Bend (break)")+
  theme_bw()+
  geom_text_repel(label=bend_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("bend_1.png",dpi=600,units="in",width=8,height=6)


################################################


cut_label_csv = read.csv("cut_labels.csv")
cut_mds = read.csv("cut_matlab_mds.csv",header=FALSE)
colnames(cut_mds) = c("Dim1","Dim2")

ggplot(data=cut_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=cut_label_csv[,2], pch=cut_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Cut")+
  theme_bw()+
  geom_text_repel(label=cut_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("cut_1.png",dpi=600,units="in",width=8,height=6)


################################################


eat_label_csv = read.csv("eat_labels.csv")
eat_mds = read.csv("eat_matlab_mds.csv",header=FALSE)
colnames(eat_mds) = c("Dim1","Dim2")

ggplot(data=eat_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=eat_label_csv[,2], pch=eat_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Eat")+
  theme_bw()+
  geom_text_repel(label=eat_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("eat_1.png",dpi=600,units="in",width=8,height=6)


################################################


fall_label_csv = read.csv("fall_labels.csv")
fall_mds = read.csv("fall_matlab_mds.csv",header=FALSE)
colnames(fall_mds) = c("Dim1","Dim2")

ggplot(data=fall_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=fall_label_csv[,2], pch=fall_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Fall")+
  theme_bw()+
  geom_text_repel(label=fall_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("fall_1.png",dpi=600,units="in",width=8,height=6)


################################################


fit_label_csv = read.csv("fit_labels.csv")
fit_mds = read.csv("fit_matlab_mds.csv",header=FALSE)
colnames(fit_mds) = c("Dim1","Dim2")

ggplot(data=fit_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=fit_label_csv[,2], pch=fit_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Fit")+
  theme_bw()+
  geom_text_repel(label=fit_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("fit_1.png",dpi=600,units="in",width=8,height=6)


################################################


hold_label_csv = read.csv("hold_labels.csv")
hold_mds = read.csv("hold_matlab_mds.csv",header=FALSE)
colnames(hold_mds) = c("Dim1","Dim2")

ggplot(data=hold_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=hold_label_csv[,2], pch=hold_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Hold")+
  theme_bw()+
  geom_text_repel(label=hold_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("hold_1.png",dpi=600,units="in",width=8,height=6)


################################################


put_label_csv = read.csv("put_labels.csv")
put_mds = read.csv("put_matlab_mds.csv",header=FALSE)
colnames(put_mds) = c("Dim1","Dim2")

ggplot(data=put_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=put_label_csv[,2], pch=put_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Put")+
  theme_bw()+
  geom_text_repel(label=put_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("put_1.png",dpi=600,units="in",width=8,height=6)


################################################

shake_label_csv = read.csv("shake_labels.csv")
shake_mds = read.csv("shake_matlab_mds.csv",header=FALSE)
colnames(shake_mds) = c("Dim1","Dim2")

ggplot(data=shake_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=shake_label_csv[,2], pch=shake_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Shake")+
  theme_bw()+
  geom_text_repel(label=shake_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("shake_1.png",dpi=600,units="in",width=8,height=6)


################################################

stack_label_csv = read.csv("stack_labels.csv")
stack_mds = read.csv("stack_matlab_mds.csv",header=FALSE)
colnames(stack_mds) = c("Dim1","Dim2")

ggplot(data=stack_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=stack_label_csv[,2], pch=stack_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Stack")+
  theme_bw()+
  geom_text_repel(label=stack_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("stack_1.png",dpi=600,units="in",width=8,height=6)


################################################

turn_label_csv = read.csv("turn_labels.csv")
turn_mds = read.csv("turn_matlab_mds.csv",header=FALSE)
colnames(turn_mds) = c("Dim1","Dim2")

ggplot(data=turn_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=turn_label_csv[,2], pch=turn_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Turn")+
  theme_bw()+
  geom_text_repel(label=turn_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("turn_1.png",dpi=600,units="in",width=8,height=6)


################################################

walk_label_csv = read.csv("walk_labels.csv")
walk_mds = read.csv("walk_matlab_mds.csv",header=FALSE)
colnames(walk_mds) = c("Dim1","Dim2")

ggplot(data=walk_mds,aes(x=Dim1, y=Dim2))+
  geom_point(aes(color=walk_label_csv[,2], pch=walk_label_csv[,3]), size=3)+
  ggtitle("Nouns that were used with: Walk")+
  theme_bw()+
  geom_text_repel(label=walk_label_csv[,1],min.segment.length = 0.2,size=2)+
  #scale_shape_manual(values=c(1,15,17),name="MCDI")+
  scale_shape_manual(values=c(1,15,17),name="Acquisition / MCDI",label=c('Neither','Infant','Toddler'))+
  scale_color_manual(values=c('blue',"red"),name='Video dataset',label=c('Yu lab egocentric vids','Sth sth/Epic kitchen'))+
  labs(caption='(Similarity measurements based on counter-fitted paragram vectors)')
ggsave("walk_1.png",dpi=600,units="in",width=8,height=6)


################################################
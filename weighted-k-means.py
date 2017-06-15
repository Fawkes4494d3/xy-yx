#!/usr/bin/env python
#weighted k means
#code written by Soumava Pal
import random
import matplotlib.pyplot as plt
import Tkinter
def d(x,y):
	return (x-y)**2
def P(U,Z,W,X,k,n,m,b):
	s=0
	for l in range(k):
		for i in range(n):
			for j in range(m):
				s+=U[i][l]*(W[j]**b)*d(X[i][j],Z[l][j])
	return s
def dist(x,y,w,b):
	s=0
	for j in range(len(x)):
		s+=(w[j]**b)*d(x[j],y[j])
	return s
def D1(j,U,Z,X,k,n):
	s=0
	for l in range(k):
		for i in range(n):
			s+=U[i][l]*d(X[i][j],Z[l][j])
	return s
def solving1(U,X,W,Z,k,n,m,b,t):
	Z1=Z
	W1=W
	distances=[]
	for i in range(n):
		M=[]
		for l in range(k):
			M.append(dist(X[i],Z1[l],W1,b))
		distances.append(M)
	membership=[distances[i].index(min(distances[i])) for i in range(n)]
	U1=[[0 for i in range(k)] for j in range(n)]
	for i in range(n):
		for l in range(k):
			if (membership[i]==l):
				U1[i][l]=1
	if (P(U1,Z1,W1,X,k,n,m,b)==P(U,Z1,W1,X,k,n,m,b) and t>=50):
		print U
		print Z1
		print W1
		return
	else:
		solving2(U1,X,W1,Z1,k,n,m,b,t)
def solving2(U,X,W,Z,k,n,m,b,t):
	W1=W
	U1=U
	Z1=[[0 for i in range(m)] for j in range(k)]
	numbers=[0 for i in range(k)]
	for l in range(k):
		for i in range(n):
			numbers[l]+=U1[i][l]
	for l in range(k):
		for j in range(m):
			for i in range(n):
				Z1[l][j]+=(U1[i][l]*X[i][j])/float(numbers[l])
	if (P(U1,Z1,W1,X,k,n,m,b)==P(U1,Z,W1,X,k,n,m,b) and t>=50):
		print U1
		print Z
		print W1
		return
	else:
		solving3(U1,X,W1,Z1,k,n,m,b,t)
def solving3(U,X,W,Z,k,n,m,b,t):
	if b>1 or b<=0:	
		D=[0 for i in range(m)]
		D_b=[0 for i in range(m)]
		U1=U
		Z1=Z
		h=0
		s=0	
		for i in range(m):
			D[i]=(D1(i,U1,Z1,X,k,n))
			if D[i]!=0:
				h+=1
				s+=1/(D[i]**(1/(b-1)))
				D_b[i]=D[i]**(1/(b-1))
		W1=[0 for i in range(m)]
		for j in range(m):
			if D_b[j]==0: W1[j]=0			
			else:
				W1[j]=1/(s*D_b[j])
		if (P(U1,Z1,W1,X,k,n,m,b)==P(U1,Z1,W,X,k,n,m,b) and t>=50):
			print U1
			print Z1
			print W1
			return
		else:
			t+=1
			solving1(U1,X,W1,Z1,k,n,m,b,t)

	elif b==1:
		D=[0 for i in range(m)]
		U1=U
		Z1=Z
		for i in range(m):
			D[i]=(D1(i,U1,Z1,X,k,n))
		j=D.index(min(D))
		W1=[0 for i in range(m)]
		W1[j]=1
		if (P(U1,Z1,W1,X,k,n,m,b)==P(U1,Z1,W,X,k,n,m,b) and t>=50):
			print U1
			print Z1
			print W1
			return
		else:
			t+=1
			solving1(U1,X,W1,Z1,k,n,m,b,t)

#main
ask=raw_input('Type r to read files or inp to input your own data:')
if ask=='r':
	filename=raw_input('Enter the name of the file you want to read:')
	f=open(filename,'r')
	vertices=f.readlines()
	vertices.pop(0)
	n=len(vertices)
	if ',' in vertices[0]: #assuming that the delimiter is either a comma...
		for i in range(n):
			vertices[i]=vertices[i][:-1] #removing the \n character
			vertices[i]=map(float,vertices[i].split(','))
			vertices[i]=vertices[i][:-1]
	elif ' ' in vertices[0]: # ...or a space
		for i in range(n):
			vertices[i]=vertices[i][:-1] #removing the \n character
			vertices[i]=map(float,vertices[i].split())
			vertices[i]=vertices[i][:-1]
	m=len(vertices[0])
	f.close()
	if m==2:
		Abscissa=[vertices[i][0] for i in range(n)]
		Ordinate=[vertices[i][1] for i in range(n)]
		print Abscissa
		print Ordinate
		plt.plot(Abscissa,Ordinate,'ro')
		plt.axis([-1,1.5,-5,45])
		plt.show()
else:
	n=int(raw_input('Enter the number of data points:'))
	m=int(raw_input('Enter the number of features:'))
	vertices=[]
	for i in range(n):
		M=map(float,raw_input().split())
		vertices.append(M)
k=int(raw_input('Enter the number of clusters:'))
beta=float(raw_input('Enter the power to which weights should be raised:'))
centers=random.sample(xrange(n),k) #choosing centers of clusters randomly
weights=[]
for i in range(m):
	weights.append(random.random())
h=sum(weights)
for i in range(m):
	weights[i]/=h
for i in range(k):
	centers[i]=vertices[centers[i]]
distances=[]
for i in range(n):
	M=[]
	for l in range(k):
		M.append(dist(vertices[i],centers[l],weights,beta))
	distances.append(M) #distances of n vertices from k centers stored in nxk matrix
membership=[distances[i].index(min(distances[i])) for i in range(n)]
adjacency=[[0 for i in range(k)] for j in range(n)]
for i in range(n):
	for j in range(k):
		if (membership[i]==j):
			adjacency[i][j]=1
t=0
solving1(adjacency,vertices,weights,centers,k,n,m,beta,t)

#!/usr/bin/env python
#weighted k means
import random
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
		return U
	else:
		return solving2(U1,X,W1,Z1,k,n,m,b,t)
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
		return U1
	else:
		return solving3(U1,X,W1,Z1,k,n,m,b,t)
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
			return U1
		else:
			t+=1
			return solving1(U1,X,W1,Z1,k,n,m,b,t)

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
			return U1
		else:
			t+=1
			return solving1(U1,X,W1,Z1,k,n,m,b,t)

#main
ask=raw_input('Type r to read files or inp to input your own data:')
member=[]
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
			member.append(int(vertices[i].pop()))
	elif ' ' in vertices[0]: # ...or a space
		for i in range(n):
			vertices[i]=vertices[i][:-1] #removing the \n character
			vertices[i]=map(float,vertices[i].split())
			member.append(int(vertices[i].pop()))
	num=max(member)
	m=len(vertices[0])
	f.close()
else:
	n=int(raw_input('Enter the number of data points:'))
	m=int(raw_input('Enter the number of features:'))
	vertices=[]
	for i in range(n):
		M=map(float,raw_input().split())
		vertices.append(M)
mean,sd=0.0,0.0
k=int(raw_input('Enter the number of clusters:'))
N=int(raw_input('Enter the number of times you want to run:'))
beta=float(raw_input('Enter the power to which weights should be raised:'))
for MJ in range(N):
	centers=random.sample(xrange(n),k) #choosing centers of clusters randomly
	weights=[]
	for i in range(m):
		weights.append(random.random())
	h=sum(weights)
	for i in range(m):
		weights[i]/=h
	h=random.sample(range(n),1)
	centers=[vertices[h[0]]]
	while (len(centers)!=k):
		distances=[]
		for i in range(n):
			mini=dist(vertices[i],centers[0],weights,beta)
			for j in range(len(centers)):
				if dist(vertices[i],centers[j],weights,beta)<mini:
					mini=dist(vertices[i],centers[j],weights,beta)
			distances.append(mini)
		for i in range(1,n):
			distances[i]+=distances[i-1]
		for i in range(n):
			distances[i]/=float(distances[n-1])
		p=random.random()
		for i in range(n):
			if (p>=distances[i] and p<=distances[i+1]):
				centers.append(vertices[i])
				break
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
	compare=solving1(adjacency,vertices,weights,centers,k,n,m,beta,t)
	membership=[compare[i].index(1) for i in range(n)]
	contingency=[[0 for i in range(num)] for j in range(k)]
	for i in range(n):
			contingency[membership[i]][member[i]-1]+=1
	marginal1=[0 for i in range(num)]
	marginal2=[0 for i in range(k)]
	for i in range(num):
		for j in range(k):
			marginal1[i]+=contingency[j][i]
	for i in range(k):
		for j in range(num):
			marginal2[i]+=contingency[i][j]
	suma=0
	sumb=0
	sumc=0
	for i in range(k):
		for j in range(num):
			suma+=(contingency[i][j]*(contingency[i][j]-1))/2.0
	for i in range(k):
		sumb+=(marginal2[i]*(marginal2[i]-1))/2.0
	for i in range(num):
		sumc+=(marginal1[i]*(marginal1[i]-1))/2.0
		ari=(suma-(sumb*sumc*2)/(n*n-n))/(0.5*sumb+0.5*sumc-(sumb*sumc*2)/(n*n-n))
	print "ARI=",ari
	mean+=ari
	sd+=ari**2
print 'The mean of the ARIs: ', float(mean)/N
print 'The standard deviation of the ARIs: ', (sd/N-(float(mean)/N)**2)**0.5

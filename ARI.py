#Written by Soumava Pal, and this code used by anyone else should be acknowledged accordingly
#!/usr/bin/env python
#ARI with k means
import random
def dist(x,y): #Euclidean distance between points x and y
	sum=0
	for i in range(len(x)):
		sum=sum+((x[i]-y[i])**2)
	return sum**0.5
def sum(x,y): #element wise sum of two arrays
	z=[]
	for i in range(len(x)):
		z.append(x[i]+y[i])
	return z
#main
ask=raw_input('Type r to read files or inp to input your own data:')
k=int(raw_input('Enter the number of clusters you want to make:'))
tol=float(raw_input('Enter the tolerance level:'))
if ask=='r':
	filename=raw_input('Enter the name of the file you want to read:')
	f=open(filename,'r')
	vertices=f.readlines()
	num=map(float,vertices[0][:-1].split())
	num=int(num.pop()) #number of clusters in the given data
	vertices.pop(0)
	n=len(vertices)
	member=[0 for i in range(n)]
	if ',' in vertices[0]: #assuming that the delimiter is either a comma...
		for i in range(n):
			vertices[i]=vertices[i][:-1] #removing the \n character
			vertices[i]=map(float,vertices[i].split(','))
			member[i]=int(vertices[i].pop())
	elif ' ' in vertices[0]: # ...or a space
		for i in range(n):
			vertices[i]=vertices[i][:-1] #removing the \n character
			vertices[i]=map(float,vertices[i].split())
			member[i]=int(vertices[i].pop())
	d=len(vertices[0])
	f.close()
else:
	n=int(raw_input('Enter the number of data points:'))
	d=int(raw_input('Enter the number of features:'))
	vertices=[]
	for i in range(n):
		M=map(float,raw_input().split())
		vertices.append(M)
mean,sd=0.0,0.0
N=int(raw_input('How many times do you want to run the clustering program? '))
for MJ in range(N):
	centers=random.sample(range(n),k) #choosing centers of clusters randomly
	for i in range(k):
		centers[i]=vertices[centers[i]]
	distances=[]
	for i in range(n):
		M=[]
		for j in range(k):
			M.append(dist(vertices[i],centers[j]))
		distances.append(M) #distances of n vertices from k centers stored in nxk matrix
	membership=[distances[i].index(min(distances[i])) for i in range(n)]
	compare=list(centers)
	centers=[[0 for i in range(d)] for i in range(k)]
	numbers=[0 for i in range(k)]
	for i in range(n):
		centers[membership[i]]=sum(centers[membership[i]],vertices[i])
		numbers[membership[i]]+=1
	for i in range(k):
		for j in range(d):
			centers[i][j]/=float(numbers[i])
	while max([dist(compare[i],centers[i]) for i in range(k)])<tol: #repeating iteration till the error is less than tolerance level
		distances=[]
		for i in range(n):
			M=[]
			for j in range(k):
				M.append(dist(vertices[i],centers[j]))
			distances.append(M)
		membership=[distances[i].index(min(distances[i])) for i in range(n)]
		compare=list(centers)
		centers=[[0 for i in range(d)] for i in range(k)]
		numbers=[0 for i in range(k)]
		for i in range(n):
			centers[membership[i]]=sum(centers[membership[i]],vertices[i])
			numbers[membership[i]]+=1
		for i in range(k):
			for j in range(d):
				centers[i][j]/=float(numbers[i])
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

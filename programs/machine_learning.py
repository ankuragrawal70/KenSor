from sklearn import svm
from sklearn import datasets
from sklearn import svm
clf = svm.SVC(gamma=0.001)
iris = datasets.load_iris()
digits = datasets.load_digits()
print digits.data[2]
print digits.images[2]

print digits.target

print clf.fit(digits.data[:-1], digits.target[:-1])
print clf.predict(digits.data[-1])
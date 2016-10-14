import codecs
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Binarizer
from sklearn.pipeline import Pipeline
from sklearn import naive_bayes
from sklearn.metrics import classification_report, accuracy_score, recall_score, precision_score, f1_score
from sklearn.cross_validation import KFold, LeaveOneOut, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier

def get_preprocessor(suffix=''):
	def preprocess(unicode_text):
		return unicode(unicode_text.strip().lower() + suffix)
	return preprocess

filename1 = 'subst_all-labeled_8forms.txt'
filename2 = 'subst_all-labeled_8oforms.txt'

def load_data(fin):
	infinitives, y = [], []
	with codecs.open(fin, 'r', encoding='utf-8') as f:
		for line in f:
			inf, label = line.split();
			infinitives.append(inf)
			y.append(int(label))
	infinitives, y = np.array(infinitives), np.array(y, dtype=np.int)
	return infinitives, y

def preprocess_data(X, n, suffix='', binarize=True):
	vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, n),preprocessor=get_preprocessor(suffix))
	X = vectorizer.fit_transform(X)
	X = Binarizer(copy=False).fit_transform(X) if binarize else X
	return X


def learn(fin):

	X, y = load_data(fin)
	X_new = preprocess_data(X, n=5, suffix='$', binarize=False)

	skf = StratifiedKFold(y, n_folds=5)
	clf = LinearSVC()

	# grid = GridSearchCV(estimator=LinearSVC(), n_jobs=4, verbose=False,param_grid={'C': (0.01, 0.03, 0.1, 0.3, 1, 1.3)}, cv=LeaveOneOut(n, indices=True))
	# grid.fit(X_new, y)

	dummy = DummyClassifier(strategy="stratified")

	accuracy, recall, precision, f1 = [], [], [], []
	dummy_acc, dummy_rec, dummy_prec, dummy_f1 = [], [], [], []
	for train_index, test_index in skf:
		X_train, X_test = X_new[train_index], X_new[test_index]
		y_train, y_test = y[train_index], y[test_index]
		print "fitting the classifier"
		clf.fit(X_train, y_train)
		dummy.fit(X_train, y_train)

		print "predicting"
		y_pred = clf.predict(X_test)
		y_dummy = dummy.predict(X_test)

		print "svm report:\n", classification_report(y_test, y_pred)
		print "dummy report: \n", classification_report(y_test, y_dummy)

		print "saving svm scores per fold"
		accuracy.append(accuracy_score(y_test, y_pred))
		precision.append(precision_score(y_test, y_pred, average='weighted'))
		recall.append(recall_score(y_test, y_pred, average='weighted'))
		f1.append(f1_score(y_test, y_pred, average='weighted'))

		print "saving dummie scores per fold"
		dummy_acc.append(accuracy_score(y_test, y_dummy))
		dummy_prec.append(precision_score(y_test, y_dummy, average='weighted'))
		dummy_rec.append(recall_score(y_test, y_dummy, average='weighted'))
		dummy_f1.append(f1_score(y_test, y_dummy, average='weighted'))

	print "accuracy mean ", np.mean(accuracy), " accuracy std ", np.std(accuracy)
	print "precision mean ", np.mean(precision), " and std ", np.std(precision)
	print "recall mean ", np.mean(recall), " and std ", np.std(recall)
	print "f1 mean ", np.mean(f1), " and std ", np.std(f1)

	print "dummy accuracy mean ", np.mean(dummy_acc), " accuracy std ", np.std(dummy_acc)
	print "dummy precision mean ", np.mean(dummy_rec), " and std ", np.std(dummy_prec)
	print "dummy recall mean ", np.mean(dummy_rec), " and std ", np.std(dummy_rec)
	print "dummy f1 mean ", np.mean(dummy_f1), " and std ", np.std(dummy_f1)


print "results for :", filename1  
learn(filename1)
print "results for :", filename2 
learn(filename2)

import newspaper
cnn=newspaper.build('http://www.cnn.com')
for url in cnn.category_urls():
    print url



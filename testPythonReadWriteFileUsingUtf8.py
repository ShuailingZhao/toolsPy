import numpy as np
import sys
import codecs

def main():
	

# write file
	f = codecs.open('./test/workfile.txt','a','utf-8')
	f.write(u'中文')
	s = '中文'
	f.write(s.encode('utf-8').decode('utf-8'))#s.encode('gbk').decode('gbk'), f.writelines(s2) write all list
	f.write(s)
	f.close()
	
# read file
	f = codecs.open('./test/workfile.txt','r','utf-8')
	while True:
		s = f.readline() #s = f.readlines() read all lines in the file
		if not s:
			break
		print('---- ',s)
	f.close()


if __name__ == "__main__":
    main()


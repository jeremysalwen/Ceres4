all: all_compiled

all_compiled: sndlib_compiled
	touch all_compiled


clean:
	rm -fr sndlib sndlib_compiled all_compiled install-dir/*


install:

#http://ccrma.stanford.edu/software/snd/sndlib/
sndlib_compiled:
	echo "\
	rm -fr sndlib;\
	tar xvzf sndlib.tar.gz;\
	cd sndlib;\
	./configure $(SNDLIBWITHJACK) --with-pic --without-guile;\
	make;\
	touch ../sndlib_compiled\
	" >makesource.sh
	sh makesource.sh
	rm makesource.sh



all_compiled: pygtk1_compiled sndlib_compiled
	touch all_compiled


clean:
	rm -fr pygtk-0.6.12 sndlib pygtk1_compiled sndlib_compiled all_compiled install-dir/*


install:
	cd pygtk-0.6.12 && make install


pygtk1_compiled: ../Makefile
	bash make_pygtk1.sh $(PYGTK1PATH)

#http://ccrma.stanford.edu/software/snd/sndlib/
sndlib_compiled:
	echo "\
	rm -fr sndlib;\
	tar xvzf sndlib.tar.gz;\
	cd sndlib;\
	./configure $(SNDLIBWITHJACK) --with-pic --without-guile;\
	make;\
	touch sndlib_compiled\
	" >makesource.sh
	sh makesource.sh
	rm makesource.sh

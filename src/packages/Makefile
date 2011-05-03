all_compiled: sndlib_compiled
	touch all_compiled

clean:
	rm -fr libxml-1.8.17 libglade-0.17 pygtk-0.6.12 sndlib libxml_compiled libglade_compiled pygtk1_compiled openmotif_compiled glib-1.2.10 glib_compiled gtk+-1.2.10 gtk+_compiled openmotif-2.3.2 sndlib_compiled all_compiled install-dir/*



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

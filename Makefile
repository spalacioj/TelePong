all: compile link

compile:
	gcc serverThreads.c -o serverThreads -lpthread

link:
	./serverThreads

clean:
	rm -f serverThreads 
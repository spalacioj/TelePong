all: compile link

compile:
	gcc PaddleSync.c server.c -o server -lpthread

link:
	./server

clean:
	rm -f serverThreads 
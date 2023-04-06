all: framework_java

.PHONY: framework_java
framework_java:
	javac `find . -name "*.java"`
	jar cvf ./Framework.jar `find ./ -name "*.class"`

clean:
	rm -f ./*.class
	rm -f ./*.jar
	rm -f ./*.bin
	rm -f ./utils/*.class

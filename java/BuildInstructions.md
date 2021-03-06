# Building Ice for Java

This page describes how to build and install Ice for Java from source code. If
you prefer, you can also download [binary distributions][1] for the supported
platforms.

## Build Requirements

### Operating Systems

Ice for Java is expected to build and run properly on Windows, OS X, and any
recent Linux distribution for x86 and x86_64, and was extensively tested using
the operating systems and compiler versions listed for our [supported platforms][2].
Due to the portability of Java, it is very likely that it will also work on other
platforms for which a suitable Java implementation is available.

### Slice to Java Translator

You will need the Slice to Java translator. ZeroC provides translator binaries for
our supported platforms. For other platforms, you will have to either port Ice for
C++ (which contains the Slice to Java translator), or you will have to translate
your Slice files to Java on a supported platform and then copy the generated Java
files to your target platform.

### Java Version

Ice for Java requires J2SE 1.7.0 or later.

The Metrics Graph feature of the graphical IceGrid administrative tool requires
J2SE 7u6 or later with JavaFX support. This feature will not be available if you
build the source with a JVM that lacks support for JavaFX. Alternatively, building
the source using J2SE 7u6 or later with JavaFX produces a JAR file that can be
used in JVMs with or without JavaFX support, as the Metrics Graph feature is
enabled dynamically.

Make sure that the `javac` and `java` commands are present in your PATH.

### Berkeley DB

"Freeze" is an optional Ice component that provides a persistence facility for
Ice applications. Freeze uses Berkeley DB as its underlying database and currently
requires Berkeley DB version 5.3 (the recommended version is 5.3.28).

ZeroC includes Berkeley DB in the binary distributions for all supported platforms,
or you can build it from source yourself.

In order to run an application that uses Freeze, you must add `db.jar` to your
CLASSPATH and verify that the Berkeley DB shared libraries are in your
`java.library.path`.

Assuming you are using ZeroC's distribution of Berkeley DB, the bash command is
shown below for Linux:

    $ export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH                 (RHEL, SLES, Amazon)
    $ export LD_LIBRARY_PATH=/usr/lib/i386-linux-gnu:$LD_LIBRARY_PATH  (Ubuntu)

On an x86_64 system with a 64-bit JVM, the 64-bit Berkeley DB libraries are
installed in a different directory:

    $ export LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH                 (RHEL, SLES, Amazon)
    $ export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH  (Ubuntu)

### Gradle

Ice for Java uses the [Gradle][3] build system, and includes the Gradle wrapper
version 2.4 in the distribution. You cannot build the Ice for Java source
distribution without an Internet connection. Except for Berkeley DB, Gradle will
download all required packages automatically. These packages are listed below.
Gradle will automatically download any necessary build artifacts from ZeroC's
Maven repository located at

    http://repo.zeroc.com/nexus/content/repositories/thirdparty

### Bzip2 Compression

Ice for Java supports protocol compression using the bzip2 classes included
with Apache Ant or available separately from [kohsuke.org]().

The Maven package id for the bzip2 JAR file is as follows:

    groupId=org.apache.tools, version=1.0, artifactId=bzip2

The demos and tests are automatically setup to enable protocol compression by
adding the bzip2 JAR to the manifest class path. For your own applications you
must add the bzip2 JAR to the application CLASSPATH to enable protocol
compression.

> *These classes are a pure Java implementation of the bzip2 algorithm and
therefore add significant latency to Ice requests.*

### JGoodies

The graphical IceGrid administrative tool uses the JGoodies libraries Common,
Forms, and Looks. The following versions were tested:

    JGoodies Common 1.8.0
    JGoodies Forms 1.8.0
    JGoodies Looks 2.6.0

The Maven package ids for the JGoodies packages are as follows:

    groupId=com.jgoodies, version=1.8.0, artifactId=jgoodies-common
    groupId=com.jgoodies, version=1.8.0, artifactId=jgoodies-forms
    groupId=com.jgoodies, version=2.6.0, artifactId=jgoodies-looks

### ProGuard

Gradle uses [ProGuard][4] to create the standalone JAR file for the graphical
IceGrid administrative tool.

The Maven package id for the ProGuard package is as follows:

    groupId=net.sourceforge, version=5.0, artifactId=proguard

### Java Application Bundler

Under OS X Gradle uses the Java Application Bundler to create an application
bundle for the graphical IceGrid administrative tool.

The Maven package id for the application bundler package is as follows:

    groupId=com.oracle, version=1.0, artifactId=appbundler
 
## Compiling Ice for Java

### Preparing to Build

This source distribution cannot be compiled successfully without the Berkeley DB
run time for Java (`db.jar`). The build system searches in standard locations
for the following two JAR files:

    db-5.3.28.jar
    db.jar

If neither of these files is present in the standard locations on your system,
you must set `dbHome` in `gradle.properties`.

The build system also requires the Slice translators from Ice for C++. If you
have not built Ice for C++ in this source distribution, you must set the
`ICE_HOME` environment variable with the path name of your Ice installation.
For example, on Unix:

    $ export ICE_HOME=/opt/Ice-3.6.0 (For local build)
    $ export ICE_HOME=/usr (For RPM installation)

On Windows:

    > set ICE_HOME=C:\Program Files (x86)\ZeroC\Ice-3.6.0

Before building Ice for Java, review the settings in the file `gradle.properties`
and edit as necessary.

### Building Ice for Java

To build Ice, all services, and tests, run

    > gradlew build

Upon completion, the Ice JAR and POM files are placed in the `lib` subdirectory.

If at any time you wish to discard the current build and start a new one, use
these commands:

    > gradlew clean
    > gradlew build

## Installing Ice for Java

To install Ice for Java in the directory specified by the `prefix` variable in
`gradle.properties` run the following command

    > gradlew install

The installation installs the following JAR files to `<prefix>/lib`.

    freeze-3.6.0.jar
    glacier2-3.6.0.jar
    ice-3.6.0.jar
    icebox-3.6.0.jar
    icediscovery-3.6.0.jar
    icegrid-3.6.0.jar
    icegridgui.jar
    icelocatordiscovery-3.6.0.jar
    icepatch2-3.6.0.jar
    icestorm-3.6.0.jar

POM files are also installed for ease of deployment to a maven-based distribution
system.

## Ice for Android

Ice requires Android 4.2 or later. The JAR files created and installed by the
standard Java build as detailed above fully support Android. However, for ease
of development and testing of Ice itself, an Android Studio project is bundled
in the source distribution which itself builds all required Ice JAR files.
This is not necessary for your own projects as it considerably complicates the
project configuration.

Building any Ice application for Android requires Android Studio and the Android
SDK build tools. We tested the following:

- Android Studio 1.0.0.
- Android SDK Build-tools 21.1.1

Ice requires at minimum API level 17:

- Android 4.2.2 (API17)

The bundled project builds Ice and a test suite application.

If you want to target a later version of the Android API level for the test
suite, edit `android/gradle.properties` and change the following variables:

    ice_compileSdkVersion
    ice_minSdkVersion
    ice_targetSdkVersion

To import the Ice for Android project into Android Studio follow these steps

1. Start Android studio
2. Select Open Project
3. Navigate to the android subdirectory
4. You should now have an "Import Project from Gradle" dialog
5. Ensure "Use default gradle wrapper" is selected and press OK 

The Android Studio project contains a `testApp` application to run the Ice test
suite. To run the application, select it in the configuration pull down and run it.

## Running the Java Tests

Some of the Ice for Java tests employ applications that are part of the Ice for
C++ distribution. If you have not built Ice for C++ in this source distribution
then you must set the `ICE_HOME` environment variable with the path name of your
Ice installation. On Unix:

    $ export ICE_HOME=/opt/Ice-3.6.0 (For local build)
    $ export ICE_HOME=/usr (For RPM installation)

On Windows:

    > set ICE_HOME=c:\Program Files (x86)\ZeroC\Ice-3.6.0

Python is required to run the test suite. To run the tests, open a command window
and change to the top-level directory. At the command prompt, execute:

    > python allTests.py

You can also run tests individually by changing to the test directory and running
this command:

    > python run.py

If everything worked out, you should see lots of `ok` messages. In case of a
failure, the tests abort with `failed`.

## IceGrid Admin Tool

Ice for Java includes a graphical administrative tool for IceGrid. It can be
found in the file `lib/icegridgui.jar`.

The JAR file is completely self-contained and has no external dependencies.
You can start the tool with the following command:

    > java -jar icegridgui.jar

In OS X there is also an application bundle named IceGrid Admin. You can start
the IceGrid Admin tool by double-clicking the IceGrid Admin icon in Finder.

[1]: https://zeroc.com/download.html
[2]: https://zeroc.com/platforms_3_6_0.html
[3]: http://gradle.org
[4]: http://proguard.sourceforge.net

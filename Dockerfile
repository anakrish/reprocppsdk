FROM alpine:3.12.3 AS cpprest-base-image

# Install prereqs
RUN apk add --no-cache curl build-base bash git boost-dev cmake zlib-dev openssl-dev ninja

RUN rm -rf /app;mkdir -p /app
	
WORKDIR /app

RUN git clone https://github.com/Microsoft/cpprestsdk.git

RUN cd cpprestsdk;\
        mkdir -p build.debug; cd build.debug;\
        cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCPPREST_EXCLUDE_WEBSOCKETS=ON  ..

RUN cd cpprestsdk; \
        ninja -C build.debug

# Install gdb for debugging
RUN apk add --no-cache gdb

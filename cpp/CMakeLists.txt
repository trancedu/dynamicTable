cmake_minimum_required(VERSION 3.16)
project(FinancialProducts LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Core Widgets REQUIRED)

# Update include paths to match actual connector structure
include_directories(
    /opt/homebrew/opt/mysql-connector-c++/include/cppconn  # Direct path to cppconn headers
    /opt/homebrew/opt/mysql-connector-c++/include  # Base include
    /opt/homebrew/opt/mysql-connector-c++/include/mysqlx  # For X DevAPI
    /opt/homebrew/opt/mysql-connector-c++/include/jdbc  # For JDBC
    /opt/homebrew/opt/openssl/include
)

link_directories(
    /opt/homebrew/opt/mysql-connector-c++/lib
    /opt/homebrew/opt/openssl/lib
)

# Add these definitions for MySQL connector
add_definitions(-DMYSQLCLIENT_STATIC_LINKING)
add_definitions(-DCPPCONN_PUBLIC_FUNC=)

# Model files
set(SOURCES
    FinancialProductModel.cpp
    ProductListModel.cpp
    FinancialProduct.cpp
    Option.cpp
    Swap.cpp
    main.cpp
    DatabaseOperations.cpp
)

set(HEADERS
    FinancialProductModel.h
    ProductListModel.h
    FinancialProduct.h
    Option.h
    Swap.h
    DatabaseOperations.h
)

add_executable(FinancialProducts ${SOURCES} ${HEADERS})

target_link_libraries(FinancialProducts PRIVATE
    Qt6::Core
    Qt6::Widgets
    mysqlcppconn
    mysqlclient
    ssl
    crypto
) 
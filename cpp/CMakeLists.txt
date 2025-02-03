cmake_minimum_required(VERSION 3.16)
project(FinancialProducts LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Core Widgets REQUIRED)

# Model files
set(SOURCES
    FinancialProductModel.cpp
    ProductListModel.cpp
    FinancialProduct.cpp
    Option.cpp
    Swap.cpp
    main.cpp
)

set(HEADERS
    FinancialProductModel.h
    ProductListModel.h
    FinancialProduct.h
    Option.h
    Swap.h
)

add_executable(FinancialProducts ${SOURCES} ${HEADERS})

target_link_libraries(FinancialProducts PRIVATE
    Qt6::Core
    Qt6::Widgets
) 
#include "DatabaseOperations.h"
#include <iostream>
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>
#include <memory>

using namespace std;

std::vector<FinancialProduct*> DatabaseOperations::loadProducts() {
    vector<FinancialProduct*> products;
    sql::Driver* driver = get_driver_instance();
    unique_ptr<sql::Connection> con(driver->connect("tcp://127.0.0.1:3306", "User", "user123"));
    con->setSchema("financial_product_db");

    // Load Options
    {
        unique_ptr<sql::Statement> stmt(con->createStatement());
        unique_ptr<sql::ResultSet> res(stmt->executeQuery("SELECT * FROM options"));
        
        while (res->next()) {
            Option* option = new Option(
                QString::fromStdString(res->getString("name")),
                res->getDouble("price"),
                res->getInt("quantity"),
                QString::fromStdString(res->getString("description")),
                res->getDouble("strike_price"),
                QString::fromStdString(res->getString("expiration")),
                res->getDouble("volatility")
            );
            option->setId(res->getInt("id"));
            products.push_back(option);
        }
    }

    // Load Swaps
    {
        unique_ptr<sql::Statement> stmt(con->createStatement());
        unique_ptr<sql::ResultSet> res(stmt->executeQuery("SELECT * FROM swaps"));
        
        while (res->next()) {
            Swap* swap = new Swap(
                QString::fromStdString(res->getString("name")),
                res->getDouble("price"),
                res->getInt("quantity"),
                QString::fromStdString(res->getString("description")),
                res->getDouble("fixed_rate"),
                res->getDouble("notional")
            );
            swap->setId(res->getInt("id"));
            products.push_back(swap);
        }
    }

    return products;
}

bool DatabaseOperations::saveProduct(FinancialProduct* product) {
    sql::Driver* driver = get_driver_instance();
    unique_ptr<sql::Connection> con(driver->connect("tcp://127.0.0.1:3306", "User", "user123"));
    con->setSchema("financial_product_db");
    con->setAutoCommit(false);

    try {
        if (auto option = dynamic_cast<Option*>(product)) {
            unique_ptr<sql::PreparedStatement> pstmt;
            
            if (product->id() == 0) {
                pstmt.reset(con->prepareStatement(
                    "INSERT INTO options (name, price, strike_price, expiration, volatility, quantity, description) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)"
                ));
            } else {
                pstmt.reset(con->prepareStatement(
                    "UPDATE options SET name=?, price=?, strike_price=?, expiration=?, volatility=?, quantity=?, description=? "
                    "WHERE id=?"
                ));
            }

            pstmt->setString(1, option->name().toStdString());
            pstmt->setDouble(2, option->price());
            pstmt->setDouble(3, option->strikePrice());
            pstmt->setString(4, option->expiration().toStdString());
            pstmt->setDouble(5, option->volatility());
            pstmt->setInt(6, option->quantity());
            pstmt->setString(7, option->description().toStdString());
            
            if (product->id() != 0) {
                pstmt->setInt(8, product->id());
            }

            pstmt->executeUpdate();

            if (product->id() == 0) {
                product->setId(getLastInsertId(*con));
            }
        }
        else if (auto swap = dynamic_cast<Swap*>(product)) {
            unique_ptr<sql::PreparedStatement> pstmt;
            
            if (product->id() == 0) {
                pstmt.reset(con->prepareStatement(
                    "INSERT INTO swaps (name, price, fixed_rate, notional, quantity, description) "
                    "VALUES (?, ?, ?, ?, ?, ?)"
                ));
            } else {
                pstmt.reset(con->prepareStatement(
                    "UPDATE swaps SET name=?, price=?, fixed_rate=?, notional=?, quantity=?, description=? "
                    "WHERE id=?"
                ));
            }

            pstmt->setString(1, swap->name().toStdString());
            pstmt->setDouble(2, swap->price());
            pstmt->setDouble(3, swap->fixedRate());
            pstmt->setDouble(4, swap->notional());
            pstmt->setInt(5, swap->quantity());
            pstmt->setString(6, swap->description().toStdString());
            
            if (product->id() != 0) {
                pstmt->setInt(7, product->id());
            }

            pstmt->executeUpdate();

            if (product->id() == 0) {
                product->setId(getLastInsertId(*con));
            }
        }

        con->commit();
        return true;
    } catch (sql::SQLException& e) {
        con->rollback();
        cerr << "SQL Error: " << e.what() << endl;
        return false;
    }
}

// Helper function to get last insert ID
int DatabaseOperations::getLastInsertId(sql::Connection& con) {
    unique_ptr<sql::Statement> stmt(con.createStatement());
    unique_ptr<sql::ResultSet> res(stmt->executeQuery("SELECT LAST_INSERT_ID()"));
    res->next();
    return res->getInt(1);
}

bool DatabaseOperations::updateProductPrice(int productId, double newPrice) {
    // Implement database update logic here
    // Example: Connect to database, execute UPDATE query
    return true;
} 
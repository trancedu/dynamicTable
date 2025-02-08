#pragma once
#include <vector>
#include "FinancialProduct.h"

// Add namespace forward declaration
namespace sql {
class Connection;
}

class DatabaseOperations {
public:
    static std::vector<FinancialProduct*> loadProducts();
    static bool saveProduct(FinancialProduct* product);
    static bool updateProductPrice(int productId, double newPrice);
    
private:
    static int getLastInsertId(sql::Connection& con);
}; 
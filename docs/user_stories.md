# E-commerce Backend User Stories Checklist

This document contains all user stories for the e-commerce backend project, organized by functional area with links to their corresponding GitHub issues.

## Legend

- **Completed** [x] - Issue is closed/done
- **In Progress** [ ] - Issue is currently being worked on
- **Planned** [ ] - Issue exists but not started

---

## Product & Category Management (Admin)

### Basic CRUD Operations - COMPLETED (Phase 1-3)

- [x] **As an** Administrator, **I want to** create a new product with a name, description, price, and stock quantity, **so that** I can add new items to the catalog.

  - **Status:** Completed in Phase 2
  - **Issue:** [#24 - Create Product Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/24)

- [x] **As an** Administrator, **I want to** view a list of all existing products, **so that** I can have an overview of the entire catalog.

  - **Status:** Completed in Phase 2
  - **Issue:** [#24 - Create Product Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/24)

- [x] **As an** Administrator, **I want to** update the details of an existing product, **so that** I can correct errors or change product information.

  - **Status:** Completed in Phase 2
  - **Issue:** [#24 - Create Product Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/24)

- [x] **As an** Administrator, **I want to** delete a product from the catalog, **so that** I can remove discontinued or unavailable items.

  - **Status:** Completed in Phase 2
  - **Issue:** [#24 - Create Product Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/24)

- [x] **As an** Administrator, **I want to** create a new product category, **so that** I can organize products effectively.

  - **Status:** Completed in Phase 2
  - **Issue:** [#23 - Create Category Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/23)

- [x] **As an** Administrator, **I want to** assign a product to a specific category, **so that** users can find it when browsing that category.

  - **Status:** Completed in Phase 2
  - **Issue:** [#24 - Create Product Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/24)

- [x] **As an** Administrator, **I want to** update or delete existing categories, **so that** I can manage the store's taxonomy.
  - **Status:** Completed in Phase 2
  - **Issue:** [#23 - Create Category Model and Admin CRUD APIs](https://github.com/joekariuki3/ecommerce_backend/issues/23)

### Enhanced Catalog Management - PLANNED (Phase 5)

- [ ] **As an** Administrator, **I want to** upload a CSV file to create multiple categories at once, **so that** I can efficiently set up my product taxonomy without manual entry.

  - **Status:** Planned
  - **Issue:** [#58 - CSV Category Bulk Upload](https://github.com/joekariuki3/ecommerce_backend/issues/58)

- [ ] **As an** Administrator, **I want to** upload a CSV file to create multiple products at once, **so that** I can quickly populate my catalog with inventory data.

  - **Status:** Planned
  - **Issue:** [#59 - CSV Product Bulk Upload](https://github.com/joekariuki3/ecommerce_backend/issues/59)

- [ ] **As an** Administrator, **I want to** download product and category data as CSV files, **so that** I can backup or analyze my catalog data externally.

  - **Status:** Planned
  - **Issue:** [#60 - CSV Export for Categories and Products](https://github.com/joekariuki3/ecommerce_backend/issues/60)

- [ ] **As an** Administrator, **I want to** see the status and results of bulk operations, **so that** I can identify and fix any import errors.

  - **Status:** Planned
  - **Issues:** Covered in [#58](https://github.com/joekariuki3/ecommerce_backend/issues/58) & [#59](https://github.com/joekariuki3/ecommerce_backend/issues/59)

- [ ] **As an** Administrator, **I want to** upload and manage product images, **so that** customers can see visual representations of products.

  - **Status:** Planned
  - **Issue:** [#61 - Product Image Management System](https://github.com/joekariuki3/ecommerce_backend/issues/61)

- [ ] **As an** Administrator, **I want to** manage product inventory levels with low-stock alerts, **so that** I can maintain adequate stock levels.
  - **Status:** Planned
  - **Issue:** [#62 - Product Inventory and Stock Management](https://github.com/joekariuki3/ecommerce_backend/issues/62)

### Advanced Product Features - PLANNED (Phase 6)

- [ ] **As an** Administrator, **I want to** set product variants (size, color, etc.), **so that** I can offer different options for the same product with individual pricing and inventory tracking.
  - **Status:** Planned
  - **Issue:** [#67 - Product Variants and Options System](https://github.com/joekariuki3/ecommerce_backend/issues/67)

---

## User Management & Authentication

### Basic Authentication - COMPLETED (Phase 1)

- [x] **As an** Unauthenticated User, **I want to** register for a new account using my email and a password, **so that** I can become a shopper.

  - **Status:** Completed in Phase 1
  - **Issue:** [#4 - User Registration API](https://github.com/joekariuki3/ecommerce_backend/issues/4)

- [x] **As an** Authenticated or Unauthenticated User, **I want to** log in with my credentials, **so that** I can access my account and protected features.

  - **Status:** Completed in Phase 1
  - **Issue:** [#5 - User Login API](https://github.com/joekariuki3/ecommerce_backend/issues/5)

- [x] **As an** Authenticated User, **I want to** log out of the system, **so that** I can securely end my session.

  - **Status:** Completed in Phase 1
  - **Issue:** [#6 - User Logout API](https://github.com/joekariuki3/ecommerce_backend/issues/6)

- [x] **As an** Authenticated User, **I want to** view and update my profile information (e.g., email, password), **so that** I can keep my account details current.
  - **Status:** Completed in Phase 1
  - **Issue:** [#7 - User Profile Management API](https://github.com/joekariuki3/ecommerce_backend/issues/7)

### Enhanced Profile Management - PLANNED (Phase 8)

- [ ] **As a** User, **I want to** manage my profile information easily, **so that** I can keep my account details current.

  - **Status:** Planned
  - **Issue:** [#74 - Enhanced User Profile Management](https://github.com/joekariuki3/ecommerce_backend/issues/74)

- [ ] **As a** User, **I want to** save multiple payment methods securely, **so that** checkout is faster in the future.

  - **Status:** Planned
  - **Issue:** [#74 - Enhanced User Profile Management](https://github.com/joekariuki3/ecommerce_backend/issues/74)

- [ ] **As a** User, **I want to** set preferences for notifications and communications, **so that** I control how the platform contacts me.
  - **Status:** Planned
  - **Issue:** [#74 - Enhanced User Profile Management](https://github.com/joekariuki3/ecommerce_backend/issues/74)

---

## Product Discovery (All Users)

### Basic Discovery - COMPLETED (Phase 3)

- [x] **As a** User (Guest or Shopper), **I want to** view a paginated list of all available products, **so that** I can browse the catalog without being overwhelmed.

  - **Status:** Completed in Phase 3
  - **Issue:** [#28 - Public Product Listing API with Pagination](https://github.com/joekariuki3/ecommerce_backend/issues/28)

- [x] **As a** User, **I want to** filter the product list by category, **so that** I can find items of a specific type.

  - **Status:** Completed in Phase 3
  - **Issue:** [#29 - Product Filtering by Category](https://github.com/joekariuki3/ecommerce_backend/issues/29)

- [x] **As a** User, **I want to** sort the visible products by price, **so that** I can find items within my budget.

  - **Status:** Completed in Phase 3
  - **Issue:** [#30 - Product Sorting by Price, Name, and Date](https://github.com/joekariuki3/ecommerce_backend/issues/30)

- [x] **As a** User, **I want to** sort the visible products by name or date added, **so that** I have multiple ways to organize my view.

  - **Status:** Completed in Phase 3
  - **Issue:** [#30 - Product Sorting by Price, Name, and Date](https://github.com/joekariuki3/ecommerce_backend/issues/30)

- [x] **As a** User, **I want to** search for a product by its name, **so that** I can quickly find a specific item I'm looking for.
  - **Status:** Completed in Phase 3
  - **Issue:** [#31 - Product Search by Name](https://github.com/joekariuki3/ecommerce_backend/issues/31)

### Enhanced Discovery - PLANNED (Phase 5-6)

- [ ] **As a** User, **I want to** see product availability status, **so that** I know if items are in stock before making decisions.

  - **Status:** Planned
  - **Issue:** [#62 - Product Inventory and Stock Management](https://github.com/joekariuki3/ecommerce_backend/issues/62)

- [ ] **As a** User, **I want to** search products using full-text search across name and description, **so that** I can find products more effectively.

  - **Status:** Planned
  - **Issue:** [#63 - Advanced Product Search with Full-Text Search](https://github.com/joekariuki3/ecommerce_backend/issues/63)

- [ ] **As a** User, **I want to** filter products by price range, **so that** I can find items within my budget.

  - **Status:** Planned
  - **Issue:** [#64 - Product Filtering by Price Range](https://github.com/joekariuki3/ecommerce_backend/issues/64)

- [ ] **As a** User, **I want to** see recently viewed products, **so that** I can easily return to items I was considering.

  - **Status:** Planned
  - **Issue:** [#65 - Recently Viewed Products Feature](https://github.com/joekariuki3/ecommerce_backend/issues/65)

- [ ] **As a** User, **I want to** see recommended products based on category browsing, **so that** I can discover related items.
  - **Status:** Planned
  - **Issue:** [#66 - Product Recommendations System](https://github.com/joekariuki3/ecommerce_backend/issues/66)

---

## Shopping Cart & Orders (Phase 7)

### Shopping Cart Management

- [ ] **As a** Registered User, **I want to** add products to my shopping cart and persist it across sessions, **so that** I can collect items for future purchase.

  - **Status:** Planned
  - **Issue:** [#68 - Shopping Cart Management System](https://github.com/joekariuki3/ecommerce_backend/issues/68)

- [ ] **As a** Guest User, **I want to** add products to a temporary cart, **so that** I can shop without creating an account.

  - **Status:** Planned
  - **Issue:** [#68 - Shopping Cart Management System](https://github.com/joekariuki3/ecommerce_backend/issues/68)

- [ ] **As a** User, **I want to** see my cart item count and total value, **so that** I know what I'm about to purchase.
  - **Status:** Planned
  - **Issue:** [#68 - Shopping Cart Management System](https://github.com/joekariuki3/ecommerce_backend/issues/68)

### Cart Operations

- [ ] **As a** User, **I want to** modify item quantities in my cart, **so that** I can adjust my order before checkout.

  - **Status:** Planned
  - **Issue:** [#69 - Cart Item Management (Add, Update, Remove)](https://github.com/joekariuki3/ecommerce_backend/issues/69)

- [ ] **As a** User, **I want to** remove items from my cart, **so that** I can eliminate unwanted products.

  - **Status:** Planned
  - **Issue:** [#69 - Cart Item Management (Add, Update, Remove)](https://github.com/joekariuki3/ecommerce_backend/issues/69)

- [ ] **As a** User, **I want to** add the same product with different variants, **so that** I can purchase multiple variations.
  - **Status:** Planned
  - **Issue:** [#69 - Cart Item Management (Add, Update, Remove)](https://github.com/joekariuki3/ecommerce_backend/issues/69)

### Order Management

- [ ] **As a** User, **I want to** convert my cart into an order, **so that** I can proceed to purchase the items.

  - **Status:** Planned
  - **Issue:** [#70 - Order Management System](https://github.com/joekariuki3/ecommerce_backend/issues/70)

- [ ] **As a** User, **I want to** view my order history, **so that** I can track my past purchases.

  - **Status:** Planned
  - **Issue:** [#70 - Order Management System](https://github.com/joekariuki3/ecommerce_backend/issues/70)

- [ ] **As an** Administrator, **I want to** view and manage all orders, **so that** I can handle fulfillment and customer service.
  - **Status:** Planned
  - **Issue:** [#70 - Order Management System](https://github.com/joekariuki3/ecommerce_backend/issues/70)

### Address Management

- [ ] **As a** User, **I want to** save multiple shipping addresses, **so that** I can ship to different locations easily.

  - **Status:** Planned
  - **Issue:** [#71 - User Address Management](https://github.com/joekariuki3/ecommerce_backend/issues/71)

- [ ] **As a** User, **I want to** set a default address, **so that** checkout is faster.

  - **Status:** Planned
  - **Issue:** [#71 - User Address Management](https://github.com/joekariuki3/ecommerce_backend/issues/71)

- [ ] **As a** User, **I want to** use different billing and shipping addresses, **so that** I have flexibility in my orders.
  - **Status:** Planned
  - **Issue:** [#71 - User Address Management](https://github.com/joekariuki3/ecommerce_backend/issues/71)

---

## Payment & Checkout (Phase 8)

### Checkout Process

- [ ] **As a** User, **I want to** review my order details before payment, **so that** I can verify everything is correct.

  - **Status:** Planned
  - **Issue:** [#72 - Checkout Process Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/72)

- [ ] **As a** User, **I want to** select shipping and billing addresses during checkout, **so that** I can control where my order goes.

  - **Status:** Planned
  - **Issue:** [#72 - Checkout Process Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/72)

- [ ] **As a** User, **I want to** see all costs broken down clearly, **so that** I understand what I'm paying for.
  - **Status:** Planned
  - **Issue:** [#72 - Checkout Process Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/72)

### Payment Processing

- [ ] **As a** User, **I want to** pay securely with my credit card, **so that** I can complete my purchase safely.

  - **Status:** Planned
  - **Issue:** [#73 - Payment Gateway Integration](https://github.com/joekariuki3/ecommerce_backend/issues/73)

- [ ] **As a** User, **I want to** receive immediate payment confirmation, **so that** I know my transaction was successful.

  - **Status:** Planned
  - **Issue:** [#73 - Payment Gateway Integration](https://github.com/joekariuki3/ecommerce_backend/issues/73)

- [ ] **As an** Administrator, **I want to** process refunds easily, **so that** I can handle returns and customer issues.
  - **Status:** Planned
  - **Issue:** [#73 - Payment Gateway Integration](https://github.com/joekariuki3/ecommerce_backend/issues/73)

---

## Customer Experience (Phase 9)

### Wishlist System

- [ ] **As a** User, **I want to** save products to a wishlist, **so that** I can purchase them later.

  - **Status:** Planned
  - **Issue:** [#75 - Wishlist System Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/75)

- [ ] **As a** User, **I want to** organize my wishlist into collections, **so that** I can categorize saved items.

  - **Status:** Planned
  - **Issue:** [#75 - Wishlist System Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/75)

- [ ] **As a** User, **I want to** easily move items from wishlist to cart, **so that** I can purchase saved products.
  - **Status:** Planned
  - **Issue:** [#75 - Wishlist System Implementation](https://github.com/joekariuki3/ecommerce_backend/issues/75)

### Promotions & Discounts

- [ ] **As an** Administrator, **I want to** create discount codes, **so that** I can run marketing campaigns.

  - **Status:** Planned
  - **Issue:** [#77 - Basic Promotion and Discount System](https://github.com/joekariuki3/ecommerce_backend/issues/77)

- [ ] **As a** User, **I want to** apply discount codes during checkout, **so that** I can save money on purchases.

  - **Status:** Planned
  - **Issue:** [#77 - Basic Promotion and Discount System](https://github.com/joekariuki3/ecommerce_backend/issues/77)

- [ ] **As an** Administrator, **I want to** set up automatic promotions, **so that** I can increase sales without manual intervention.
  - **Status:** Planned
  - **Issue:** [#77 - Basic Promotion and Discount System](https://github.com/joekariuki3/ecommerce_backend/issues/77)

---

## Analytics & Business Intelligence (Phase 10)

- [ ] **As an** Administrator, **I want to** view sales analytics dashboard, **so that** I can track business performance.

  - **Status:** Planned
  - **Issue:** [#76 - Sales Analytics and Reporting Dashboard](https://github.com/joekariuki3/ecommerce_backend/issues/76)

- [ ] **As an** Administrator, **I want to** see inventory analytics, **so that** I can optimize stock levels.

  - **Status:** Planned
  - **Issue:** [#76 - Sales Analytics and Reporting Dashboard](https://github.com/joekariuki3/ecommerce_backend/issues/76)

- [ ] **As an** Administrator, **I want to** analyze customer behavior, **so that** I can improve the platform.
  - **Status:** Planned
  - **Issue:** [#76 - Sales Analytics and Reporting Dashboard](https://github.com/joekariuki3/ecommerce_backend/issues/76)

---

## API & System Quality

### Documentation & CI/CD - IN PROGRESS (Phase 4)

- [x] **As a** Developer, **I want to** have comprehensive API documentation generated from the code, **so that** frontend developers can easily integrate with the backend.

  - **Status:** Completed in Phase 4
  - **Issue:** [#25 - Setup API Documentation with Swagger/OpenAPI](https://github.com/joekariuki3/ecommerce_backend/issues/25)

- [ ] **As a** Developer, **I want** the system to have a CI/CD pipeline, **so that** code changes are automatically tested, built, and deployed, ensuring reliability and speed.
  - **Status:** In Progress
  - **Issue:** [#22 - Configure GitHub Secrets and CI/CD Pipeline](https://github.com/joekariuki3/ecommerce_backend/issues/22)

### System Foundation - COMPLETED (Phase 1)

- [x] **As a** Developer, **I want to** have proper project structure and setup, **so that** development can proceed efficiently.

  - **Status:** Completed in Phase 1
  - **Issue:** [#1 - Setup Project Structure and Environment](https://github.com/joekariuki3/ecommerce_backend/issues/1)

- [x] **As a** Developer, **I want to** have database models properly configured with relationships, **so that** data integrity is maintained.

  - **Status:** Completed in Phase 1
  - **Issue:** [#2 - Setup Database Configuration and Models](https://github.com/joekariuki3/ecommerce_backend/issues/2)

- [x] **As a** Developer, **I want to** have JWT authentication middleware, **so that** protected routes are properly secured.
  - **Status:** Completed in Phase 1
  - **Issue:** [#3 - Implement JWT Authentication Middleware](https://github.com/joekariuki3/ecommerce_backend/issues/3)

---

## Progress Summary

### Completed Phases

- **Phase 1**: Project Foundation & Authentication (9/9 stories completed)
- **Phase 2**: Admin Catalog Management (2/2 stories completed)
- **Phase 3**: Public Product Discovery (4/4 stories completed)

### Current Phase

- **Phase 4**: Documentation & CI/CD (1/2 stories completed) - 1 remaining

### Upcoming Phases

- **Phase 5**: Enhanced Catalog Management (6 stories planned)
- **Phase 6**: Advanced Product Features (5 stories planned)
- **Phase 7**: Shopping Cart & Orders (9 stories planned)
- **Phase 8**: Payment & Checkout (6 stories planned)
- **Phase 9**: Customer Experience (6 stories planned)
- **Phase 10**: Analytics & Business Intelligence (3 stories planned)

**Overall Progress**: 16 of 51 user stories completed (31%)

---

## Quick Links to Active Issues

### Currently In Progress (Phase 4)

- [Issue #22 - Configure GitHub Secrets and CI/CD Pipeline](https://github.com/joekariuki3/ecommerce_backend/issues/22)

### Ready to Start (Phase 5)

- [Issue #58 - CSV Category Bulk Upload](https://github.com/joekariuki3/ecommerce_backend/issues/58)
- [Issue #59 - CSV Product Bulk Upload](https://github.com/joekariuki3/ecommerce_backend/issues/59)
- [Issue #60 - CSV Export for Categories and Products](https://github.com/joekariuki3/ecommerce_backend/issues/60)
- [Issue #61 - Product Image Management System](https://github.com/joekariuki3/ecommerce_backend/issues/61)
- [Issue #62 - Product Inventory and Stock Management](https://github.com/joekariuki3/ecommerce_backend/issues/62)

### Development Priority Recommendation

1. Complete Issue #22 to finish Phase 4
2. Start Phase 5 with Issue #61 (Product Images) for immediate visual impact
3. Follow with Issue #62 (Stock Management) for business value
4. Continue with CSV operations (#58, #59, #60) for administrative efficiency
